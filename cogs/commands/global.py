import discord
import pyplayhd

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext
from utils.date import display_time
from utils.autocompletes import ModeOption

from mcapi.player import get_uuid

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mcplayhd: pyplayhd.Client = self.bot.mcplayhd

    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.respond("World")

    @discord.slash_command()
    async def modes(self, ctx: BotApplicationContext):
        await ctx.defer()
        await ctx.respond(str(self.mcplayhd.fastbuilder.modes))

    @discord.slash_command()
    async def stats(self, ctx: BotApplicationContext, name: str):
        await ctx.defer()
        await ctx.respond(self.mcplayhd.fastbuilder.mode_player_stats(pyplayhd.Mode.SHORT, name))

    @discord.slash_command()
    async def time(self, ctx: BotApplicationContext, mode: discord.Option(ModeOption, choices=pyplayhd.Mode.values()), name: str = ""):
        player_name = name or ctx.member_data.uuid
        if player_name == "":
            await ctx.respond("You need to specify a player")
            return
        
        builder_player: pyplayhd.BuilderPlayer = self.mcplayhd.fastbuilder.mode_player_stats(mode, player_name)
        stats: pyplayhd.BuilderStats = builder_player.builder_stats
        
        await ctx.respond(display_time(stats.time_total//1000))

        print(self.mcplayhd.fastbuilder.api_info())

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
