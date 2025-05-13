from ddm import *
from utils.references import References

class MemberData(Saveable):
    __slots__ = ("_guild_id", "update_channel", "whitelist_channel")

    def __init__(self, guild_id):
        self._guild_id = guild_id
        
        self.update_channel: int = -1
        self.whitelist_channel: int = -1

        super().__init__(References.guild_folder(self._guild_id, "config.json"))


    @Saveable.update
    def save_attr(self, name, value):
        super().__setattr__(name, value)

    def __setattr__(self, name, value):
        if name in self.get_saveable_attrs():
            return self.save_attr(name, value)
        return super().__setattr__(name, value)
