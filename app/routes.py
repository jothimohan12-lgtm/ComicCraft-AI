from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.schemas import ComicRequest
from app.services.image_generator import generate_image
from app.services.workflow import generate_comic


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    """
    Render the ComicCraft homepage.
    """

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "settings": get_settings()
        },
    )


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate_form(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):
    """
    Generate a comic from HTML form data.
    """

    try:
        payload = ComicRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        comic = generate_comic(payload)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "comic": comic
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "settings": get_settings(),
                "error": str(exc),
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_json(payload: ComicRequest):
    """
    Generate a comic through the JSON API.
    """

    try:

        return generate_comic(payload)

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    pdf: str = "",
):
    """
    Display PDF export confirmation.
    """

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "pdf_url": pdf
        },
    )


@router.post("/test-image")
async def test_image(
    prompt: str = Form(...),
):
    """
    Developer endpoint for testing image generation.
    """

    try:

        image_url = generate_image(prompt)

        return {
            "image_url": image_url
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc