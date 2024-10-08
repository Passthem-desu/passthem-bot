from nonebot_plugin_alconna import UniMessage
from sqlalchemy import func, select

from src.base.command_events import MessageContext
from src.common.command_deco import (
    listen_message,
    match_regex,
    require_admin,
)
from src.core.unit_of_work import get_unit_of_work
from src.models.level import level_repo
from src.models.models import Award


@listen_message()
@require_admin()
@match_regex("^:: ?(所有|全部) ?(等级|级别) ?$")
async def _(ctx: MessageContext, _):
    async with get_unit_of_work() as uow:
        query = select(
            Award.level_id,
            func.count(Award.data_id),
        ).group_by(Award.level_id)
        counts = dict((await uow.session.execute(query)).tuples().all())
    levels = [
        (level.lid, level.display_name, level.weight, level.color, level.awarding)
        for level in level_repo.sorted
    ]

    weight_sum = sum((l[2] for l in levels))

    message = UniMessage("===== 所有等级 =====")

    for lid, name, weight, color_code, price in levels:
        if weight_sum > 0:
            prob = f"权重{weight} 概率{round(weight / weight_sum * 100, 2)}%"
        else:
            prob = f"权重{weight}"

        message += (
            f"\n- {name}[{color_code}] {prob} 奖励 {price}薯片 共有 {counts[lid]} 小哥"
        )

    await ctx.send(message)
