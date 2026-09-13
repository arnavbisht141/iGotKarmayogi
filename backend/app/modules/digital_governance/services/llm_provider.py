"""Multi-LLM Round-Robin Provider for Digital Governance & Cybersecurity Content Generation.

Supports token round-robin key rotation across:
- Groq (llama-3.3-70b-versatile)
- NVIDIA NIM (meta/llama-3.1-70b-instruct)
- Google Gemini (gemini-1.5-flash / gemini-2.0-flash)
- OpenAI (gpt-4o-mini / gpt-4o)

Provides automatic failover across providers and an intelligent deterministic
fallback engine for offline or zero-token civil-service sandbox generation.
"""

import os
import re
import json
import logging
from typing import Dict, Any, List, Optional
import httpx

logger = logging.getLogger("digital_governance.llm")


class MultiLLMProvider:
    """
    Manages multi-provider LLM queries with token round-robin rotation,
    graceful provider failover, and civil-service heuristic fallback.
    """

    def __init__(self):
        # Parse comma-separated or single keys
        self.groq_keys = self._parse_keys("GROQ_API_KEY", "GROQ_API_KEYS")
        self.nim_keys = self._parse_keys("NIM_API_KEY", "NIM_API_KEYS")
        self.gemini_keys = self._parse_keys("GOOGLE_API_KEY", "GEMINI_API_KEY", "GEMINI_API_KEYS")
        self.openai_keys = self._parse_keys("OPENAI_API_KEY", "OPENAI_API_KEYS")

        # Models & base URLs (configured for low-traffic, high-throughput, minimal rate-limiting)
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.nim_model = os.getenv("NIM_MODEL", "meta/llama-3.1-8b-instruct")
        self.nim_base_url = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-8b")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # Key rotation indices
        self._key_indices = {
            "groq": 0,
            "nim": 0,
            "gemini": 0,
            "openai": 0,
        }

    def _parse_keys(self, *env_vars: str) -> List[str]:
        keys = []
        for var in env_vars:
            val = os.getenv(var, "").strip()
            if val:
                for k in val.split(","):
                    cleaned = k.strip()
                    if cleaned and cleaned not in keys:
                        keys.append(cleaned)
        return keys

    def get_next_key(self, provider: str) -> Optional[str]:
        """Rotate to the next API key in round-robin fashion for the given provider."""
        key_list = getattr(self, f"{provider}_keys", [])
        if not key_list:
            return None
        idx = self._key_indices[provider] % len(key_list)
        key = key_list[idx]
        self._key_indices[provider] = (idx + 1) % len(key_list)
        return key

    def get_provider_status(self) -> Dict[str, Any]:
        """Returns configured status of all supported LLM providers."""
        return {
            "groq": {"configured": len(self.groq_keys) > 0, "key_count": len(self.groq_keys), "model": self.groq_model},
            "nim": {"configured": len(self.nim_keys) > 0, "key_count": len(self.nim_keys), "model": self.nim_model},
            "gemini": {"configured": len(self.gemini_keys) > 0, "key_count": len(self.gemini_keys), "model": self.gemini_model},
            "openai": {"configured": len(self.openai_keys) > 0, "key_count": len(self.openai_keys), "model": self.openai_model},
        }

    async def call_groq(self, prompt: str, system_prompt: str = "", json_mode: bool = False) -> Optional[str]:
        key = self.get_next_key("groq")
        if not key:
            return None
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model": self.groq_model,
            "messages": messages,
            "temperature": 0.2,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
                logger.warning(f"Groq API returned status {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"Groq invocation failed: {e}")
        return None

    async def call_nim(self, prompt: str, system_prompt: str = "", json_mode: bool = False) -> Optional[str]:
        key = self.get_next_key("nim")
        if not key:
            return None
        url = f"{self.nim_base_url.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.nim_model,
            "messages": messages,
            "temperature": 0.2,
        }
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
                logger.warning(f"NVIDIA NIM returned status {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"NVIDIA NIM invocation failed: {e}")
        return None

    async def call_gemini(self, prompt: str, system_prompt: str = "", json_mode: bool = False) -> Optional[str]:
        key = self.get_next_key("gemini")
        if not key:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={key}"
        full_text = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        payload = {"contents": [{"parts": [{"text": full_text}]}]}
        if json_mode:
            payload["generationConfig"] = {"responseMimeType": "application/json"}

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                logger.warning(f"Google Gemini returned status {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"Google Gemini invocation failed: {e}")
        return None

    async def call_openai(self, prompt: str, system_prompt: str = "", json_mode: bool = False) -> Optional[str]:
        key = self.get_next_key("openai")
        if not key:
            return None
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model": self.openai_model,
            "messages": messages,
            "temperature": 0.2,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
                logger.warning(f"OpenAI returned status {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"OpenAI invocation failed: {e}")
        return None

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        json_mode: bool = False,
        preferred_provider: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes query through provider order:
        Preferred (if specified) -> Groq -> NIM -> Gemini -> OpenAI -> Heuristic Fallback.
        """
        providers = ["groq", "nim", "gemini", "openai"]
        if preferred_provider and preferred_provider in providers:
            providers.remove(preferred_provider)
            providers.insert(0, preferred_provider)

        for p in providers:
            caller = getattr(self, f"call_{p}")
            res = await caller(prompt, system_prompt=system_prompt, json_mode=json_mode)
            if res:
                return {
                    "text": res,
                    "provider": p,
                    "model": getattr(self, f"{p}_model"),
                    "is_fallback": False,
                }

        # Offline heuristic fallback
        return {
            "text": "",
            "provider": "heuristic_engine",
            "model": "rule-based-civil-defense",
            "is_fallback": True,
        }

    @staticmethod
    def parse_json_safely(raw_text: str) -> Optional[Dict[str, Any]]:
        """Safely extract JSON object from markdown fences or conversational output."""
        if not raw_text:
            return None
        clean = raw_text.strip()
        # Direct parse attempt
        try:
            return json.loads(clean)
        except Exception:
            pass
        # Regex search for JSON block
        match = re.search(r"\{[\s\S]*\}", clean)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        return None


llm_provider = MultiLLMProvider()
