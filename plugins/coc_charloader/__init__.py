from nonebot.plugin import PluginMetadata

# from .commands import *

__plugin_meta__ = PluginMetadata(
    name="COC角色管理器",
    description="克苏鲁的召唤角色数据加载/保存系统",
    usage=[
        ".load 角色名    # 加载已有角色",
        ".save [角色名]  # 保存当前角色(可选指定名称)",
        ".chars         # 查看所有可用角色",
    ],
    type="application",
    extra={
        "author": "Aeoluze",
        "version": "0.1.0",
        "data_location": "./data/coc_chars/",
    },
)
