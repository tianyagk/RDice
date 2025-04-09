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
    STR: int = Field(50, ge=15, le=90)
    CON: int = Field(50, ge=15, le=90)
    DEX: int = Field(50, ge=15, le=90)
    APP: int = Field(50, ge=15, le=90)
    POW: int = Field(50, ge=15, le=90)
    SIZ: int = Field(50, ge=15, le=90)
    INT: int = Field(50, ge=15, le=90)
    EDU: int = Field(50, ge=15, le=90)

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

    # 技能系统
    skills: Dict[str, int] = Field(
        default_factory=lambda: {"侦查": 25, "图书馆": 20, "闪避": 10},
        description="技能名称与数值的映射",
    )

    # 背景故事
    background: Optional[str] = None
    personal_desc: Optional[str] = None

    # 模型验证
    @validator("skills")
    def validate_skills(cls, v):
        for skill, value in v.items():
            if value < 0 or value > 100:
                raise ValueError(f"技能 {skill} 值超出范围(0-100)")
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
