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
    def remove(self, member_id: int) -> bool:
        try:
            self.listed.remove(member_id)
            return True
        except ValueError:
            return False
    
    def remove_uuid(self, uuid: str) -> bool:
        try:
            #TODO: make this work
            # return self.remove(self.listed.index(uuid))
            return False
        except ValueError:
            return False