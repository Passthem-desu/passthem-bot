"""
在目前的开发阶段，有很多需要用到的功能，例如同步存档之类。
如果有一些需要方便开发的指令，就写到这里吧！
"""

import subprocess
from pathlib import Path

from src.base.command_events import GroupContext, OnebotContext
from src.base.db import DatabaseManager
from src.common.decorators.command_decorators import (
    listenGroup,
    listenOnebot,
    matchLiteral,
    matchRegex,
    requireAdmin,
)
from src.common.get_local_ip import get_ip
from src.common.save_file_handler import pack_save


@listenOnebot()
@requireAdmin()
@matchLiteral("::get-ip")
async def _(ctx: OnebotContext):
    await ctx.reply("\n".join(get_ip()))


@listenOnebot()
@requireAdmin()
@matchLiteral("::manual-save")
async def _(ctx: OnebotContext):
    await DatabaseManager.get_single().manual_checkpoint()
    await ctx.reply("ok")


@listenGroup()
@requireAdmin()
@matchRegex(
    "^:: ?(导出|输出|保存|发送|生成|构建|建造|吐出|献出) ?(你(自己)?的)? ?(存档|文件|心脏|大脑)$"
)
async def _(ctx: GroupContext, _):
    await DatabaseManager.get_single().manual_checkpoint()
    fp = await pack_save()
    await ctx.bot.call_api(
        "upload_group_file",
        group_id=ctx.event.group_id,
        file=str(fp.absolute()),
        name=fp.name,
    )


@listenOnebot()
@requireAdmin()
@matchLiteral("::reload-script")
async def _(ctx: OnebotContext):
    await ctx.reply("服务器即将重启")
    subprocess.call(["sh", Path("./linux/upgrade.sh")])
