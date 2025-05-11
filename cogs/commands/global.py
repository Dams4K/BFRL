import discord
import pyplayhd

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext

from mcapi.player import get_uuid

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

    @discord.slash_command()
    async def link(self, ctx: BotApplicationContext, name: str):
        md = ctx.member_data
        if md is None:
            await ctx.respond("Error")
            return

        md.set_uuid(get_uuid(name))
        await ctx.respond(f"Your discord account is linked to the minecraft account named {name}")


def setup(bot):
    bot.add_cog(Global(bot))
