from utils.bot_contexts import BotApplicationContext
from discord import Interaction

def is_administrator(ctx: BotApplicationContext):
    return ctx.author.guild_permissions.administrator

def i_is_administrator(int: Interaction):
    return int.user.guild_permissions.administrator