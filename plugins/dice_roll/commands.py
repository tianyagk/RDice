from nonebot.plugin import on_command, get_plugin_config
from nonebot.rule import to_me, Rule
from nonebot.params import CommandArg, ArgPlainText
from nonebot.matcher import Matcher
# from nonebot.adapters.console import MessageEvent, Message
from nonebot.adapters.onebot.v11 import MessageEvent, Message
# from nonebot.adapters.onebot.v11.helpers import extract_numbers

from .config import Config
from .handler import *

plugin_config = get_plugin_config(Config)


async def is_enable() -> bool:
    """插件是否启用"""
    return plugin_config.plugin_enabled


# 基础骰子命令
dice_cmd = on_command(
    "r",
    aliases={"roll", "掷骰"},
    priority=5,
    rule=Rule(is_enable),
    block=True,
)


@dice_cmd.handle()
async def handle_dice(event: MessageEvent, arg: Message = CommandArg()):
    expr = arg.extract_plain_text().strip() or "1d100"
    try:
        result, process = DiceRoller.roll(expr)
        await dice_cmd.finish(f"🎲 投掷 {process} = {result}")
    except DiceError as e:
        await dice_cmd.finish(f"骰子错误：{e}")


# COC技能检定
check_cmd = on_command(
    "ra", aliases={"检定"}, priority=5, rule=Rule(is_enable), block=True
)


@check_cmd.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    await skill_check(event, check_cmd, arg.extract_plain_text())


async def skill_check(
    event: MessageEvent, matcher: Matcher, skill_name: str = ArgPlainText()
):
    """处理 .ra 技能名 指令"""
    # 这里应该连接角色卡系统获取技能值
    # 示例中使用固定值演示
    if "侦查" in skill_name:
        skill_value = 60
    elif "图书馆" in skill_name:
        skill_value = 70
    else:
        await matcher.finish(f"找不到技能：{skill_name}")

    success, grade, roll = DiceRoller.coc_check(skill_value)

    await matcher.finish(f"[{grade}] {skill_name}检定\n" f"D100={roll}/{skill_value}")


# 理智检定
san_cmd = on_command(
    "sc",
    aliases={"san", "理智检定"},
    priority=5,
    rule=Rule(is_enable),
    block=True,
)


@san_cmd.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split(" ")
    if len(args) != 2:
        await san_cmd.finish("格式错误，正确格式：.sc 成功扣除/失败扣除 当前理智 (如 .sc 1/1d6 60)")

    try:
        # 模拟当前SAN值
        current_san = int(args[-1]) or 100
        success, _, roll = DiceRoller.coc_check(current_san)

        if success:
            loss = args[0].split("/")[0]
            result = f"理智检定通过，SAN值减少 {loss}"
        else:
            loss = DiceRoller.roll(args[0].split("/")[1])[0]
            result = f"理智检定失败！SAN值减少 {loss}"

        new_san = max(0, current_san - int(loss))
        await san_cmd.finish(
            f"SAN检定：D100={roll}/{current_san}\n" f"{result} (当前SAN：{new_san})"
        )
    except DiceError as e:
        await san_cmd.finish(f"理智检定错误：{e}")
