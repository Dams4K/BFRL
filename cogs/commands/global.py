import discord
from discord.ext import commands

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.respond("World")


def setup(bot):
    bot.add_cog(Global(bot))
