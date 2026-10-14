"""SiliconFlow multimodal chat client. Never stores or logs API keys."""

import base64
import mimetypes
from pathlib import Path

import requests


DEFAULT_BASE_URL = "https://api.siliconflow.cn/v1"
DEFAULT_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"


class SiliconFlowError(Exception):
    def __init__(self, message_key, status=None):
        super().__init__(message_key)
        self.message_key = message_key
        self.status = status


def call_siliconflow_vl(
    prompt, image_path, api_key, model=DEFAULT_MODEL, base_url=DEFAULT_BASE_URL
):
    """Return debate content or a locale-independent error for the UI to translate."""
    if not api_key:
        raise SiliconFlowError("api_key_missing")

    image_path = Path(image_path)
    try:
        encoded_image = base64.b64encode(image_path.read_bytes()).decode("ascii")
    except OSError as exc:
        raise SiliconFlowError("api_image_error") from exc

    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/jpeg"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 2000,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            timeout=(10, 120),
        )
    except requests.Timeout as exc:
        raise SiliconFlowError("api_timeout") from exc
    except requests.RequestException as exc:
        raise SiliconFlowError("api_connection") from exc

    if response.status_code != 200:
        raise SiliconFlowError("api_error", status=response.status_code)

    try:
        content = response.json()["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Empty content")
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise SiliconFlowError("api_invalid_response") from exc
    return content
