from nonebot.plugin import on_command, get_plugin_config
from nonebot.rule import to_me, Rule
from nonebot.params import CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent, Message

from nonebot import require

require("coc_charloader")
from plugins.coc_charloader.handler import storage  # type: ignore

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
async def handle_check(
    event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()
):
    """处理 .ra 技能名 指令"""
    user_id = event.get_user_id()
    skill_name = arg.extract_plain_text().strip()

    if not skill_name:
        await check_cmd.finish("请指定检定技能，例如: .ra 侦查")

    # 获取用户当前角色
    investigator = await storage.get_character(user_id)

    if not investigator:
        check_cmd.finish("角色未载入，无法基于角色数据进行检定")
    else:
        # 有角色数据，从角色卡获取技能值
        skill_value = investigator.skills.get(skill_name, 0)
        char_info = f"角色:{investigator.name}({investigator.occupation})"

    # 进行检定
    success, grade, roll = DiceRoller.coc_check(skill_value)

    # 构建结果消息
    result = (
        f"{char_info}\n" f"[{grade}] {skill_name}检定\n" f"D100={roll}/{skill_value}"
    )

    # 特殊结果处理 - 大成功/大失败
    if grade == "大成功":
        result += "\n✨ 真是惊人的好运！"
    elif grade == "大失败":
        result += "\n💥 哦不，情况变得更糟了！"

    await check_cmd.finish(result)


# 理智检定
san_check_cmd = on_command(
    "sc",
    aliases={"san", "理智检定"},
    priority=5,
    rule=Rule(is_enable),
    block=True,
)


@san_check_cmd.handle()
async def handle_san_check(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text()
    if "/" not in args:
        await san_check_cmd.finish(
            "格式错误，正确格式：.sc 成功扣除/失败扣除 (如 .sc 1/1d6)"
        )

    user_id = event.get_user_id()
    # 获取用户当前角色
    investigator = await storage.get_character(user_id)

    if not investigator:
        check_cmd.finish("角色未载入，无法基于角色数据进行检定")

    try:
        # 模拟当前SAN值
        current_san = investigator.current_san
        success, _, roll = DiceRoller.coc_check(current_san)

        if success:
            loss = args.split("/")[0]
            if "d" in loss:
                loss = DiceRoller.roll(loss)[0]
            result = f"理智检定通过，SAN值减少 {loss}"
        else:
            loss = DiceRoller.roll(args.split("/")[1])[0]
            result = f"理智检定失败！SAN值减少 {loss}"

        new_san = max(0, current_san - int(loss))
        investigator.current_san = new_san
        await san_check_cmd.finish(
            f"SAN检定：D100={roll}/{current_san}\n" f"{result} (当前SAN：{new_san})"
        )
    except DiceError as e:
        await san_check_cmd.finish(f"理智检定错误：{e}")
