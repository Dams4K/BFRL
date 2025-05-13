import discord
import pyplayhd

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext
from utils.checks import is_administrator

from mcapi.player import get_uuid
from ddmc import *

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
        if await self.wl_remove_member(ctx, member):
            return
        elif await self.wl_remove_name(ctx, name):
            return
        
        await ctx.respond("Argument missing!")
    
    async def wl_remove_member(self, ctx: BotApplicationContext, member: discord.Member) -> bool:
        if member is None:
            return False
        
        if ctx.whitelist_data.remove(member.id):
            await ctx.respond(f"{member.display_name} removed from the whitelist")
        else:
            await ctx.respond(f"{member.display_name} is not in the whitelist")

        return True
    
    async def wl_remove_name(self, ctx: BotApplicationContext, name: str) -> bool:
        if name == "":
            return False

        uuid = get_uuid(name)
        if uuid == "":
            await ctx.respond("Incorrect name")
            return True
        
        if ctx.whitelist_data.remove_uuid(uuid):
            await ctx.respond(f"{name} removed from the whitelist")
        else:
            await ctx.respond(f"{name} is not in the whitelist")

        return True
        


def setup(bot):
    bot.add_cog(Whitelist(bot))
