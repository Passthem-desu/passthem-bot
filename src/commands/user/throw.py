import time

from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot_plugin_alconna import At, Emoji, Reply, Text, UniMessage

from src.base.command_events import OnebotContext
from src.common.command_deco import listen_message, require_awake
from src.common.data.awards import use_award
from src.common.rd import get_random
from src.core.unit_of_work import get_unit_of_work
from src.services.stats import StatService

FREQUENCY_LIMIT: dict[int, float] = {}


def generate_throw_message(sender_id: int, target: int, success: bool, count: int):
    msg = (
        UniMessage.text(
            get_random().choice(
                (
                    "怎么有股臭味啊？原来 ",
                    "",
                    "突然，",
                    "在一瞬间，",
                    "不留神，",
                    "在背地里偷笑了一下的 ",
                    "脚滑的 ",
                    "肯定不是故意的 ",
                    "肯定是不小心的 ",
                )
            )
        )
        .at(user_id=str(sender_id))
        .text(" 向 ")
        .at(user_id=str(target))
        .text(" 扔出去了一个粑粑小哥，")
    )
    if success:
        msg.text(
            get_random().choice(
                (
                    "扔中了，粑粑小哥爬到了他的库存里面",
                    "完美的命中！",
                    "粑粑小哥奋力跑出加速度，进了他的库存",
                    "进球了！！！！",
                    "完美一击！",
                    "虽然偏了，但粑粑小哥像回旋镖一样命中了他的背后",
                    "中",
                    "三分球！",
                    "这下不用退钱了",
                    "实心球技术不错！",
                    "砸中了！",
                )
            )
        )
    else:
        msg.text(
            get_random().choice(
                (
                    "没扔中，粑粑小哥在地里烂掉了",
                    "偏了一点，下次努力吧！",
                    "粑粑小哥掉到八目鳗穴里了",
                    "结果不小心扔错了方向。",
                    "但在空中消失了",
                    "结果被龙卷风吸走了",
                    "却不小心掉到了池塘里面污染水质",
                    "被空中莫名出现的钢筋挡住了",
                    "但是却被吸入四维空间碎块了",
                    "这时候，路边的吹风机突然开始运作，粑粑被弹开了",
                )
            )
        )
    msg.text(f"（库存还有 {count} 个粑粑小哥）")
    return msg


async def analyze_throw_message(ctx: OnebotContext):
    is_throw = False
    is_poop = False
    target: set[int] = set()

    for segment in ctx.message:
        if isinstance(segment, Text):
            text = segment.text
            for i in (
                "史",
                "石",
                "屎",
                "粑粑",
                "💩",
                "大便",
                "便便",
                "大变",
                "大便",
                "答辩",
                "矢",
                "十",
            ):
                if i in text:
                    is_poop = True
            for i in ("丢", "扔", "抛", "吃", "赤", "吔", "叱", "持"):
                if i in text:
                    is_throw = True
            # 根据否定词的个数来判断是否表确定意义。
            nope_count = 0
            for i in ("不", "别", "莫", "讨厌", "勿"):
                nope_count += text.count(i)
            if nope_count % 2 == 1:
                return
        elif isinstance(segment, At):
            target.add(int(segment.target))
        elif isinstance(segment, Reply):
            if segment.origin is not None and isinstance(
                (msg := segment.origin), MessageSegment
            ):
                msgid: str | None = msg.data.get("id", None)
                if msgid is None:
                    continue
                res = await ctx.bot.call_api("get_msg", message_id=msgid)
                sender_obj = res.get("sender", None)
                if sender_obj is None:
                    return
                uid = sender_obj.get("user_id", None)
                if uid is None:
                    return
                target.add(int(uid))
        elif isinstance(segment, Emoji):
            if segment.id == "59":
                is_poop = True
        else:
            return

    if not is_throw or not is_poop or len(target) != 1:
        return

    return target.pop()


@listen_message()
@require_awake
async def _(ctx: OnebotContext):
    FREQUENCY_LIMIT.setdefault(ctx.sender_id, 0)
    if time.time() - FREQUENCY_LIMIT[ctx.sender_id] < 10:
        return
    FREQUENCY_LIMIT[ctx.sender_id] = time.time()

    target_qqid = await analyze_throw_message(ctx)

    if target_qqid is None:
        return
    if str(target_qqid) == ctx.bot.self_id:
        return
    if target_qqid == ctx.sender_id:
        # 如果是自己，就提示不能自丢。
        await ctx.reply(UniMessage.text("呀，你不能丢自己啊！"))
        return

    # 扔粑粑
    success = get_random().random() < 0.5

    async with get_unit_of_work(ctx.sender_id) as uow:
        fuid = await uow.users.get_uid(ctx.sender_id)
        tuid = await uow.users.get_uid(target_qqid)

        poop = await uow.awards.get_aid("粑粑小哥")
        if poop is None:
            return
        await use_award(uow, fuid, poop, 1)
        if success:
            await uow.inventories.give(tuid, poop, 1)

        count = await uow.inventories.get_storage(fuid, poop)
        stats = StatService(uow)
        await stats.throw_baba(fuid, tuid, success)

    await ctx.send(generate_throw_message(ctx.sender_id, target_qqid, success, count))
