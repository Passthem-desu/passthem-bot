import PIL
import PIL.Image
from src.common.dataclasses.shop_data import ProductData
from src.common.draw.texts import Fonts, drawASingleLineClassic, drawLimitedBoxOfTextClassic
from src.components.display_box import display_box


async def product_box(product: ProductData):
    left_display = await display_box(product.background_color, product.image, False)
    rightDescription = await drawLimitedBoxOfTextClassic(
        text=product.description,
        maxWidth=567,
        lineHeight=19,
        color="#ffffff",
        font=Fonts.VONWAON_BITMAP_16,
        fontSize=16,
    )
    rightTitle = await drawASingleLineClassic(
        text=product.title,
        fontSize=43,
        color="#ffffff",
        font=Fonts.HARMONYOS_SANS_BLACK,
    )

    if product.sold_out:
        image_new = PIL.Image.open("./res/new.png")
        image_new = image_new.convert("RGBA")

        left_display.paste(image_new, (88, 0), image_new)

    block = PIL.Image.new(
        "RGB", (800, max(180, rightDescription.height + 89)), "#9B9690"
    )
    block.paste(left_display, (18, 18), left_display)
    block.paste(rightTitle, (212, 18), rightTitle)
    block.paste(rightDescription, (212, 75), rightDescription)

    return block
