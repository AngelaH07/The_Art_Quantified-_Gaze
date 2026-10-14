"""SiliconFlow multimodal chat client. Never stores or logs API keys."""

import base64
import json
import mimetypes
from pathlib import Path

import requests
from urllib3.exceptions import ReadTimeoutError


DEFAULT_BASE_URL = "https://api.siliconflow.cn/v1"
DEFAULT_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"


class SiliconFlowError(Exception):
    def __init__(self, message_key, status=None):
        super().__init__(message_key)
        self.message_key = message_key
        self.status = status


def stream_siliconflow_vl(
    prompt, image_path, api_key, model=DEFAULT_MODEL, base_url=DEFAULT_BASE_URL
):
    """Yield answer chunks as they arrive, keeping the read timeout per chunk."""
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
        "stream": True,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=(10, 120),
        )
        try:
            if response.status_code != 200:
                raise SiliconFlowError("api_error", status=response.status_code)

            response.encoding = "utf-8"
            has_content = False
            completed = False
            for line in response.iter_lines(chunk_size=1024, decode_unicode=True):
                if not line:
                    continue
                try:
                    if isinstance(line, bytes):
                        line = line.decode("utf-8")
                    if not line.startswith("data:"):
                        continue  # SSE heartbeats and event metadata.
                    data = line[5:].strip()
                    if data == "[DONE]":
                        completed = True
                        break
                    chunk = json.loads(data)
                    if "error" in chunk:
                        raise SiliconFlowError("api_invalid_response")
                    choices = chunk.get("choices", [])
                    if not isinstance(choices, list):
                        raise ValueError("Invalid choices")
                    for choice in choices:
                        delta = choice.get("delta") or {}
                        text = delta.get("content")
                        if text is not None and not isinstance(text, str):
                            raise ValueError("Invalid content")
                        if choice.get("finish_reason") is not None:
                            completed = True
                        if text:
                            has_content = has_content or bool(text.strip())
                            yield text
                except (ValueError, KeyError, TypeError, AttributeError) as exc:
                    raise SiliconFlowError("api_invalid_response") from exc
            if not has_content:
                raise SiliconFlowError("api_invalid_response")
            if not completed:
                raise SiliconFlowError("api_incomplete_response")
        finally:
            response.close()
    except requests.RequestException as exc:
        # Requests wraps read timeouts raised during iter_lines in ConnectionError.
        if isinstance(exc, requests.Timeout) or any(
            isinstance(arg, ReadTimeoutError) for arg in exc.args
        ):
            raise SiliconFlowError("api_timeout") from exc
        raise SiliconFlowError("api_connection") from exc


def call_siliconflow_vl(
    prompt, image_path, api_key, model=DEFAULT_MODEL, base_url=DEFAULT_BASE_URL
):
    """Collect the same stream for callers that need a completed string."""
    return "".join(stream_siliconflow_vl(prompt, image_path, api_key, model, base_url))
