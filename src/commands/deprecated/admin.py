from dataclasses import dataclass
import re
from typing import Any, Callable, Coroutine, cast
from nonebot.adapters.onebot.v11 import Message

from .old_version import (
    CheckEnvironment,
    at,
    localImage,
    text,
    Command,
    CallbackBase,
    WaitForMoreInformationException,
    databaseIO
)
from src.common.download import download, writeData
from .db import *
from .messages import *

from src.models import *

from src.common.db import AsyncSession


def isFloat():
    def inner(x: str):
        try:
            float(x)
            return True
        except:
            pass
        return False

    return inner


def combine(*rules: Callable[[str], bool]):
    def inner(x: str):
        for rule in rules:
            if not rule(x):
                return False

        return True

    return inner

def not_negative():
    def inner(x: str):
        return float(x) >= 0

    return combine(isFloat(), inner)





from .keywords import *
from .tools import getSender, isValidColorCode, requireAdmin


@requireAdmin
@dataclass
class CatchAllLevel(Command):
    commandPattern: str = f"^:: ?{KEYWORD_EVERY}{KEYWORD_LEVEL}"
    argsPattern: str = "$"

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        return await allLevels(env.session)


@requireAdmin
@dataclass
class CatchAllAwards(Command):
    commandPattern: str = f"^:: ?{KEYWORD_EVERY}{KEYWORD_AWARDS}"
    argsPattern: str = "$"

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        return await allAwards(env.session)


@requireAdmin
@databaseIO()
class CatchSetInterval(Command):
    def __init__(self):
        super().__init__(f"^:: ?{KEYWORD_CHANGE} ?{KEYWORD_INTERVAL}", " ?(-?[0-9]+)$")

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return setIntervalWrongFormat()

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        interval = int(result.group(3))
        await setInterval(env.session, interval)
        message = settingOk()

        return message


@requireAdmin
@databaseIO()
class Give(Command):
    def __init__(self):
        super().__init__(
            "^/give",
            " (\\d+) (\\S+)( \\d+)?$",
        )

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message(
            [
                at(env.sender),
                text(" Invalid format, expected /give <uid> <awardName>"),
            ]
        )

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        award = await getAwardByName(env.session, result.group(2))

        if award is None:
            return self.notExists(env, result.group(2))

        count = 1

        if result.group(3):
            count = int(result.group(3)[1:])

        await giveAward(
            env.session,
            await getUser(env.session, int(result.group(1))),
            award,
            count,
        )

        message = Message(
            [at(env.sender), text(f" : 已将 {award.name} 给予用户 {result.group(1)}")]
        )

        return message


@requireAdmin
@databaseIO()
class Clear(Command):
    def __init__(self):
        super().__init__(
            "^/clear",
            "( (\\d+)( (\\S+))?)?$",
        )

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message(
            [
                at(env.sender),
                text(" Invalid format."),
            ]
        )

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        if result.group(2) == None:
            await clearUserStorage(env.session, await getSender(env))

            return Message([at(env.sender), text(f" 清空了你的背包")])

        user = await getUser(env.session, int(result.group(2)))

        if result.group(4) == None:
            await clearUserStorage(env.session, user)

            return Message(
                [
                    at(env.sender),
                    text(f" 清空了 {result.group(2)} 的背包"),
                ]
            )

        award = await getAwardByName(env.session, result.group(4))

        if award is None:
            return self.notExists(env, result.group(4))

        await clearUserStorage(env.session, user, award)

        return Message(
            [
                at(env.sender),
                text(f" 清空了 {result.group(2)} 背包里的所有 {result.group(4)}"),
            ]
        )


@requireAdmin
@databaseIO()
@dataclass
class CatchLevelModify(Command):
    commandPattern: str = (
        f"^:: ?{KEYWORD_CHANGE} ?{KEYWORD_LEVEL} ?(名称|名字|权重|色值|色号|颜色|奖励|金钱|获得|优先级|优先度|优先)"
    )
    argsPattern: str = " ?(\\S+) (.+)$"

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message([at(env.sender), text("MSG_MODIFY_LEVEL_WRONG_FORMAT")])

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        level = await getLevelByName(env.session, result.group(4))

        if level is None:
            return self.notExists(env, result.group(4))

        modifyElement = result.group(3)
        data = result.group(5)

        if modifyElement == "名称" or modifyElement == "名称":
            level.name = data
        elif modifyElement == "权重":
            if not not_negative()(data):
                return Message([at(env.sender), text("MSG_WEIGHT_INVALID")])

            level.weight = float(data)
        elif (
            modifyElement == "金钱"
            or modifyElement == "获得"
            or modifyElement == "奖励"
        ):
            if not not_negative()(data):
                return Message([at(env.sender), text("MSG_MONEY_INVALID")])

            level.price = int(data)
        elif (
            modifyElement == "优先级"
            or modifyElement == "优先度"
            or modifyElement == "优先"
        ):
            if re.match("^-?\\d+$", data):
                level.sorting_priority = int(data)
        else:
            if not isValidColorCode(data):
                return Message([at(env.sender), text("MSG_COLOR_CODE_INVALID")])

            level.color_code = data

        return modifyOk()


