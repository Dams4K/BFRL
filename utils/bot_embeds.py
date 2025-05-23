import discord
from random import choices

class BotEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if text := get_text_footer():
            self.set_footer(text=text)

class NormalEmbed(BotEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = discord.Colour.dark_magenta()

class WarningEmbed(BotEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = discord.Colour.orange()

class DangerEmbed(BotEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = discord.Colour.brand_red()

class InformativeEmbed(BotEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = discord.Colour.blurple()

def get_text_footer():
    texts = {
        None: 3000,
        "go outside": 10,
        "have you heard about CPS Display?": 3,
        "play minecraft.": 4,
        'watch "person of interest"': 3,
        "FMA is a masterpiece too!": 3,
        "Tunic is a masterpiece": 4,
        "good bye.": 15,
        "as you wish": 15,
        "secrets are everywhere": 4,
        "[ The Fourth wall has shattered ]": 10
    }

    return choices(list(texts.keys()), weights=list(texts.values()))[0] 