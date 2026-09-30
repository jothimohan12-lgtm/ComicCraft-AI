from pydantic import BaseModel, Field, field_validator


class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1)
    title: str
    scene_description: str
    image_prompt: str


class PanelStory(BaseModel):
    panel_number: int = Field(ge=1)
    title: str
    caption: str
    narration: str
    dialogue: str = ""
    image_prompt: str


class ComicRequest(BaseModel):
    story_prompt: str = Field(
        min_length=5,
        max_length=2000,
    )

    character_name: str = Field(
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        min_length=1,
        max_length=120,
    )

    tone: str = Field(
        min_length=1,
        max_length=50,
    )

    art_style: str = Field(
        min_length=1,
        max_length=80,
    )

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style",
    )
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty.")

        return value


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
    image_url: str
    caption: str
    narration: str
    dialogue: str = ""


class ComicResponse(BaseModel):
    title: str
    panels: list[ComicPanel]
    pdf_url: str