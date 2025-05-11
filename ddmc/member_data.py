from ddm import *
from enum import member

class MemberData(Saveable):
    __slots__ = ("_guild_id", "_member_id", "uuid")

    def __init__(self, member_id, guild_id):
        self._member_id = member_id
        self._guild_id = guild_id

        self.uuid = ""

    @Saveable.update()
    def set_uuid(self, value: str):
        self.uuid = value
