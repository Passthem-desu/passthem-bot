from src.imports import *


@listenOnebot()
@matchRegex("^(mysp|我有多少薯片)$")
@withSessionLock()
async def _(ctx: OnebotMessageContext, session: AsyncSession, _):
    res = await session.execute(
        select(User.money).filter(User.qq_id == ctx.getSenderId())
    )
    res = res.scalar_one_or_none() or 0.0

    await ctx.reply(UniMessage(la.msg.mysp.format(f"{int(res)}{la.unit.money}")))
