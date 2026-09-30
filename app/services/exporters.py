from __future__ import annotations

import uuid
from pathlib import Path

from fpdf import FPDF


ROOT = Path(
    __file__
).resolve().parents[2]


EXPORT_DIR = (
    ROOT
    / "static"
    / "exports"
)


def _font(
    pdf: FPDF,
    style: str = "",
) -> None:
    """
    Configure a standard PDF font.
    """

    pdf.set_font(
        "Helvetica",
        style=style,
        size=12,
    )


def save_pdf(
    title: str,
    layout: list[dict],
) -> str:
    """
    Create a multi-page PDF comic.
    """

    EXPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        f"comic-"
        f"{uuid.uuid4().hex[:10]}"
        f".pdf"
    )

    path = EXPORT_DIR / filename

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=16,
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_title(title)

        _font(
            pdf,
            "B",
        )

        pdf.cell(
            0,
            10,
            text=(
                f"Panel "
                f"{panel['panel_number']}: "
                f"{panel['title']}"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )

        image_path = (
            ROOT
            / panel["image_url"].lstrip("/")
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=15,
                y=32,
                w=180,
                h=135,
            )

            pdf.set_y(174)

        _font(pdf)

        pdf.multi_cell(
            0,
            7,
            text=panel[
                "scene_description"
            ],
        )

        pdf.ln(2)

        _font(
            pdf,
            "B",
        )

        pdf.multi_cell(
            0,
            7,
            text=(
                "Caption: "
                + panel["caption"]
            ),
        )

        _font(pdf)

        pdf.multi_cell(
            0,
            7,
            text=panel["narration"],
        )

        if panel.get("dialogue"):

            pdf.ln(2)

            _font(
                pdf,
                "I",
            )

            pdf.multi_cell(
                0,
                7,
                text=(
                    "Dialogue: "
                    + panel["dialogue"]
                ),
            )

    pdf.output(
        str(path)
    )

    return (
        f"/static/exports/{filename}"
    )