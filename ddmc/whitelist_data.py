from ddm import *
from utils.references import References

class WhitelistData(Saveable):
    __slots__ = ("_guild_id", "listed")

    def __init__(self, guild_id):
        self._guild_id = guild_id
        
        self.listed = []

        super().__init__(References.guild_folder(self._guild_id, f"whitelist.json"))
    
    @Saveable.update()
    def add(self, member_id: int):
        self.listed.append(member_id)

    @Saveable.update()
    def remove(self, member_id: int):
        self.listed.remove(member_id)