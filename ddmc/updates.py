import time

from ddm import *
from utils.references import References
from pyplayhd import *

class Updates(Saveable):
    __slots__ = ("_guild_id", "next_update")

    def __init__(self, guild_id):
        self._guild_id = guild_id

        self.next_updates = []
        
        super().__init__(References.guild_folder(self._guild_id, f"updates.json"))
    
    def update(self):
        players = self.get_to_update()

    def get_to_update(self):
        timestamp = int(time.time())
        return [uuid for uuid, time in self.next_update.items() if time < timestamp]