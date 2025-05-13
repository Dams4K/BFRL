from ddm import *
from utils.references import References

from .member_data import MemberData

from pyplayhd import *

class BuilderPlayerData(Saveable):
    __slots__ = (
        "_guild_id", "_uuid", "did",
        "normal",
        "short", "extra_short",
        "inclined", "inclined_short",
        "onestack"
    )

    def __init__(self, guild_id, uuid):
        self._guild_id = guild_id
        self._uuid = uuid

        self.normal = BuilderStatsData(Mode.NORMAL)
        self.short = BuilderStatsData(Mode.SHORT)
        self.extra_short = BuilderStatsData(Mode.EXTRASHORT)
        self.inclined = BuilderStatsData(Mode.INCLINED)
        self.inclined_short = BuilderStatsData(Mode.INCLINEDSHORT)
        self.onestack = BuilderStatsData(Mode.ONESTACK)

        self.did = -1

        super().__init__(References.guild_folder(self._guild_id, f"players/{self._uuid}.json"))
    
    def has_discord_account(self) -> bool:
        return self.did >= 0
    
    def get_member_data(self) -> MemberData | None:
        if not self.has_discord_account():
            return None

        return MemberData(self._guild_id, self.did)

class BuilderStatsData(Data, BuilderStats):
    __slots__ = ("_mode", "time_best", "time_total")
    USE_ONLY_SLOTS = True

    def __init__(self, mode: Mode, *args, **kwargs):
        self._mode = mode

        super().__init__(*args, **kwargs)
