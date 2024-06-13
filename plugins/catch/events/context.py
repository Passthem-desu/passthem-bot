from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast

from nonebot.adapters.console.event import MessageEvent as _ConsoleEvent
from nonebot.adapters.console.bot import Bot as _ConsoleBot

from nonebot.adapters.onebot.v11 import GroupMessageEvent as _OneBotGroupMessageEvent
from nonebot.adapters.onebot.v11 import PrivateMessageEvent as _OneBotPrivateMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as _OneBotMessageEvent
from nonebot.adapters.onebot.v11.bot import Bot as _OnebotBot

from nonebot_plugin_alconna.uniseg.message import UniMessage
from nonebot_plugin_alconna import Segment
from nonebot.adapters import Event, Bot

from arclet.alconna.typing import TDC


TE = TypeVar("TE", bound=Event)
TB = TypeVar("TB", bound=Bot)
TS = TypeVar("TS", bound=Segment)


class Context(Generic[TE, TDC]):
    event: TE

    def getEvent(self) -> TE:
        return self.event
    
    def getMessage(self) -> TDC:
        return cast(TDC, self.event.get_message())
    
    def getText(self) -> str:
        return self.event.get_message().extract_plain_text()


@dataclass
class UniContext(Generic[TE, TB, TS], Context[TE, UniMessage[TS]]):
    event: TE
    bot: TB

    async def send(self, message: UniMessage[Any]) -> None:
        await message.send(
            target=self.event,
            bot=self.bot,
        )


class OnebotGroupMessageContext(UniContext[_OneBotGroupMessageEvent, _OnebotBot, TS]):
    pass


class OnebotPrivateMessageContext(UniContext[_OneBotPrivateMessageEvent, _OnebotBot, TS]):
    pass


class OnebotMessageContext(UniContext[_OneBotMessageEvent, _OnebotBot, TS]):
    def getSenderId(self):
        return self.event.sender.user_id


class ConsoleMessageContext(UniContext[_ConsoleEvent, _ConsoleBot, TS]):
    def getSenderId(self):
        return None


PublicContext = OnebotMessageContext[TS] | ConsoleMessageContext[TS]