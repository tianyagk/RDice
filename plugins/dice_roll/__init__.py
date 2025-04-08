from nonebot.plugin import PluginMetadata

from .commands import *

__plugin_meta__ = PluginMetadata(
    name="COC骰子模拟器",
    description="克苏鲁的召唤(COC)跑团专用骰子插件",
    usage=[
        ".r 3d6    # 投掷3个6面骰",
        ".ra 侦查  # 进行侦查技能检定",
        ".sc 1/1d6  # 理智检定(成功扣1/失败扣1d6)",
        ".st 力量 50 # 设置临时属性值",
    ],
    type="application",
    homepage="https://your-bot-website.com",
    extra={"author": "YourName"},
)
