import json
import re


def parse_llm_json(text: str):
    """Extracts the JSON object/array from an LLM reply, tolerating code fences and prose."""
    if not text:
        raise ValueError("empty LLM response")
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if fenced:
        text = fenced.group(1)
    starts = [i for i in (text.find("{"), text.find("[")) if i != -1]
    if not starts:
        raise ValueError("no JSON found in LLM response")
    end = max(text.rfind("}"), text.rfind("]"))
    return json.loads(text[min(starts):end + 1])
