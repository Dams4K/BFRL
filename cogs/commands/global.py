import discord
import pyplayhd

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.respond("World")

    @discord.slash_command()
    async def modes(self, ctx: BotApplicationContext):
        print(ctx.member_data)
        await ctx.defer()
        mcplayhd: pyplayhd.Client = self.bot.mcplayhd
        await ctx.respond(str(mcplayhd.fastbuilder.modes))

def setup(bot):
    bot.add_cog(Global(bot))
