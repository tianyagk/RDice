from nonebot.plugin import on_command
from nonebot.params import CommandArg, ArgPlainText, EventPlainText
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.matcher import Matcher

from .handler import storage
from .model import Investigator

load_cmd = on_command("load", aliases={"加载角色"}, priority=5, block=True)
save_cmd = on_command("save", aliases={"保存角色"}, priority=5, block=True)
chars_cmd = on_command("chars", aliases={"角色列表"}, priority=5, block=True)


@load_cmd.handle()
async def load_character(
    event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()
):
    char_name = arg.extract_plain_text().strip()
    if not char_name:
        await matcher.send("请指定角色名称，例如：.load 张三")

    user_id = event.get_user_id()

    try:
        char = await storage.load_character(user_id, char_name)
        await matcher.send(
            f"角色加载成功！\n"
            f"姓名：{char.name}\n"
            f"职业：{char.occupation}\n"
            f"HP: {char.HP} MP: {char.MP} SAN: {char.SAN}"
        )
    except FileNotFoundError:
        await matcher.finish(f"角色 {char_name} 不存在")
    except Exception as e:
        await matcher.finish(f"加载失败：{str(e)}")


@save_cmd.handle()
async def save_character(
    event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()
):
    user_id = event.get_user_id()
    new_name = arg.extract_plain_text().strip() or None

    try:
        if not await storage.get_character(user_id):
            await matcher.finish("你还没有加载任何角色")

        saved_name = await storage.save_character(user_id, new_name)
        await matcher.send(f"角色已保存为：{saved_name}")
    except Exception as e:
        await matcher.finish(f"保存失败：{str(e)}")


@chars_cmd.handle()
async def list_characters(matcher: Matcher):
    try:
        chars = await storage.list_available()
        if not chars:
            await matcher.finish("没有可用的角色数据")

        msg = "可用角色列表：\n" + "\n".join(
            f"{i+1}. {name}" for i, name in enumerate(chars)
        )
        await matcher.send(msg)
    except Exception as e:
        await matcher.finish(f"获取角色列表失败：{str(e)}")
