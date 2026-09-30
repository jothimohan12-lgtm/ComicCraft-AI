from app.schemas import (
    PanelOutline,
    PanelStory,
)


def build_comic_layout(
    outline: list[PanelOutline],
    story: list[PanelStory],
    image_urls: list[str],
) -> list[dict]:
    """
    Match outlines, story content, and generated images
    into the final panel layout.
    """

    stories = {
        panel.panel_number: panel
        for panel in story
    }

    layout = []

    for index, panel in enumerate(outline):

        item = stories.get(
            panel.panel_number
        )

        if item is None:
            raise ValueError(
                f"Missing story for panel "
                f"{panel.panel_number}"
            )

        if index >= len(image_urls):
            raise ValueError(
                f"Missing image for panel "
                f"{panel.panel_number}"
            )

        layout.append(
            {
                "panel_number": panel.panel_number,

                "title": (
                    item.title
                    or panel.title
                ),

                "scene_description": (
                    panel.scene_description
                ),

                "image_prompt": (
                    item.image_prompt
                    or panel.image_prompt
                ),

                "image_url": image_urls[index],

                "caption": item.caption,

                "narration": item.narration,

                "dialogue": item.dialogue,
            }
        )

    return layout