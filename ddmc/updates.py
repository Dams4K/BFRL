import os
import time

from ddm import *
from utils.references import References
from pyplayhd import *

from .member_data import MemberData

class Updates(Saveable):
    __slots__ = ("_bot", "next_updates",)

    def __init__(self, bot):
        self._bot = bot

        self.next_updates = {}
        
        super().__init__(os.path.join(References.FOLDER_DATAS, "updates.json"))
    
    def get_to_update(self):
        timestamp = int(time.time())
        return [uuid for uuid, time in self.next_updates.items() if time < timestamp]

    @Saveable.update
    def load_known(self):
        dirs = os.listdir(References.guilds_folder())
        for gf in dirs:
            guild_id = int(gf)
            
            mf = os.path.join(References.guilds_folder(), gf, "members")
            members = os.listdir(mf)
            
            for member_str in members:
                smember_id: str = member_str.split(".")[0]
                if not smember_id.isdecimal():
                    continue
                
                member_id = int(smember_id)
                member_data = MemberData(self._bot, guild_id, member_id)

                self.next_updates.setdefault(member_data.uuid, 0)
    
    @Saveable.update
    def update_time(self, uuid, time):
        self.next_updates[uuid] = time