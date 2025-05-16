import gspread

from discord.ext import commands, tasks

from sqlalchemy import asc
from sqlalchemy import select
from sqlalchemy import and_

from db import *
from googlesheet.sheet import *

from mcapi.player import get_name

START_ROW = 2

class UpdateSheet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.update_global.start()


    def cog_unload(self):
        self.update_global.cancel()
        self.update_short.cancel()
        self.update_extrashort.cancel()
        self.update_normal.cancel()
        self.update_long.cancel()
        self.update_inclined.cancel()
        self.update_inclinedshort.cancel()
        self.update_onestack.cancel()


    def update_sheet(self, mode: Mode, worksheet: gspread.Worksheet):
        lb = Score.get_leaderboard(mode)

        cells = worksheet.range(START_ROW, 1, len(lb)+START_ROW-1, 3)
        
        for i in range(len(lb)):
            ranking_cell =  cells[3*i]
            pseudo_cell =   cells[3*i+1]
            score_cell =    cells[3*i+2]

            score, rank = lb[i]
            if score is None or rank is None:
                continue

            ranking_cell.value = f"#{rank}"
            pseudo_cell.value = score.get_name()
            score_cell.value = "{:.3f}".format(score.time_best/1000)

        
        worksheet.update_cells(cells, value_input_option="USER_ENTERED")
    

    @tasks.loop(minutes=4)
    async def update_short(self):
        self.update_sheet(Mode.SHORT, short_worksheet)
    
    @tasks.loop(minutes=4)
    async def update_extrashort(self):
        self.update_sheet(Mode.EXTRASHORT, extrashort_worksheet)

    @tasks.loop(minutes=4)
    async def update_normal(self):
        self.update_sheet(Mode.NORMAL, normal_worksheet)
    
    @tasks.loop(minutes=6)
    async def update_long(self):
        self.update_sheet(Mode.LONG, long_worksheet)

    @tasks.loop(minutes=6)
    async def update_inclined(self):
        self.update_sheet(Mode.INCLINED, inclined_worksheet)

    @tasks.loop(minutes=4)
    async def update_inclinedshort(self):
        self.update_sheet(Mode.INCLINEDSHORT, inclinedshort_worksheet)

    @tasks.loop(minutes=10)
    async def update_onestack(self):
        self.update_sheet(Mode.ONESTACK, onestack_worksheet)

    @tasks.loop(minutes=4)
    async def update_global(self):
        worksheet = global_worksheet

        lb = Score.global_leaderboard()

        cells = worksheet.range(START_ROW, 1, len(lb)+START_ROW-1, 5)
        
        for i in range(len(lb)):
            ranking_cell =  cells[5*i]
            pseudo_cell =   cells[5*i+1]
            score_cell =    cells[5*i+2]
            normal_cell =    cells[5*i+3]
            short_cell =    cells[5*i+4]

            rank, uuid, global_time, normal_time, short_time = lb[i]
            if global_time is None or rank is None:
                continue

            score = Score.of_uuid(uuid, Mode.SHORT)

            ranking_cell.value = f"#{rank}"
            pseudo_cell.value = score.get_name()
            score_cell.value = "{:.3f}".format(global_time/1000)
            normal_cell.value = "{:.3f}".format(normal_time/1000)
            short_cell.value = "{:.3f}".format(short_time/1000)

        
        worksheet.update_cells(cells, value_input_option="USER_ENTERED")

    @update_global.before_loop
    async def before_update_global(self):
        await self.bot.wait_until_ready()

        # Start others
        self.update_short.start()
        self.update_extrashort.start()
        self.update_normal.start()
        self.update_long.start()
        self.update_inclined.start()
        self.update_inclinedshort.start()
        self.update_onestack.start()

def setup(bot):
    bot.add_cog(UpdateSheet(bot))
