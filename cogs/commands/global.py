import discord
import pyplayhd

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext
from utils.date import display_time
from utils.autocompletes import ModeOption
from utils.bot_embeds import *
from utils.view import WhitelistConfirmation

from mcapi.player import get_uuid

from db import *

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mcplayhd: pyplayhd.Client = self.bot.mcplayhd

    @discord.slash_command()
    async def time(self, ctx: BotApplicationContext, mode: discord.Option(ModeOption, choices=pyplayhd.Mode.values()), name: str = ""):
        player_uuid = get_uuid(name) or ctx.dmember.uuid
        if player_uuid == "":
            await ctx.respond("You need to specify a player")
            return
        
        score = Score.of_uuid(player_uuid, mode)
        if score.time_total is None or score.time_total == 0:
            await ctx.respond("No information about this player available for now")
            return
        
        calculated_time = display_time(score.time_total//1000)
        await ctx.respond(calculated_time)

    @discord.slash_command()
    async def link(self, ctx: BotApplicationContext, name: str):
        dm = ctx.dmember
        dm.unlist()
        dm.set_uuid(get_uuid(name))

        await ctx.respond(f"Your discord account is linked to the minecraft account named {name}")

        await self.send_whitelist_verification(ctx.dguild, ctx.dmember)
    
    async def send_whitelist_verification(self, dguild: Guild, dmember: Member):        
        member: discord.Member = await dmember.fetch_user(self.bot)
        channel: discord.TextChannel = await dguild.fetch_whitelist_channel(self.bot)
        if channel is None:
            return

        embed = InformativeEmbed(title="Whitelist request", description=f"{member.mention} has linked his discord account to `{dmember.get_name()}`")
        embed.set_footer(text=str(member.id))

        await channel.send(embed=embed, view=WhitelistConfirmation())

def setup(bot):
    bot.add_cog(Global(bot))
