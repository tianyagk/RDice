import random
import re
from typing import Tuple, Optional


class DiceError(Exception):
    """自定义骰子异常"""

    pass


class DiceRoller:
    @staticmethod
    def roll(dice_expr: str) -> Tuple[int, str]:
        """
        处理标准骰子表达式 (如 3d6+2)
        返回: (最终结果, 过程描述)
        """
        try:
            # 匹配形如 2d6+1 的表达式
            match = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", dice_expr.lower())
            if not match:
                raise DiceError("无效的骰子表达式")

            count, sides, modifier = match.groups()
            count, sides = int(count), int(sides)
            modifier = int(modifier) if modifier else 0

            if count <= 0 or sides <= 0:
                raise DiceError("骰子数量和面数必须为正数")

            rolls = [random.randint(1, sides) for _ in range(count)]
            total = sum(rolls) + modifier

            process = f"{count}D{sides}={rolls}"
            if modifier > 0:
                process += f"+{modifier}"
            elif modifier < 0:
                process += f"{modifier}"

            return total, process
        except ValueError:
            raise DiceError("骰子表达式解析错误")

    @staticmethod
    def coc_check(skill_value: int) -> Tuple[bool, str, int]:
        """
        COC技能检定
        返回: (是否成功, 评级, 骰值)
        """
        roll = random.randint(1, 100)
        if roll == 1:
            return True, "大成功", roll
        if roll == 100:
            return False, "大失败", roll

        success = roll <= skill_value
        if success:
            if roll <= skill_value // 2:
                grade = "困难成功" if skill_value >= 50 else "成功"
            elif roll <= skill_value // 5:
                grade = "极难成功" if skill_value >= 50 else "成功"
            else:
                grade = "成功"
        else:
            grade = "失败"

        return success, grade, roll
