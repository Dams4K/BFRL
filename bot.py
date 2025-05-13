import os
import discord
import pyplayhd

from utils.references import References
from utils.bot_contexts import BotApplicationContext

from ddmc import WhitelistConfirmation

class BFRL(discord.Bot):
    def __init__(self):
        super().__init__(debug_guilds=References.DEBUG_GUILDS)
        self.mcplayhd: pyplayhd.Client = pyplayhd.Client(References.MCPLAYHD_TOKEN)

    async def on_ready(self):
        os.system("clear||cls")
        print(self.user, "is ready!")
        print("py-cord version:", discord.__version__)

        self.add_view(WhitelistConfirmation())

    async def get_application_context(self, interaction, cls = BotApplicationContext):
        return await super().get_application_context(interaction, cls=cls)

    def load_cogs(self, path: str):
        cogs = self.get_cogs(path)
        for cog in cogs:
            self.load_extension(cog)
            print(f"{cog} is loaded")

    def get_cogs(self, path: str) -> list:
        cogs = []
        for root, subdirs, files in os.walk(path):
            for file in files:
                if not file.endswith("py"):
                    continue

                cog_path = os.path.join(root, file).replace("/", ".").replace(".py", "")
                cogs.append(cog_path)
        return cogs
