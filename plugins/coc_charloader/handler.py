from typing import Dict, Optional
from .model import CharacterManager, Investigator


class UserCharacterStorage:
    """用户角色内存存储"""

    def __init__(self):
        self.user_char_map: Dict[str, Investigator] = {}
        self.manager = CharacterManager()

    async def load_character(self, user_id: str, char_name: str) -> Investigator:
        """为用户加载角色"""
        char = self.manager.load_from_file(char_name)
        char.player_id = user_id  # 确保绑定当前用户
        self.user_char_map[user_id] = char
        return char

    async def save_character(self, user_id: str, new_name: str = None) -> str:
        """保存用户当前角色"""
        if user_id not in self.user_char_map:
            raise ValueError("用户没有加载任何角色")

        char = self.user_char_map[user_id]
        saved_name = self.manager.save_to_file(char, new_name)
        return saved_name

    async def get_character(self, user_id: str) -> Optional[Investigator]:
        """获取用户当前角色"""
        return self.user_char_map.get(user_id)

    async def list_available(self) -> list:
        """获取所有可用角色"""
        return self.manager.list_characters()


storage = UserCharacterStorage()
