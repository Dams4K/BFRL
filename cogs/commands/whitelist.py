import discord
import pyplayhd

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext
from utils.checks import is_administrator

from mcapi.player import get_uuid
from ddmc import MemberData

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx: BotApplicationContext):
        return is_administrator(ctx)
    
    whitelist = discord.SlashCommandGroup("whitelist")

    @whitelist.command(name="add")
    async def whitelist_add(self, ctx: BotApplicationContext, member: discord.Member, name: str) -> None:
        uuid: str = get_uuid(name)
        if uuid == "":
            await ctx.respond("Incorrect minecraft name")
            return

        md = MemberData(ctx.guild.id, member.id)
        md.set_uuid(uuid)
        ctx.whitelist_data.add(member.id)

        await ctx.respond(f"{member.display_name} is now whitelisted")
    
    @whitelist.command(name="remove")
    async def whitelist_remove(self, ctx: BotApplicationContext, member: discord.Member = None, name: str = "") -> None:
        if member is None and name == "":
            await ctx.respond("Argument missing!")
            return

        if member:
            if ctx.whitelist_data.remove(member.id):
                await ctx.respond(f"{member.display_name} removed from the whitelist")
                return
            await ctx.respond(f"{member.display_name} is not in the whitelist")
            return
        
        uuid = get_uuid(name)
        if uuid == "":
            await ctx.respond("Incorrect name")
            return

        if ctx.whitelist_data.remove_uuid(uuid):
            await ctx.respond(f"{name} removed from the whitelist")
            return
        await ctx.respond("ERR")
        


def setup(bot):
    bot.add_cog(Whitelist(bot))
