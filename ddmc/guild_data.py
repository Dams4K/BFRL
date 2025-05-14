import discord

from ddm import *

from utils.references import References
from utils.bot_embeds import InformativeEmbed

from .member_data import *
from .whitelist_data import *

from pyplayhd import *

class GuildConfig(Saveable):
    __slots__ = ("_bot", "_guild_id", "update_channel", "whitelist_channel")

    def __init__(self, bot, guild_id):
        self._bot: discord.Bot = bot
        self._guild_id = guild_id
        
        self.update_channel: int = -1
        self.whitelist_channel: int = -1

        super().__init__(References.guild_folder(self._guild_id, "config.json"))

    @Saveable.update
    def set_whitelist_channel(self, value):
        self.whitelist_channel = value

    async def send_whitelist_verification(self, member_data: MemberData):
        if self.whitelist_channel < 0:
            return
        
        member: discord.Member = await self._bot.fetch_user(member_data._member_id)
        channel: discord.TextChannel = await self._bot.fetch_channel(self.whitelist_channel)
        if channel is None:
            return

        embed = InformativeEmbed(title="Whitelist request", description=f"{member.mention} has linked his discord account to `{member_data.player_name}`")
        embed.set_footer(text=str(member_data._member_id))

        await channel.send(embed=embed, view=WhitelistConfirmation())
    
    async def send_new_pb(self, uuid, mode: Mode, time: int):
        mb = MemberData.from_uuid(self._bot, self._guild_id, uuid)
        whitelist = WhitelistData(self._guild_id)
        if not whitelist.is_listed(mb):
            print(uuid, "is not listed")
            return

        if self.update_channel < 0:
            return

        player_name = get_name(uuid)

        channel: discord.TextChannel = await self._bot.fetch_channel(self.update_channel)
        if channel is None:
            return
        
        await channel.send(f"New time of `{time/1000}` for {player_name} in {mode}")

    @staticmethod
    async def guilds_send_new_pb(bot, uuid, mode: Mode, time: int):
        dirs = os.listdir(References.guilds_folder())
        for gf in dirs:
            guild_id = int(gf)
            guild_config = GuildConfig(bot, guild_id)
            await guild_config.send_new_pb(uuid, mode, time)

class WhitelistConfirmation(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Add to whitelist", custom_id="add", style=discord.ButtonStyle.green)
    async def add_button(self, button, interaction: discord.Interaction):
        embeds = interaction.message.embeds
        if len(embeds) == 0:
            await interaction.response.send_message("Failed to add the member to the whitelist")
            return
        
        embed: discord.Embed = embeds[0]
        member_id = int(embed.footer.text)
        wl = WhitelistData(interaction.guild.id)
        wl.add(member_id)

        await interaction.message.delete()
        await interaction.response.send_message("Member added to the whitelist", ephemeral=True)

    @discord.ui.button(label="Reject", custom_id="reject", style=discord.ButtonStyle.red)
    async def reject_button(self, button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.send_message("Member rejected", ephemeral=True)