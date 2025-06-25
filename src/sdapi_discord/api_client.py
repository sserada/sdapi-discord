import base64
import io
import os

import httpx
from PIL import Image


def async_generate_image(prompt: str) -> io.BytesIO:
    api_url = os.getenv("SD_API_URL")
    if not api_url:
        raise ValueError("SD_API_URL is not set")

    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 512,
        "height": 512,
    }

    with httpx.Client() as client:
        response = client.post(url=f'{api_url}/sdapi/v1/txt2img', json=payload, timeout=120)
        response.raise_for_status()
        r = response.json()

    if "images" not in r or not r["images"]:
        raise ValueError("No images in response")

    image_data = base64.b64decode(r['images'][0])
    return io.BytesIO(image_data)
