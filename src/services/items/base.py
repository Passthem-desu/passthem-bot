from pydantic import BaseModel

from src.base.resources import Resource, static_res
from src.core.unit_of_work import UnitOfWork


class UseItemArgs(BaseModel):
    count: int = 1
    target_uid: int | None = None


class BaseItem(BaseModel):
    """
    物品的基类
    """

    name: str
    "物品的名字，同时会传入数据库作为物品的 ID"

    description: str
    "物品的描述"

    image: Resource = static_res("blank_placeholder.png")
    "物品的图片"

    item_sorting: float = 0.0
    """
    物品的排序顺序，会从小到大排序，小的在前，大的在后。
    如果你需要调整物品的排序，你可以更改这个字段，成随意的你认为的浮点值。
    """

    group: str
    """
    物品的物品组
    """

    async def can_be_used(self, uow: UnitOfWork, uid: int, args: UseItemArgs) -> bool:
        """
        能否使用这个物品，如果需要更改逻辑，请重载这个函数
        """
        return False

    async def use(self, uow: UnitOfWork, uid: int, args: UseItemArgs) -> None:
        """
        使用这个物品触发的逻辑，如果需要更改逻辑，请重载这个函数。
        在这里，你需要实现物品减少的逻辑，并告知用于你使用了这个物品的相关消息。

        在这里发送消息，你需要从 src.base.onebot.onebot_tools 中导入 tell 函数。
        """
        return None


class ItemInventoryDisplay(BaseModel):
    meta: BaseItem
    count: int = -1
    stats: int = -1


class ItemService:
    """
    物品服务
    """

    items: dict[str, BaseItem]

    def __init__(self) -> None:
        self.items = {}

    def register(self, item: BaseItem) -> None:
        assert (
            item.name not in self.items
        ), f"物品名 {item.name} 发生冲突了，请检查是否有重复注册"
        self.items[item.name] = item

    async def get_inventory_displays(
        self, uow: UnitOfWork, uid: int | None
    ) -> list[tuple[str, list[ItemInventoryDisplay]]]:
        """
        获得物品栏的展示清单，如果未提供 uid，则返回所有已经注册的物品。
        """

        _results: dict[str, list[ItemInventoryDisplay]] = {}

        if uid is not None:
            inventory = await uow.items.get_dict(uid)
            for key, (count, stats) in inventory.items():
                if key not in self.items:
                    continue
                item = self.items[key]
                _results.setdefault(item.group, [])
                _results[item.group].append(
                    ItemInventoryDisplay(
                        meta=item,
                        count=count,
                        stats=stats,
                    )
                )
        else:
            for item in self.items.values():
                _results.setdefault(item.group, [])
                _results[item.group].append(
                    ItemInventoryDisplay(
                        meta=item,
                    )
                )

        results = [(group, ls) for group, ls in _results.items()]
        results.sort(key=lambda result: result[0])
        return results


_global_service = ItemService()


def get_item_service() -> ItemService:
    """
    获得全局的物品管理服务
    """
    return _global_service


def register_item(item: BaseItem):
    """
    注册物品
    """
    get_item_service().register(item)
