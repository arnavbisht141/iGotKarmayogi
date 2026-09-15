"""Sarvam AI speech for the oral board: speech-to-text for answers and text-to-speech for the board member.

The API key stays on the server; the browser only calls the behavioural speech endpoints.
"""
import base64
import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

SARVAM_BASE_URL = "https://api.sarvam.ai"
MAX_AUDIO_BYTES = 10 * 1024 * 1024
MAX_TTS_CHARS = 2500  # bulbul:v3 request limit
REQUEST_TIMEOUT_SECONDS = 60


class SpeechServiceError(RuntimeError):
    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


def _headers() -> dict:
    if not settings.SARVAM_API_KEY:
        raise SpeechServiceError("Sarvam speech services are not configured on the server.", 503)
    return {"api-subscription-key": settings.SARVAM_API_KEY}


def transcribe(audio: bytes, filename: str, content_type: str, language_code: str = "en-IN") -> dict:
    headers = _headers()
    if not audio:
        raise SpeechServiceError("The audio clip was empty.", 400)
    if len(audio) > MAX_AUDIO_BYTES:
        raise SpeechServiceError("The audio clip is too large.", 413)
    try:
        response = httpx.post(
            f"{SARVAM_BASE_URL}/speech-to-text",
            headers=headers,
            files={"file": (filename, audio, content_type)},
            data={"model": settings.SARVAM_STT_MODEL, "language_code": language_code},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as exc:
        logger.warning("Sarvam speech-to-text request failed: %s", exc)
        raise SpeechServiceError("The speech service could not be reached.") from exc
    if response.status_code != 200:
        logger.warning("Sarvam speech-to-text returned %s: %s", response.status_code, response.text[:300])
        raise SpeechServiceError("The speech service could not transcribe this clip.")
    body = response.json()
    return {"transcript": (body.get("transcript") or "").strip(), "language_code": body.get("language_code")}


def synthesize(text: str, language_code: str = "en-IN") -> bytes:
    headers = _headers()
    try:
        response = httpx.post(
            f"{SARVAM_BASE_URL}/text-to-speech",
            headers=headers,
            json={
                "text": text[:MAX_TTS_CHARS],
                "language_code": language_code,
                "model": settings.SARVAM_TTS_MODEL,
                "speaker": settings.SARVAM_TTS_SPEAKER,
                "output_audio_codec": "mp3",
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as exc:
        logger.warning("Sarvam text-to-speech request failed: %s", exc)
        raise SpeechServiceError("The speech service could not be reached.") from exc
    if response.status_code != 200:
        logger.warning("Sarvam text-to-speech returned %s: %s", response.status_code, response.text[:300])
        raise SpeechServiceError("The speech service could not generate audio.")
    audios = response.json().get("audios") or []
    if not audios:
        raise SpeechServiceError("The speech service returned no audio.")
    return base64.b64decode(audios[0])
