import pyplayhd

from discord.ext import commands, tasks

from db import *

class UpdateStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mcplayhd: pyplayhd.Client = bot.mcplayhd

        self.to_update = []

        self.fetch_update.start()


    def cog_unload(self):
        self.fetch_update.cancel()
        self.update.cancel()

    @tasks.loop(minutes=1)
    async def fetch_update(self):
        self.to_update = Score.to_update()
    
    @tasks.loop(seconds=1.4) # 6 modes, so 6 call to the api
    async def update(self):
        if self.to_update == []:
            return
        score: Score = self.to_update.pop()
        old_time: int = score.time_best
        old_rank = score.get_rank()

        score.update()

        if old_time is None:
            # First time we got the data, we don't want to send message
            return

        if old_rank != score.get_rank() and old_rank != None:
            await score.send_new_rank(self.bot, old_time, old_rank)
        elif old_time != score.time_best:
            await score.send_new_time(self.bot, old_time, old_rank)


    @fetch_update.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()
        self.update.start()

def setup(bot):
    bot.add_cog(UpdateStats(bot))
