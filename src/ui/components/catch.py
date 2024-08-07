import PIL
import PIL.Image
import PIL.ImageChops
import PIL.ImageDraw
from imagetext_py import TextAlign

from src.ui.base.basics import Fonts, paste_image, render_text
from src.ui.components.awards import display_box
from src.ui.views.award import AwardDisplay


def catch(data: AwardDisplay, background: str = "#9B9690") -> PIL.Image.Image:
    """
    渲染 AwardDetail
    """

    left_display = display_box(data)
    rightDescription = render_text(
        text=data.info.description,
        width=567,
        color="#ffffff",
        font=[Fonts.VONWAON_BITMAP_16, Fonts.MAPLE_UI],
        font_size=16,
        line_spacing=1.25,
        paragraph_spacing=15,
    )
    rightTitle = render_text(
        text=data.info.display_name,
        font_size=43,
        color="#ffffff",
        font=[Fonts.JINGNAN_JUNJUN, Fonts.ALIMAMA_SHU_HEI, Fonts.MAPLE_UI],
    )
    rightStar = render_text(
        text=data.info.level.display_name,
        width=400,
        font_size=43,
        align=TextAlign.Right,
        color=data.info.level.color,
        font=Fonts.MAPLE_UI,
    )
    leftNotation = render_text(
        text=data.notation,
        color=(
            "#FFFFFF"
            if data.notation == "+1"
            else "#FFFD55" if data.notation == "+2" else "#8BFA84"
        ),
        font=Fonts.MARU_MONICA,
        font_size=48,
        margin_bottom=5,
        margin_top=0,
        margin_left=0,
    )
    leftNotationShadow = render_text(
        text=data.notation,
        color="#000000",
        font=Fonts.MARU_MONICA,
        font_size=48,
        margin_bottom=5,
        margin_top=3,
        margin_left=3,
    )

    block = PIL.Image.new(
        "RGBA", (800, max(180, rightDescription.height + 89)), background
    )
    paste_image(block, left_display, 18, 18)
    paste_image(block, rightTitle, 212, 18)
    paste_image(block, rightDescription, 212, 75)
    paste_image(block, rightStar, 379, 14)
    paste_image(block, leftNotationShadow, 26, 107)
    paste_image(block, leftNotation, 26, 107)

    return block
