import json

from google import genai
from google.genai import types

from app.config import get_settings
from app.schemas import ComicRequest, PanelOutline


def _client() -> genai.Client:
    """
    Create the Gemini API client.
    """

    settings = get_settings()

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_outline(
    request: ComicRequest,
) -> list[PanelOutline]:
    """
    Generate a structured five-panel comic outline.
    """

    settings = get_settings()

    prompt = f"""
Create a cohesive {settings.panel_count}-panel comic outline.

USER STORY IDEA:
{request.story_prompt}

MAIN CHARACTER:
{request.character_name}

SETTING:
{request.setting}

TONE:
{request.tone}

ART STYLE:
{request.art_style}

Requirements:

1. Return exactly {settings.panel_count} panels.
2. Number panels from 1 through {settings.panel_count}.
3. The story must have a clear beginning.
4. Develop the conflict or central idea.
5. Include a meaningful turning point.
6. Finish with a satisfying ending.
7. Keep the main character visually consistent.
8. Keep the setting coherent.
9. scene_description must describe what should visibly appear.
10. image_prompt must be detailed enough for an image-generation model.
11. Keep image prompts safe and suitable for a general audience.
12. Make each panel visually distinct.
"""

    client = _client()

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[PanelOutline],
            temperature=0.8,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty comic outline."
        )

    data = json.loads(response.text)

    outlines = [
        PanelOutline.model_validate(item)
        for item in data
    ]

    return outlines