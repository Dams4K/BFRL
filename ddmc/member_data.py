from ddm import *
from utils.references import References

from mcapi.player import get_name

class MemberData(Saveable):
    __slots__ = ("_bot", "_guild_id", "_member_id", "uuid")

    def __init__(self, bot, guild_id, member_id):
        self._bot = bot
        self._guild_id = guild_id
        self._member_id = member_id

        self.uuid = ""

        super().__init__(References.guild_folder(self._guild_id, f"members/{self._member_id}.json"))

    @Saveable.update()
    def set_uuid(self, value: str):
        self.uuid = value
        self._bot.updates.update_time(self.uuid, 0)
    
    @property
    def player_name(self) -> str:
        return get_name(self.uuid)
