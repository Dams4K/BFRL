import discord

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext
from utils.checks import is_administrator

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx: BotApplicationContext):
        return is_administrator(ctx)
    
    config = discord.SlashCommandGroup("config", default_member_permissions=discord.Permissions(administrator=True))
    update = config.create_subgroup("update")
    messages = config.create_subgroup("messages")

    whitelist = config.create_subgroup("whitelist")
    link = config.create_subgroup("link")

    @update.command(name="channel")
    async def updates_channel(self, ctx: BotApplicationContext, channel: discord.TextChannel):
        ctx.dguild.set_update_channel(channel)
        await ctx.respond(f"New update channel is now {channel.mention}")

    @messages.command(name="rank")
    async def messages_rank(self, ctx: BotApplicationContext, message: str):
        ctx.dguild.set_rank_message(message)
        await ctx.respond("New rank message set")

    @messages.command(name="time")
    async def messages_time(self, ctx: BotApplicationContext, message: str):
        ctx.dguild.set_time_message(message)
        await ctx.respond("New time message set")

    @whitelist.command(name="channel")
    async def whitelist_channel(self, ctx: BotApplicationContext, channel: discord.TextChannel):
        ctx.dguild.set_whitelist_channel(channel)
        await ctx.respond(f"New self-whitelist is now {channel.mention}")

    @link.command(name="required")
    async def link_required(self, ctx: BotApplicationContext, role: discord.Role):
        ctx.dguild.set_link_required_role(role)
        await ctx.respond(f"{role.name} is now required to use the command /link")

def setup(bot):
    bot.add_cog(Guild(bot))