@requireAdmin
@databaseIO()
@dataclass
class CatchCreateLevel(Command):
    commandPattern: str = f"^:: ?{KEYWORD_CREATE} ?{KEYWORD_LEVEL} "
    argsPattern: str = "(\\S+)$"

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        levelName = result.group(3)

        existLevel = await getLevelByName(env.session, levelName)

        if existLevel is not None:
            return Message([at(env.sender), text("MSG_LEVEL_ALREADY_EXISTS")])

        level = Level(name=levelName, weight=0)

        env.session.add(level)

        return Message([at(env.sender), text("ok")])


@requireAdmin
@databaseIO()
@dataclass
class CatchAddSkin(Command):
    commandPattern: str = f"^:: ?{KEYWORD_CREATE} ?{KEYWORD_SKIN} "
    argsPattern: str = "(\\S+) (\\S+)$"

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message([at(env.sender), text("MSG_CREATE_SKIN_WRONG_FORMAT")])

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        award = await getAwardByName(env.session, result.group(3))

        if award is None:
            return self.notExists(env, result.group(3))

        skin = await getSkinByName(env.session, result.group(4))

        if skin is not None:
            return Message([at(env.sender), text("MSG_SKIN_ALREADY_EXISTS")])

        skin = Skin(name=result.group(4), award=award)

        env.session.add(skin)

        return Message([at(env.sender), text("MSG_SKIN_ADDED_SUCCESSFUL")])


@dataclass
class CatchModifySkinCallback(CallbackBase):
    skin_id: int
    param: str

    async def callback(self, env: CheckEnvironment) -> Message | None:
        skin = await getSkinById(env.session, self.skin_id)

        if self.param == "名字" or self.param == "名称":
            if not re.match("^\\S+$", env.text):
                raise WaitForMoreInformationException(
                    self, Message([at(env.sender), text("MSG_INPUT_NAME_WRONG_FORMAT")])
                )

            skin.name = env.text
            return modifyOk()

        if self.param == "描述":
            skin.extra_description = env.text
            return modifyOk()

        if self.param == "价钱" or self.param == "价格":
            if not isFloat()(env.text):
                raise WaitForMoreInformationException(
                    self,
                    Message([at(env.sender), text("MSG_INPUT_PRICE_WRONG_FORMAT")]),
                )

            skin.price = float(env.text)
            return modifyOk()

        if len(images := env.message.include("image")) != 1:
            raise WaitForMoreInformationException(
                self, Message([at(env.sender), text("MSG_IMAGE_WRONG_FORMAT")])
            )

        image = images[0]

        fp = getSkinTarget(skin)
        await writeData(await download(image.data["url"]), fp)
        skin.image = fp
        return modifyOk()


@requireAdmin
@databaseIO()
@dataclass
class CatchModifySkin(Command):
    commandPattern: str = (
        f"^:: ?{KEYWORD_CHANGE} ?{KEYWORD_SKIN} ?(名字|名称|描述|图像|图片|价钱|价格)"
    )
    argsPattern: str = " (\\S+)$"

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message([at(env.sender), text("MSG_MODIFY_SKIN_WRONG_FORMAT")])

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        skin = await getSkinByName(env.session, result.group(4))

        if skin is None:
            return self.notExists(env, result.group(4))

        callback = CatchModifySkinCallback(cast(int, skin.data_id), result.group(3))
        raise WaitForMoreInformationException(
            callback, Message([at(env.sender), text("MSG_PLEASE_INPUT")])
        )


