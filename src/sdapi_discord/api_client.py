import base64
import io
import json
import os
from typing import Optional

import httpx


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

    with httpx.Client() as client:
        response = client.post(url=f'{api_url}/sdapi/v1/txt2img', json=payload, timeout=120)
        response.raise_for_status()
        r = response.json()

    if "images" not in r or not r["images"]:
        raise ValueError("No images in response")

    image_data = base64.b64decode(r['images'][0])
    info = json.loads(r['info'])
    return io.BytesIO(image_data), info
