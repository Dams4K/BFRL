from bot import BFRL

from utils.references import References

bot = BFRL()
bot.load_cogs(References.FOLDER_COGS)
bot.run(References.DISCORD_TOKEN)
