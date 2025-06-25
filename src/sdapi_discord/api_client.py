import base64
import io
import json
import os
from typing import Optional

import httpx

from .exceptions import ApiClientError, ApiConnectionError, ApiTimeoutError


def generate_image(prompt: str, negative_prompt: Optional[str] = None, seed: Optional[int] = -1, steps: Optional[int] = 20, width: Optional[int] = 512, height: Optional[int] = 512, sampler: Optional[str] = "Euler a", cfg_scale: Optional[float] = 7.0) -> tuple[io.BytesIO, str]:
    api_url = os.getenv("SD_API_URL")
    if not api_url:
        raise ValueError("SD_API_URL is not set")

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "steps": steps,
        "width": width,
        "height": height,
        "sampler_name": sampler,
        "cfg_scale": cfg_scale,
    }

    try:
        with httpx.Client() as client:
            response = client.post(url=f'{api_url}/sdapi/v1/txt2img', json=payload, timeout=120)
            response.raise_for_status()
            r = response.json()
    except httpx.TimeoutException as e:
        raise ApiTimeoutError(f"API request timed out: {e}") from e
    except httpx.RequestError as e:
        raise ApiConnectionError(f"Failed to connect to API: {e}") from e

    if "images" not in r or not r["images"]:
        raise ApiClientError("No images in API response")

    try:
        image_data = base64.b64decode(r['images'][0])
        info = json.loads(r['info'])
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise ApiClientError(f"Failed to parse API response: {e}") from e

    return io.BytesIO(image_data), info
