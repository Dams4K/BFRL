from discord.ext import commands, tasks

import pyplayhd

class UpdateStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mcplayhd: pyplayhd.Client = bot.mcplayhd

        self.update.start()

    def cog_unload(self):
        self.update.cancel()

    @tasks.loop(minutes=1)
    async def update(self):
        # print(self.mcplayhd.fastbuilder.modes)
        pass

    @update.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(UpdateStats(bot))