@requireAdmin
@dataclass
class CatchAdminDisplay(Command):
    commandPattern: str = f"^:: ?{KEYWORD_DISPLAY}"
    argsPattern: str = " (\\S+)( \\S+)?$"

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message([at(env.sender), text("MSG_DISPLAY_ADMIN_WRONG_FORMAT")])

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        award = await getAwardByName(env.session, result.group(2))

        if award is None:
            return self.notExists(env, result.group(2))

        imgUrl = award.img_path
        desc = award.description

        if result.group(3) is not None:
            skin = await getSkinByName(env.session, result.group(3)[1:])

            if skin is None or skin.award != award:
                return self.notExists(env, result.group(3)[1:])

            imgUrl = skin.image

            if len(skin.extra_description) > 0:
                desc = skin.extra_description

        return Message(
            [
                at(env.sender),
                text("MSG_ADMIN_DISPLAY"),
                await localImage(imgUrl),
                text(f"\n\n{desc}"),
            ]
        )


@requireAdmin
@databaseIO()
@dataclass
class CatchAdminObtainSkin(Command):
    commandPattern: str = f":: ?{KEYWORD_OBTAIN} ?{KEYWORD_SKIN}"
    argsPattern: str = " (\\S+)$"

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message([at(env.sender), text("MSG_MODIFY_SKIN_WRONG_FORMAT")])

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        skin = await getSkinByName(env.session, result.group(3))

        if skin is None:
            return self.notExists(env, result.group(3))

        await obtainSkin(env.session, await getSender(env), skin)

        return modifyOk()


@requireAdmin
@databaseIO()
@dataclass
class CatchAdminDeleteSkinOwnership(Command):
    commandPattern: str = f":: ?{KEYWORD_REMOVE_OBTAIN} ?{KEYWORD_SKIN}"
    argsPattern: str = " (\\S+)$"

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message([at(env.sender), text("MSG_MODIFY_SKIN_WRONG_FORMAT")])

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        skin = await getSkinByName(env.session, result.group(3))

        if skin is None:
            return self.notExists(env, result.group(3))

        await deleteSkinOwnership(env.session, await getSender(env), skin)
        return modifyOk()


@requireAdmin
@databaseIO()
@dataclass
class CatchResetEveryoneCacheCount(Command):
    commandPattern: str = f":: ?{KEYWORD_RESET} ?{KEYWORD_CACHE_COUNT}"
    argsPattern: str = "( (\\d+))?$"

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message([at(env.sender), text("MSG_RESET_CACHE_WRONG_FORMAT")])

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        if result.group(4) is None:
            await resetCacheCount(env.session, 1)
            return Message([at(env.sender), text("MSG_RESET_CACHE_OK")])

        count = int(result.group(4))
        if count < 1:
            return self.errorMessage(env)
        await resetCacheCount(env.session, count)


@requireAdmin
@databaseIO()
@dataclass
class CatchGiveMoney(Command):
    commandPattern: str = ":: ?给钱"
    argsPattern: str = " (\\d+) (-?\\d+)"

    def errorMessage(self, env: CheckEnvironment) -> Message | None:
        return Message([at(env.sender), text("MSG_GIVE_MONEY_WRONG_FORMAT")])

    async def handleCommand(self, env: CheckEnvironment, result: re.Match[str]):
        money = int(result.group(2))

        user = await getUser(env.session, int(result.group(1)))
        user.money += money

        return Message([at(env.sender), text("MSG_GIVE_MONEY_OK")])


@requireAdmin
@databaseIO()
@dataclass
class AddAltName(Command):
    commandPattern: str = (
        f"^:: ?{KEYWORD_CREATE}({KEYWORD_AWARDS}|{KEYWORD_LEVEL}|{KEYWORD_SKIN}) ?{KEYWORD_ALTNAME} (\\S+) (\\S+)"
    )
    argsPattern: str = ""

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        ty = result.group(2)
        name = result.group(7)
        alt = result.group(8)

        if re.match(KEYWORD_AWARDS, ty):
            award = await getAwardByName(env.session, name)
            if award is None:
                return self.notExists(env, name)

            if await createAwardAltName(env.session, award, alt):
                return Message([at(env.sender), text("MSG_ADD_ALTNAME_OK")])
            return Message([at(env.sender), text("MSG_ALTNAME_EXISTS")])

        if re.match(KEYWORD_LEVEL, ty):
            level = await getLevelByName(env.session, name)
            if level is None:
                return self.notExists(env, name)

            if await createLevelAltName(env.session, level, alt):
                return Message([at(env.sender), text("MSG_ADD_ALTNAME_OK")])
            return Message([at(env.sender), text("MSG_ALTNAME_EXISTS")])

        if re.match(KEYWORD_SKIN, ty):
            skin = await getSkinByName(env.session, name)
            if skin is None:
                return self.notExists(env, name)

            if await createSkinAltName(env.session, skin, alt):
                return Message([at(env.sender), text("MSG_ADD_ALTNAME_OK")])
            return Message([at(env.sender), text("MSG_ALTNAME_EXISTS")])

        return Message([at(env.sender), text("MSG_ADD_ALTNAME_WRONG_TYPE")])


