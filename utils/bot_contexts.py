from discord import ApplicationContext

from ddmc import *

class BotApplicationContext(ApplicationContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.member_data = None
        self.whitelist_data = None
        self.guild_config = None
        if self.guild:
            self.member_data = MemberData(self.bot, self.guild.id, self.user.id if hasattr(self, "user") else self.author.id)
            self.whitelist_data = WhitelistData(self.guild.id)
            self.guild_config = GuildConfig(self.bot, self.guild.id)
