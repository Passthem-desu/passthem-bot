class KagamiCoreException(Exception):
    """小镜 Bot 抓小哥游戏的错误类型的基类"""

    @property
    def message(self) -> str:
        return "通常来说，你应该看不到这条错误信息。如果你看到了，请联系开发组修复。"
    
    def __str__(self) -> str:
        return self.message


class ObjectNotFoundException(KagamiCoreException):
    """当找不到某个对象时抛出此异常"""

    def __init__(self, obj_type: str, obj_name: str) -> None:
        super().__init__()
        self.obj_type = obj_type
        self.obj_name = obj_name

    @property
    def message(self) -> str:
        return f"我好像不知道你说的 {self.obj_name} 是什么 {self.obj_type}"


class RecipeMissingException(KagamiCoreException):
    """在更新配方信息时，因为原配方不存在，所以没办法更新信息"""

    @property
    def message(self) -> str:
        return "原配方不存在，两个参数都要填写"


class ObjectAlreadyExistsException(KagamiCoreException):
    """当某个对象已经存在时抛出此异常"""

    def __init__(self, obj_name: str | None) -> None:
        super().__init__()
        self.obj_name = obj_name

    @property
    def message(self) -> str:
        if self.obj_name:
            return f"你所说的 {self.obj_name} 已经存在了"
        return "相应的对象已经存在"


class LackException(KagamiCoreException):
    """用户缺少什么的时候的报错信息"""

    def __init__(self, obj_type: str, required: str | float | int, current: str | float | int) -> None:
        super().__init__()
        self.obj_type = obj_type
        self.required = required
        self.current = current

    @property
    def message(self) -> str:
        return (
            f"啊呀！你的 {self.obj_type} 不够了，"
            f"你需要 {self.required} {self.obj_type}，"
            f"你只有 {self.current} {self.obj_type}"
        )
