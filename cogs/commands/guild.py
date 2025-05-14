import discord

from discord.ext import commands

from utils.bot_contexts import BotApplicationContext
from utils.checks import is_administrator

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx: BotApplicationContext):
        return is_administrator(ctx)
    
    update = discord.SlashCommandGroup("update")

    @update.command(name="channel")
    async def updates_channel(self, ctx: BotApplicationContext, channel: discord.TextChannel):
        ctx.dguild.set_update_channel_id(channel.id)
        await ctx.respond(f"New update channel is now {channel.mention}")

def setup(bot):
    bot.add_cog(Guild(bot))