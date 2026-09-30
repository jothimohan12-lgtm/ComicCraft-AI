# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI web application that transforms a user's story idea into a five-panel AI-generated comic.

## Features

- Story prompt input
- Character customization
- Setting customization
- Story tone selection
- Art style selection
- Gemini AI comic outline generation
- Gemini AI narration and dialogue generation
- AI image generation
- Comic preview
- PDF export
- JSON API
- FastAPI Swagger documentation
- Image-generation test endpoint
- Health endpoint

## Technology

Frontend:

- HTML
- CSS
- JavaScript
- Jinja2

Backend:

- Python
- FastAPI
- Uvicorn
- Pydantic

AI:

- Google Gemini
- Hugging Face
- Optional local Stable Diffusion

PDF:

- fpdf2

## Project structure

```text
ComicCraft/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routes.py
│   ├── schemas.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       ├── exporters.py
│       └── workflow.py
│
├── templates/
├── static/
├── tests/
├── .env
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md