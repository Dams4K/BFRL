import os

from ddm import *

from utils.references import References
from utils.date import next_time

from .member_data import MemberData

from pyplayhd import *

class BuilderPlayerData(Saveable):
    __slots__ = (
        "_uuid",
        "normal", "long",
        "short", "extrashort",
        "inclined", "inclinedshort",
        "onestack"
    )

    def __init__(self, uuid):
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
    def update(self) -> int:
        self.normal.update(self._uuid)
        self.long.update(self._uuid)
        self.short.update(self._uuid)
        self.extrashort.update(self._uuid)
        self.inclined.update(self._uuid)
        self.inclinedshort.update(self._uuid)
        self.onestack.update(self._uuid)

        return next_time(self.short.time_best)
        

class BuilderStatsData(Data, BuilderStats):
    __slots__ = ("_mode", "time_best", "time_total")
    USE_ONLY_SLOTS = True

    def __init__(self, mode: Mode, *args, **kwargs):
        self._mode = mode

        self.time_best = -1
        self.time_total = -1

        super().__init__(*args, **kwargs)

    def update(self, uuid: str):
        mcplayhd = Client(References.MCPLAYHD_TOKEN)
        if builder_player := mcplayhd.fastbuilder.mode_player_stats(self._mode, uuid):
            self.time_best = builder_player.builder_stats.time_best
            self.time_total = builder_player.builder_stats.time_total
