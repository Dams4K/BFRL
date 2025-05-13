import pyplayhd

from discord.ext import commands, tasks

from ddmc import *

class UpdateStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mcplayhd: pyplayhd.Client = bot.mcplayhd

        self.updates_data = self.bot.updates
        self.to_update = []

        self.fetch_update.start()

    def cog_unload(self):
        self.fetch_update.cancel()

    @tasks.loop(minutes=1)
    async def fetch_update(self):
        self.to_update = self.updates_data.get_to_update()
    
    @tasks.loop(seconds=6) # 6 modes, so 6 call to the api
    async def update(self):
        if self.to_update == []:
            return
        uuid = self.to_update.pop()

        builder_data = BuilderPlayerData(uuid)
        next_time = builder_data.update()

        self.updates_data.update_time(uuid, next_time)


    @fetch_update.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()
        self.update.start()

def setup(bot):
    bot.add_cog(UpdateStats(bot))
