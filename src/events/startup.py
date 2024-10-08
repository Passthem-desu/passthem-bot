import functools

import nonebot
from loguru import logger

from src.base.db import DatabaseManager
from src.base.event.event_timer import addInterval
from src.common.config import get_config

driver = nonebot.get_driver()


@driver.on_startup
async def _():
    @functools.partial(addInterval, get_config().autosave_interval, skip_first=True)
    async def _():
        await DatabaseManager.get_single().manual_checkpoint()
        logger.info("数据库自动保存指令执行完了。")
