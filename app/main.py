from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


BASE_DIR = Path(__file__).resolve().parents[1]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create application directories when the server starts.
    """

    panels_directory = BASE_DIR / "static" / "panels"
    exports_directory = BASE_DIR / "static" / "exports"

    panels_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    exports_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    yield


app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description=(
        "Generate structured comic stories, AI illustrations, "
        "and downloadable PDF comics."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static",
)


app.include_router(router)


@app.get("/health")
async def health():
    """
    Simple health-check endpoint.
    """

    return {
        "status": "ok"
    }