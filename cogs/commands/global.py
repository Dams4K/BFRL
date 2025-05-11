import discord
import pyplayhd
from discord.commands.context import ApplicationContext
from discord.ext import commands

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.respond("World")

    @discord.slash_command()
    async def modes(self, ctx: ApplicationContext):
        await ctx.defer()
        mcplayhd: pyplayhd.Client = self.bot.mcplayhd
        await ctx.respond(str(mcplayhd.fastbuilder.modes))

def setup(bot):
    bot.add_cog(Global(bot))
