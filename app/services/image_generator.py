from __future__ import annotations

import re
import uuid
from pathlib import Path

from PIL import Image, ImageDraw

from app.config import get_settings


ROOT = Path(__file__).resolve().parents[2]

PANEL_DIR = (
    ROOT
    / "static"
    / "panels"
)


def _safe_name(prompt: str) -> str:
    """
    Convert an image prompt into a safe filename.
    """

    slug = re.sub(
        r"[^a-zA-Z0-9]+",
        "-",
        prompt.lower(),
    )

    slug = slug.strip("-")

    slug = slug[:45]

    if not slug:
        slug = "panel"

    return (
        f"{slug}-"
        f"{uuid.uuid4().hex[:8]}"
        ".png"
    )


def _placeholder(
    prompt: str,
    path: Path,
) -> None:
    """
    Generate a simple placeholder image.

    Useful for testing the application without
    configuring an image-generation provider.
    """

    image = Image.new(
        "RGB",
        (1024, 768),
        "#f3efe5",
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (24, 24, 1000, 744),
        outline="#222222",
        width=8,
    )

    draw.text(
        (60, 70),
        "ComicCraft Preview",
        fill="#222222",
    )

    cleaned_prompt = " ".join(
        prompt.split()
    )

    draw.multiline_text(
        (60, 150),
        cleaned_prompt[:500],
        fill="#333333",
        spacing=10,
    )

    image.save(
        path,
        format="PNG",
    )


def _hf_image(
    prompt: str,
) -> Image.Image:
    """
    Generate an image through Hugging Face.
    """

    from huggingface_hub import InferenceClient

    settings = get_settings()

    if not settings.hf_token:
        raise RuntimeError(
            "HF_TOKEN is required when "
            "IMAGE_PROVIDER=hf."
        )

    client = InferenceClient(
        api_key=settings.hf_token,
        provider="auto",
    )

    image = client.text_to_image(
        prompt=prompt,
        model=settings.hf_image_model,
    )

    return image


def _local_diffusion(
    prompt: str,
) -> Image.Image:
    """
    Generate an image using local Diffusers.
    """

    import torch

    from diffusers import StableDiffusionPipeline

    settings = get_settings()

    device = settings.local_image_device

    if device == "auto":
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

    pipe = StableDiffusionPipeline.from_pretrained(
        settings.local_image_model
    )

    pipe = pipe.to(device)

    result = pipe(
        prompt,
        num_inference_steps=settings.local_image_steps,
        height=768,
        width=1024,
    )

    return result.images[0]


def generate_image(
    prompt: str,
) -> str:
    """
    Generate and save an image for a comic panel.

    Returns a browser-accessible static URL.
    """

    settings = get_settings()

    PANEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = _safe_name(prompt)

    path = PANEL_DIR / filename

    provider = settings.image_provider.lower()

    try:

        if provider == "hf":

            image = _hf_image(prompt)

            image.save(
                path,
                format="PNG",
            )

        elif provider == "local":

            image = _local_diffusion(prompt)

            image.save(
                path,
                format="PNG",
            )

        else:

            _placeholder(
                prompt,
                path,
            )

    except Exception:
        """
        If an optional image provider fails,
        keep the rest of ComicCraft usable.
        """

        _placeholder(
            prompt,
            path,
        )

    return (
        f"/static/panels/{filename}"
    )