import discord
import pyplayhd

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext
from utils.checks import is_administrator

from mcapi.player import get_uuid

from db import *

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx: BotApplicationContext):
        return is_administrator(ctx)
    
    whitelist = discord.SlashCommandGroup("whitelist", default_member_permissions=discord.Permissions(administrator=True))

    @whitelist.command(name="role")
    async def whitelist_role(self, ctx: BotApplicationContext, role: discord.Role):
        ctx.guild_config.set_role_id(role.id)
        await ctx.respond(f"New role required to use the link cmd is now {role.name}")

    @whitelist.command(name="add")
    async def whitelist_add(self, ctx: BotApplicationContext, member: discord.Member, name: str) -> None:
        uuid: str = get_uuid(name)
        if uuid == "":
            await ctx.respond("Incorrect minecraft name")
            return

        dm = Member.from_id(ctx.guild.id, member.id)
        dm.set_uuid(uuid)
        dm.whitelist()

        await ctx.respond(f"{member.display_name} is now whitelisted")

    
    @whitelist.command(name="remove")
    async def whitelist_remove(self, ctx: BotApplicationContext, member: discord.Member = None, name: str = "") -> None:
        member: Member = None
        if not member is None:
            member = Member.from_id(ctx.guild.id, member.id)
        if uuid := get_uuid(name):
            member = Member.from_uuid(ctx.guild.id, uuid)

        if member is None:
            await ctx.respond("Member not found")
            return

        member.unlist()
        await ctx.respond("Member unlisted")
    
    
def setup(bot):
    bot.add_cog(Whitelist(bot))