@requireAdmin
@databaseIO()
@dataclass
class RemoveAltName(Command):
    commandPattern: str = (
        f"^:: ?{KEYWORD_REMOVE}({KEYWORD_AWARDS}|{KEYWORD_LEVEL}|{KEYWORD_SKIN}) ?{KEYWORD_ALTNAME} (\\S+)"
    )
    argsPattern: str = ""

    async def handleCommand(
        self, env: CheckEnvironment, result: re.Match[str]
    ) -> Message | None:
        ty = result.group(2)
        alt = result.group(7)

        if re.match(KEYWORD_AWARDS, ty):
            obj = await getAwardAltNameObject(env.session, alt)
        elif re.match(KEYWORD_LEVEL, ty):
            obj = await getLevelAltNameObject(env.session, alt)
        elif re.match(KEYWORD_SKIN, ty):
            obj = await getSkinAltNameObject(env.session, alt)
        else:
            obj = None

        if obj is None:
            return Message([at(env.sender), text("MSG_ALTNAME_NOT_EXISTS")])

        await deleteObj(env.session, obj)
        return Message([at(env.sender), text("MSG_REMOVE_ALTNAME_OK")])


@requireAdmin
@databaseIO()
@dataclass
class AddTags(Command):
    commandPattern: str = f"^:: ?{KEYWORD_CREATE}({KEYWORD_AWARDS}|{KEYWORD_LEVEL}|{KEYWORD_SKIN}){KEYWORD_TAG} (\\S+) (\\S+) (\\S+)"
    argsPattern: str = "$"

    async def handleCommand(self, env: CheckEnvironment, result: re.Match[str]) -> Message | None:
        ty = result.group(2)
        name = result.group(7)
        tag_name = result.group(8)
        tag_args = result.group(9)

        tag = await getTag(env.session, tag_name, tag_args)

        if re.match(KEYWORD_AWARDS, ty):
            award = await getAwardByName(env.session, name)
            if award is None:
                return self.notExists(env, name)
            
            await addAwardTag(env.session, award, tag)
            return Message([at(env.sender), text("MSG_ADD_TAG_OK")])

        if re.match(KEYWORD_LEVEL, ty):
            level = await getLevelByName(env.session, name)
            if level is None:
                return self.notExists(env, name)
            
            await addLevelTag(env.session, level, tag)
            return Message([at(env.sender), text("MSG_ADD_TAG_OK")])

        if re.match(KEYWORD_SKIN, ty):
            skin = await getSkinByName(env.session, name)
            if skin is None:
                return self.notExists(env, name)
            
            await addSkinTag(env.session, skin, tag)
            return Message([at(env.sender), text("MSG_ADD_TAG_OK")])
        
        return Message([at(env.sender), text("MSG_ADD_TAG_WRONG_TYPE")])


@requireAdmin
@databaseIO()
@dataclass
class RemoveTags(Command):
    commandPattern: str = f"^:: ?{KEYWORD_REMOVE}({KEYWORD_AWARDS}|{KEYWORD_LEVEL}|{KEYWORD_SKIN}){KEYWORD_TAG} (\\S+) (\\S+) (\\S+)"
    argsPattern: str = "$"

    async def handleCommand(self, env: CheckEnvironment, result: re.Match[str]) -> Message | None:
        ty = result.group(2)
        name = result.group(7)
        tag_name = result.group(8)
        tag_args = result.group(9)
        
        tag = await getTag(env.session, tag_name, tag_args)

        if re.match(KEYWORD_AWARDS, ty):
            award = await getAwardByName(env.session, name)
            if award is None:
                return self.notExists(env, name)
            
            await removeAwardTag(env.session, award, tag)
            return Message([at(env.sender), text("MSG_REMOVE_TAG_OK")])

        if re.match(KEYWORD_LEVEL, ty):
            level = await getLevelByName(env.session, name)
            if level is None:
                return self.notExists(env, name)
            
            await removeLevelTag(env.session, level, tag)
            return Message([at(env.sender), text("MSG_REMOVE_TAG_OK")])
        
        if re.match(KEYWORD_SKIN, ty):
            skin = await getSkinByName(env.session, name)
            if skin is None:
                return self.notExists(env, name)
            
            await removeSkinTag(env.session, skin, tag)
            return Message([at(env.sender), text("MSG_REMOVE_TAG_OK")])
        
        return Message([at(env.sender), text("MSG_REMOVE_TAG_WRONG_TYPE")])
