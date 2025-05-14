import os

from ddm import *

from utils.references import References
from utils.date import next_time

from .member_data import MemberData
from .guild_data import GuildConfig

from pyplayhd import *

class BuilderPlayerData(Saveable):
    __slots__ = (
        "_bot",
        "_uuid",
        "normal", "long",
        "short", "extrashort",
        "inclined", "inclinedshort",
        "onestack"
    )

    def __init__(self, bot, uuid):
        self._bot = bot
        self._uuid = uuid

        self.normal = BuilderStatsData(Mode.NORMAL)
        self.long = BuilderStatsData(Mode.LONG)
        self.short = BuilderStatsData(Mode.SHORT)
        self.extrashort = BuilderStatsData(Mode.EXTRASHORT)
        self.inclined = BuilderStatsData(Mode.INCLINED)
        self.inclinedshort = BuilderStatsData(Mode.INCLINEDSHORT)
        self.onestack = BuilderStatsData(Mode.ONESTACK)

        super().__init__(os.path.join(References.FOLDER_DATAS, f"players/{self._uuid}.json"))
    
    @Saveable.update
    async def update(self) -> int:
        await self.normal.update(self._bot, self._uuid)
        await self.long.update(self._bot, self._uuid)
        await self.short.update(self._bot, self._uuid)
        await self.extrashort.update(self._bot, self._uuid)
        await self.inclined.update(self._bot, self._uuid)
        await self.inclinedshort.update(self._bot, self._uuid)
        await self.onestack.update(self._bot, self._uuid)

        return next_time(self.short.time_best)
        

class BuilderStatsData(Data, BuilderStats):
    __slots__ = ("_mode", "time_best", "time_total")
    USE_ONLY_SLOTS = True

    def __init__(self, mode: Mode, *args, **kwargs):
        self._mode = mode

        self.time_best = -1
        self.time_total = -1

        super().__init__(*args, **kwargs)

    async def update(self, bot, uuid: str):
        mcplayhd = Client(References.MCPLAYHD_TOKEN)
        if builder_player := mcplayhd.fastbuilder.mode_player_stats(self._mode, uuid):
            new_best = builder_player.builder_stats.time_best
            if self.time_best != new_best:
                self.time_best = new_best
                await GuildConfig.guilds_send_new_pb(bot, uuid, self._mode, new_best)
            self.time_total = builder_player.builder_stats.time_total
