"""
包装的 HTML 转图像的工具，包含各种模板套用等工具
"""

# 我了个爆豆啊，怎么又有 Stub 文件找不到
import asyncio
import base64
import pathlib
import shutil
import time
import uuid
from typing import Any

import jinja2
from html2image import Html2Image
from nonebot import get_driver, logger  # type: ignore

from src.common.decorators.threading import make_async
from src.common.draw.texts import Fonts

temp_base = pathlib.Path("./data/temp/screenshot/")


html_to_image = Html2Image(output_path=str(temp_base.absolute()))
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(pathlib.Path("./templates/"))
)


@make_async
def clear_temp_screenshot():
    """
    清空临时文件夹中的截图文件
    """

    for fp in temp_base.iterdir():
        shutil.rmtree(fp)


def screenshot(html: str, render_size: tuple[int, int]):
    """使用 html2image 接口渲染一张图片

    Args:
        html (str): HTML 文本
        render_size (tuple[int, int]): 渲染的图片大小

    Returns:
        pathlib.Path: 文件的地址
    """

    begin = time.time()
    fn = f"screenshot-{uuid.uuid4().hex}.png"
    html_to_image.screenshot(html, size=render_size, save_as=fn)  # type: ignore
    logger.info(time.time() - begin)
    return temp_base / fn


@make_async
def render(template: str, render_size: tuple[int, int], *args: Any, **kwargs: Any):
    """从模板渲染一张图片

    Args:
        template (str): 模板文件名，遵守 jinja2 的规则
        render_size (tuple[int, int]): 渲染的图片大小

    Returns:
        pathlib.Path: 创建的临时文件的位置
    """
    tpl = jinja_environment.get_template(template)
    res = tpl.render(
        *args,
        **kwargs,
        passbot_fonts=[
            {
                "name": f.name,
                "base64": base64.b64encode((pathlib.Path(f.value)).read_bytes()).decode(),
            }
            for f in Fonts
        ],
    )

    if get_driver().env == "dev":
        with open(temp_base / "test.html", "w", encoding="utf-8") as f:
            f.write(res)

    return screenshot(res, render_size)
