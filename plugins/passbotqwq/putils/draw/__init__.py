import base64
import io
from typing import Tuple
import PIL
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


PILLOW_COLOR_LIKE = int | tuple[int] | tuple[int, int] | tuple[int, int, int] | tuple[int, int, int, int] | str | float | tuple[float]
PILLOW_COLOR_LIKE_WEAK = PILLOW_COLOR_LIKE | None

IMAGE = PIL.Image.Image

FONT_HARMONYOS_SANS = r'C:\Windows\Fonts\HarmonyOS_Sans_SC_Regular.ttf'
FONT_HARMONYOS_SANS_BLACK = r'C:\Windows\Fonts\HarmonyOS_Sans_SC_Black.ttf'


def newImage(size: Tuple[int, int] = (500, 500), color: PILLOW_COLOR_LIKE = 'white'):
    img = PIL.Image.new('RGB', size, color)
    return img


def imageToBytes(img: IMAGE):
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    return buffer.getvalue()


def _hello_world(text: str = '抓小哥图片合成测试中'):
    img = newImage(color='#000000')

    draw = PIL.ImageDraw.Draw(img)
    font = PIL.ImageFont.FreeTypeFont(FONT_HARMONYOS_SANS_BLACK, 32)

    left, top, right, bottom = font.getbbox(text)

    width = right - left
    height = top - bottom

    drawLeft = 250 - width / 2
    drawTop = 250 + height / 2

    draw.text((drawLeft, drawTop), text, "#ffffff", font)

    return imageToBytes(img)
