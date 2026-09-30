from app.schemas import ComicRequest

from app.services.exporters import save_pdf
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout


def generate_comic(
    request: ComicRequest,
) -> dict:
    """
    Execute the complete ComicCraft pipeline.

    1. Generate outline.
    2. Generate story.
    3. Generate panel images.
    4. Build layout.
    5. Export PDF.
    """

    outline = generate_outline(
        request
    )

    if len(outline) != 5:
        raise RuntimeError(
            "Expected 5 panels, "
            f"received {len(outline)}."
        )

    story = generate_story(
        request,
        outline,
    )

    if len(story) != 5:
        raise RuntimeError(
            "Expected 5 story panels, "
            f"received {len(story)}."
        )

    image_urls = [
        generate_image(
            panel.image_prompt
        )
        for panel in story
    ]

    layout = build_comic_layout(
        outline,
        story,
        image_urls,
    )

    title = (
        "ComicCraft: "
        f"{request.character_name}'s Story"
    )

    pdf_url = save_pdf(
        title,
        layout,
    )

    return {
        "title": title,
        "panels": layout,
        "pdf_url": pdf_url,
    }