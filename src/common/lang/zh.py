from packaging.version import Version


class About:
    update: dict[str, list[str]] = {
        "0.2.0": [
            "将数据使用数据库储存",
            "修复间隔为 0 时报错的问题",
        ],
        "0.2.1": [
            "修复了一些界面文字没有中心对齐的问题",
            "修复了抓小哥时没有字体颜色的问题",
        ],
        "0.3.0": [
            "正式添加皮肤系统",
            "限制了管理员指令只能在一些群执行",
            "修复了新玩家的周期被设置为 3600 的问题",
            "重新架构了关于图片生成的代码",
        ],
        "0.4.0": [
            "添加了商店系统",
        ],
        "0.4.1": [
            "将版本更新信息倒序而非正序显示",
            "调整了库存的显示顺序",
            "新抓到小哥能够获得奖励了",
            "来・了（数据恢复）",
        ],
        "0.4.2": [
            "热更新：修复了新用户有关的各种小问题",
        ],
        "0.4.3": [
            "修复了无法应用多个皮肤的问题",
            "调整了图片编码器以加快图片的生成速度",
        ],
        "0.4.4": [
            "调整了抓小哥进度中等级显示的顺序",
            "修复了可以靠刷屏多次抓小哥的 BUG",
            "还有一点，等你抽到了百变小哥就知道了～",
        ],
        "0.4.5": [
            "修复了抓小哥时没有显示新小哥的问题",
            "修复了抓小哥展示页面中描述意外断行的问题",
            "删去了一些判断使得文字的渲染速度能够加快",
        ],
        "0.5.0": [
            "尝试修复了抓小哥时出现的数据库冲突问题",
            "更新了一个跟给小哥有关的特性",
        ],
        "0.5.1": [
            "修复了金钱数量不会增加的问题",
            "修复了没有回复人的问题",
        ],
        "0.5.2": [
            "修复了切换皮肤没有响应的问题",
            "大幅度优化了抓小哥的速度",
        ],
        "0.5.3": [
            "修复了和给小哥有关的一个特性",
            "修复了抓小哥界面中皮肤没有正常展示的 Bug",
            "优化了部分指令",
        ],
        "0.5.4": [
            "修复了一处数字显示的问题",
            "修复了有些地方金钱没有正常改变的问题",
        ],
        "0.5.5": [
            "修复了一些和皮肤有关的问题",
            "给",
        ],
        "0.5.6": [
            "修复了mysp不显示单位的问题",
            "删除了对给的回应",
            "添加了喜报",
            "添加了复读镜，现在你可以操作小镜去抓 wum 了",
        ],
        "0.5.7": [
            "修复了切换皮肤命令",
            "修复了喜报指令",
        ],
        "0.5.8": [
            "现在呼叫小镜，可以加 Emoji 表情和 QQ 表情了",
            "新增了皮肤收集进度指令，看看你收集了多少皮肤",
            "AlphaQX: 调整了「复读镜」指令，现在的回应会更加人性化了",
            "MrChenBeta: 新增小镜jrrp指令，快来测测你的人品吧",
        ],
        "0.5.9": [
            "优化了小镜商店页面",
            "AlphaQX: 修复复读镜",
            "耶",
        ],
        "0.5.10": [
            "耶（已修复）",
            "修复了小镜商店有关的问题",
            "修正了「小镜！！！」时的提示词",
        ],
        "0.5.11": [
            "修复了小镜商店中买皮肤不会扣钱的问题",
            "榆木华: 更改了喜报的格式",
            "榆木华: 抓小哥进度添加标题、小哥数量",
            "榆木华: 微调抓进度界面，新增进度百分比计算与显示",
        ],
        "0.5.12": [
            "修复小镜商店的 Bug",
            "从本次更新之后，喜报的信息能够持久化保存了",
            "榆木华: 库存界面添加标题",
            "榆木华: 给抓小哥界面加了标题",
        ],
        "0.5.13": [
            "在多个地方显示群昵称而不是 QQ 名称",
            "修复了一些文字显示的问题，现在支持显示 Emoji 表情了",
            "记得「签到」",
            "榆木华：在抓进度界面增加了筛选等级功能，例如 zhuajd -l 5 就可以筛选查看五级的小哥进度",
            "榆木华：修复了小票二维码错位的问题",
        ],
        "0.5.13.1": [
            "试图修正了 zhuajd 过程中可能出现的 max() arg 为空的问题",
        ],
        "0.5.14": [
            "榆木华：调整了全部小哥界面和抓小哥界面的排版等",
            "榆木华：优化签到和jrrp指令，优化帮助信息",
            "榆木华：商店价格加阴影，以防难以辨认",
        ],
        "0.5.15": [
            "修复小镜 bot 会无故扣钱的问题",
            "榆木华：在今日人品消息中增加今日小哥",
            "榆木华：在皮肤进度界面添加标题",
        ],
        "0.5.16": [
            "榆木华：将帮助信息和更新信息改为图片生成，优化了界面",
        ],
        "0.6.0": [
            "上线合成系统。",
        ],
        "0.6.1": [
            "修正合成系统并回档。",
        ],
        "0.6.2": [
            "晚安……",
            "榆木华：调整了合成的相关算法",
            "榆木华：为合成添加了界面！",
            "榆木华：修复了库存为 0 时仍然显示在库存中的问题",
        ],
        "0.6.3": [
            "“晚安”指令改为“小镜晚安”，添加了对半个小时的支持",
            "Dleshers沣：喜报中增加了新抓小哥的提示",
        ],
        "0.6.4": [
            "是",
            "榆木华：更改了一些消息的文本",
        ],
        "0.7.0": [
            "调整了随机数生成器",
            "榆木华：调整了商店的界面",
            "榆木华：降低了合成的难度",
        ],
        "0.7.1": [
            "修复了一些指令无法正常使用的问题",
            "修复了新玩家无法正常创建帐号的问题",
        ],
        "0.7.2": [
            "owo",
            "修复了一些界面中可能出现的字体缺失问题",
            "这次很多更新是在底层进行的，所以还有可能出现一些 bug……",
            "距离公测已经不远了，在不久之后，会清空内测阶段的存档，感谢大家一直以来的支持，没有大家，抓小哥不会走到今天！",
        ],
        "0.8.0": [
            "引入成就系统（测试中）",
            "修复了重构以后和之前版本不同的一些表现",
        ],
        "0.8.1": [
            "修复了一个界面问题",
        ],
        "0.8.2": [
            "修复了一个界面问题",
            "修复「欧皇附体」成就判定错误",
            "调整了合成小哥的随机数生成机制",
            "下线了复读镜指令",
        ],
        "0.8.4": [
            "榆木华：把今日人品合入签到，并暂时取消显示今日小哥",
            "榆木华：优化合成算法",
        ],
        "0.8.5": [
            "修复了输入单撇号会导致报错的问题",
            "叫小镜的时候不会响应粽子表情",
        ],
        "0.8.6": [
            "是小哥现在也会给钱了",
            "调整了一些发送消息的时机",
            "移除了开头的跳舞，准备试验现在能不能让 bot 更加稳定",
        ],
        "0.9.0": [
            "优化了合成的界面",
            "调整了一些消息的文字",
            "为 kz 指令添加了大写的匹配",
            "去除了一个特性",
            "调大了小镜商店的字号",
        ],
        "0.9.1": [
            "优化了合成的界面",
            "调整了一些消息的文字",
            "为 kz 指令添加了大写的匹配",
            "去除了一个特性",
            "调大了小镜商店的字号",
        ],
        "0.10.0": [
            "架构了一个新的底层机制，在界面完成后，将会与大家见面，请大家期待",
            "去除了一个特性",
            "修复了一处字体问题",
        ],
        "0.10.1": [
            "修复了小镜不回应某些人的问题",
        ],
        "0.10.2": [
            "谁出货了？给他丢粑粑小哥吧！",
            "更改了小镜晚安的逻辑，晚安需谨慎哦！真的！！！一定要注意！！！！",
            "榆木华：更新了研究员华的对话",
        ],
        "0.10.3": [
            "小帕：调整了百变小哥的合成",
            "玛对：调整成就的显示方式，使其更不让人误解",
            "坏枪：调整了丢粑粑的相关判定",
        ],
        "1.0.0": [
            "猎场功能上线",
            "实现了新的界面渲染方式，这个方案现在进入了测试阶段",
        ],
        "1.0.1": [
            "修复了已知的问题（微信语）",
        ],
        "1.0.2": [
            "修复了不显示用户名的问题，此时将替换为显示 QQ 号",
            "调整了一些界面",
        ],
        "1.0.3": [
            "修复了一些用户只能显示 QQ 号的问题",
            "在一些界面显示了 QQ 头像",
            "调整了一些指令",
        ]
    }


class La:
    about = About()


la = La()


def get_latest_version() -> str:
    return sorted(la.about.update.keys(), reverse=True, key=Version)[0]


def get_latest_versions(count: int = 3) -> list[str]:
    return sorted(la.about.update.keys(), reverse=True, key=Version)[:count]


__all__ = ["la", "get_latest_version", "get_latest_versions"]
