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


def setup(bot):
    bot.add_cog(Whitelist(bot))
