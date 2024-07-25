from typing import Any

from nonebot_plugin_alconna import UniMessage

from src.ui.base.basics import Fonts, horizontal_pile, render_text, vertical_pile
from src.ui.base.tools import image_to_bytes
from src.ui.components.awards import display_box
from src.ui.components.catch import catch
from src.ui.views.recipe import MergeResult
from utils.threading import make_async


def render_merge_image(data: MergeResult):
    area_title_1 = render_text(
        text=data.title1,
        width=567,
        color="#FFFFFF",
        font=Fonts.HARMONYOS_SANS_BLACK,
        font_size=80,
        margin_bottom=30,
    )

    mats = [display_box(inp) for inp in data.inputs]
    area_material_box = horizontal_pile(
        images=mats,
        background="#8A8580",
        paddingX=24,
        marginLeft=18,
        marginBottom=24,
    )

    area_title_2 = render_text(
        text=data.title2,
        width=567,
        color="#FFFFFF",
        font=Fonts.HARMONYOS_SANS_BLACK,
        font_size=60,
        margin_bottom=18,
    )

    area_product_entry = catch(data.output)

    area_title_3 = render_text(
        text=data.title3,
        width=567,
        color="#FFFFFF",
        font=Fonts.HARMONYOS_SANS_BLACK,
        font_size=24,
        margin_top=12,
    )

    return vertical_pile(
        [
            area_title_1,
            area_material_box,
            area_title_2,
            area_product_entry,
            area_title_3,
        ],
        15,
        "left",
        "#8A8580",
        60,
        60,
        60,
        60,
    )


async def render_merge_message(data: MergeResult) -> UniMessage[Any]:
    image = await make_async(image_to_bytes)(await make_async(render_merge_image)(data))

    return UniMessage.image(raw=image)
