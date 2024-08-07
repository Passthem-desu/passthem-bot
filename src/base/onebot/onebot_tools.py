import nonebot

from src.base.onebot.onebot_api import get_group_list, send_group_msg, send_private_msg
from src.base.onebot.onebot_basic import MessageLike, OnebotBotProtocol
from src.common.config import config

LAST_CONTEXT_RECORDER: dict[int, int] = {}


def record_last_context(qqid: int, group_id: int | None = None):
    if group_id is None:
        LAST_CONTEXT_RECORDER.pop(qqid, None)
    else:
        LAST_CONTEXT_RECORDER[qqid] = group_id


async def broadcast(bot: OnebotBotProtocol, message: MessageLike):
    group_list = await get_group_list(bot)

    for group in group_list:
        if config.enable_white_list and group.group_id not in config.white_list_groups:
            continue

        await send_group_msg(bot, group.group_id, message)


async def tell(qqid: int, message: MessageLike, bot: OnebotBotProtocol | None = None):
    if bot is None:
        bot = nonebot.get_bot()

    if qqid not in LAST_CONTEXT_RECORDER:
        await send_private_msg(bot, qqid, message)
    else:
        await send_group_msg(bot, LAST_CONTEXT_RECORDER[qqid], message)
