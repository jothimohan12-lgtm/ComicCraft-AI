import json

from google import genai
from google.genai import types

from app.config import get_settings
from app.schemas import (
    ComicRequest,
    PanelOutline,
    PanelStory,
)


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


def generate_story(
    request: ComicRequest,
    outline: list[PanelOutline],
) -> list[PanelStory]:
    """
    Expand the structured outline into detailed comic narration,
    captions, dialogue, and image prompts.
    """

    settings = get_settings()

    outline_text = "\n\n".join(
        (
            f"Panel {panel.panel_number}: "
            f"{panel.title}\n"
            f"Scene: {panel.scene_description}\n"
            f"Image prompt: {panel.image_prompt}"
        )
        for panel in outline
    )

    prompt = f"""
Expand the following comic outline into polished comic storytelling.

ORIGINAL STORY IDEA:
{request.story_prompt}

MAIN CHARACTER:
{request.character_name}

SETTING:
{request.setting}

TONE:
{request.tone}

ART STYLE:
{request.art_style}

OUTLINE:
{outline_text}

Requirements:

1. Return exactly {settings.panel_count} panels.
2. Preserve all panel numbers.
3. Preserve the overall story sequence.
4. Keep character continuity.
5. Write a short caption for every panel.
6. Write concise narration for every panel.
7. Add dialogue when it improves the scene.
8. Keep dialogue natural and brief.
9. Do not introduce unnecessary major characters.
10. Do not unexpectedly change the setting.
11. Make the visual image prompt detailed.
12. Keep image prompts suitable for general audiences.
13. Make the complete story feel like one connected comic.
"""

    client = _client()

    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[PanelStory],
            temperature=0.9,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty comic story."
        )

    data = json.loads(response.text)

    stories = [
        PanelStory.model_validate(item)
        for item in data
    ]

    return stories