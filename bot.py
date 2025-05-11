import os

import discord

from utils.references import References

class BFRL(discord.Bot):
    def __init__(self):
        super().__init__(debug_guilds=References.DEBUG_GUILDS)

    async def on_ready(self):
        os.system("clear||cls")
        print(self.user, "is ready!")
        print("py-cord version:", discord.__version__)

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
