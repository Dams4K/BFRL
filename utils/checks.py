from utils.bot_contexts import BotApplicationContext

def is_administrator(ctx: BotApplicationContext):
    return ctx.author.guild_permissions.administrator