from discord.ext.commands import Converter

from pyplayhd import Mode

class ModeOption(Converter):
    async def convert(self, ctx, name) -> Mode:
        return Mode[name.upper()]