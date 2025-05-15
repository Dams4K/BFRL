import discord

from db import *

from utils.checks import i_is_administrator

class WhitelistConfirmation(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction):
        return i_is_administrator(interaction)

    @discord.ui.button(label="Add to whitelist", custom_id="add", style=discord.ButtonStyle.green)
    async def add_button(self, button, interaction: discord.Interaction):
        embeds = interaction.message.embeds
        if len(embeds) == 0:
            await interaction.response.send_message("Failed to add the member to the whitelist")
            return
        
        embed: discord.Embed = embeds[0]
        member_id = int(embed.footer.text)
        
        Whitelist.whitelist(interaction.guild.id, member_id)

        await interaction.message.delete()
        await interaction.response.send_message("Member added to the whitelist", ephemeral=True)

    @discord.ui.button(label="Reject", custom_id="reject", style=discord.ButtonStyle.red)
    async def reject_button(self, button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.send_message("Member rejected", ephemeral=True)