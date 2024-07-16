from dataclasses import dataclass

from pydantic import BaseModel

from src.base.exceptions import ObjectNotFoundException


@dataclass
class Level(BaseModel):
    """
    抓小哥中小哥的等级
    """

    __pydantic_fields_set__ = {
        "lid",
        "search_names",
        "display_name",
        "weight",
        "color",
        "awarding",
        "sorting_priority",
    }

    lid: int = -1
    search_names: list[str]
    display_name: str
    weight: float
    color: str
    awarding: int
    sorting_priority: int = 0


class LevelRepository:
    """
    管理小哥等级数据的数据管理器，在生产环境中应保持只读
    """

    _LEVELS: dict[int, Level] = {}

    def register(
        self,
        id: int,
        search_names: list[str],
        display_name: str,
        weight: float,
        color: str,
        awarding: int,
        sorting_priority: int = 0,
    ):
        self._LEVELS[id] = Level(
            lid=id,
            search_names=search_names,
            display_name=display_name,
            weight=weight,
            color=color,
            awarding=awarding,
            sorting_priority=sorting_priority,
        )

    def clear(self):
        self._LEVELS = {}

    def register_basics(self):
        self.register(1, ["一星", "一", "1"], "★", 65, "#C6C1BF", 2)
        self.register(2, ["二星", "二", "2"], "★★", 24.5, "#C0E8AE", 5)
        self.register(3, ["三星", "三", "3"], "★★★", 8, "#BDDAF5", 10)
        self.register(4, ["四星", "四", "4"], "★★★★", 2.0, "#D4BCE3", 40)
        self.register(5, ["五星", "五", "5"], "★★★★★", 0.5, "#F1DD95", 120)
        self.register(0, ["零星", "零", "0"], "☆", 0, "#9e9d95", 0, -1)

    @property
    def levels(self):
        return self._LEVELS

    @property
    def sorted(self):
        return sorted(
            self.levels.values(), key=lambda l: (-l.sorting_priority, l.weight)
        )

    @property
    def sorted_index(self):
        return {v.lid: i for i, v in enumerate(self.sorted)}

    @property
    def name_index(self):
        return {
            **{level.display_name: level for level in self.sorted},
            **{name: level for level in self.sorted for name in level.search_names},
        }

    def get_by_name(self, name: str):
        return self.name_index.get(name)
    
    def get_by_name_strong(self, name: str):
        r = self.name_index.get(name)
        if r is None:
            raise ObjectNotFoundException("等级", name)
        return r

    def get_by_id(self, id: int):
        return self.levels[id]


# 目前暂时以单例模式运作
level_repo = LevelRepository()
"小哥等级的单例"

level_repo.register_basics()


__all__ = ["Level", "LevelRepository", "level_repo"]
