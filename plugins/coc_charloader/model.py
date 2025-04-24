from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, List
from pathlib import Path
import json


class Investigator(BaseModel):
    """COC调查员完整数据模型"""

    # 基础信息
    player_id: str = Field(..., description="绑定的玩家ID")
    name: str = Field("无名调查员", max_length=30)
    age: int = Field(20, ge=15, le=90)
    occupation: str = Field("无业", description="职业")

    # 核心属性
    STR: int = Field(50, ge=1, le=99, description="力量")
    CON: int = Field(50, ge=1, le=99, description="体质")
    DEX: int = Field(50, ge=1, le=99, description="敏捷")
    APP: int = Field(50, ge=1, le=99, description="外貌")
    POW: int = Field(50, ge=1, le=99, description="意志")
    SIZ: int = Field(50, ge=1, le=99, description="体格")
    INT: int = Field(50, ge=1, le=99, description="智力")
    EDU: int = Field(50, ge=1, le=99, description="教育")
    
    # 额外属性
    LUCK: int = Field(50, ge=1, le=99, description="幸运")
    MOV: int = Field(8, ge=1, le=99, description="移动")
    CREDIT_RATING: int = Field(0, ge=0, le=99, description="信用评级")
    
    # 当前状态
    current_hp: int = Field(0, ge=0)
    current_mp: int = Field(0, ge=0)
    current_san: int = Field(0, ge=0)
    current_luck: int = Field(0, ge=0)

    # 衍生属性
    @property
    def HP(self) -> int:
        return (self.CON + self.SIZ) // 10

    @property
    def MP(self) -> int:
        return self.POW // 5

    @property
    def SAN(self) -> int:
        return self.POW

    @property
    def BUILD(self) -> int:
        """体格构建值"""
        if self.STR + self.SIZ < 65:
            return -2
        elif self.STR + self.SIZ < 85:
            return -1
        elif self.STR + self.SIZ < 125:
            return 0
        elif self.STR + self.SIZ < 165:
            return 1
        else:
            return 2

    @property
    def DB(self) -> str:
        """伤害奖励"""
        build = self.BUILD
        if build == -2:
            return "-2"
        elif build == -1:
            return "-1"
        elif build == 0:
            return "+0"
        elif build == 1:
            return "+1d4"
        else:
            return "+1d6"

    # 技能系统
    skills: Dict[str, int] = Field(
        default_factory=dict,
        description="技能名称与数值的映射",
    )
    
    combat_skills: Dict[str, int] = Field(
        default_factory=dict,
        description="战斗技能名称与数值的映射",
    )
    
    language_skills: Dict[str, int] = Field(
        default_factory=dict,
        description="语言技能名称与数值的映射",
    )

    # 背景故事
    background: Optional[str] = None
    personal_desc: Optional[str] = None
    belongings: Optional[str] = None  # 随身物品
    weapons: Optional[str] = None    # 武器信息
    backstory: Optional[str] = None  # 背景故事详情

    # 模型验证
    @validator("skills", "combat_skills", "language_skills")
    def validate_skills(cls, v):
        for skill, value in v.items():
            if value < 0 or value > 100:
                raise ValueError(f"技能 {skill} 值超出范围(0-100)")
        return v
    
    @validator("current_hp", pre=True, always=True)
    def set_hp_default(cls, v, values):
        if v == 0 and "CON" in values and "SIZ" in values:
            return (values["CON"] + values["SIZ"]) // 10
        return v
    
    @validator("current_mp", pre=True, always=True)
    def set_mp_default(cls, v, values):
        if v == 0 and "POW" in values:
            return values["POW"] // 5
        return v
    
    @validator("current_san", pre=True, always=True)
    def set_san_default(cls, v, values):
        if v == 0 and "POW" in values:
            return values["POW"]
        return v
    
    @validator("current_luck", pre=True, always=True)
    def set_luck_default(cls, v, values):
        if v == 0 and "LUCK" in values:
            return values["LUCK"]
        return v


class CharacterManager:
    """角色数据管理器"""

    def __init__(self, data_dir: str = "./data/coc_chars"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_path(self, char_name: str) -> Path:
        """获取角色文件路径"""
        return self.data_dir / f"{char_name}.json"

    def load_from_file(self, char_name: str) -> Investigator:
        """从JSON文件加载角色"""
        path = self.get_path(char_name)
        if not path.exists():
            raise FileNotFoundError(f"角色 {char_name} 不存在")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Investigator(**data)

    def save_to_file(
        self, investigator: Investigator, name_override: str = None
    ) -> str:
        """保存角色到JSON文件"""
        save_name = name_override or investigator.name
        path = self.get_path(save_name)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(investigator.dict(), f, ensure_ascii=False, indent=2)

        return save_name

    def list_characters(self) -> List[str]:
        """列出所有可用角色"""
        return sorted([f.stem for f in self.data_dir.glob("*.json") if f.is_file()])
