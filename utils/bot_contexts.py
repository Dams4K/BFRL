from discord import ApplicationContext

from db import *

class BotApplicationContext(ApplicationContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dmember = None
        self.dguild = None
        if self.guild:
            self.dmember = Member.from_id(self.guild.id, self.author.id)
            self.dguild = Guild.from_id(self.guild.id)
