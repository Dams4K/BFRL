from ddm import *
from utils.references import References

class MemberData(Saveable):
    __slots__ = ("_guild_id", "_member_id", "uuid")

    def __init__(self, guild_id, member_id):
        self._guild_id = guild_id
        self._member_id = member_id

        self.uuid = ""

        super().__init__(References.guild_folder(self._guild_id, f"members/{self._member_id}.json"))

    @Saveable.update()
    def set_uuid(self, value: str):
        self.uuid = value
