"""Solve Retrosheet Exercises."""

from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.models import Label
from bokeh.models import LabelSet
from bokeh.models import Slope
from bokeh.models.widgets import Panel
from bokeh.models.widgets import Tabs
from bokeh.palettes import viridis
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.transform import factor_cmap

from collections import defaultdict

import csv
import math
import pandas as pd

output_file('retrosheet.html')

eighties = pd.read_csv('data/retrosheet/allgameex1980s.csv')
nineties = pd.read_csv('data/retrosheet/allgameex1990s.csv')
aughts = pd.read_csv('data/retrosheet/allgameex2000s.csv')
teens = pd.read_csv('data/retrosheet/allgameex2010s.csv')

game_data = pd.concat([eighties, nineties, aughts, teens])

game_data['GAME_MON'] = pd.to_datetime(game_data['GAME_DT'],
                                       format='%Y%m%d').dt.month

game_data['GAME_COUNT'] = 1
game_data['TOTAL_HR'] = game_data['AWAY_HR_CT'] + game_data['HOME_HR_CT']

parknames = defaultdict()
with open('data/retrosheet/parkID.csv', newline='') as p:
    parks = csv.reader(p, delimiter=',')
    for row in parks:
        parknames[row[0]] = row[1]

people = defaultdict()
with open('data/retrosheet/personID.csv', newline='') as person:
    persons = csv.reader(person, delimiter=',')
    for row in persons:
        people[row[0]] = row[2] + " " + row[1]

game_data['PARK_ID'] = game_data['PARK_ID'].replace(parknames)
game_data['BASE4_UMP_ID'] = game_data['BASE4_UMP_ID'].replace(people)

mon_hr = game_data.groupby('GAME_MON').agg({'TOTAL_HR': 'sum',
                                            'GAME_COUNT': 'sum'})

mon_hr['AVG_HR'] = mon_hr['TOTAL_HR'] / mon_hr['GAME_COUNT']
month_names = ['March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October']
mon_hr['MONTH_NAME'] = month_names
mon_hr['MON_LABELS'] = mon_hr['AVG_HR'].round(3)

park_hr = game_data.groupby('PARK_ID').agg({'TOTAL_HR': 'sum',
                                            'GAME_COUNT': 'sum'})
park_hr['AVG_HR'] = park_hr['TOTAL_HR'] / park_hr['GAME_COUNT']
park_hr = park_hr.sort_values('AVG_HR', ascending=False)

print(mon_hr)
print(park_hr.nlargest(5, 'AVG_HR'))
print(park_hr.nsmallest(5, 'AVG_HR'))

ump_run = game_data.groupby('BASE4_UMP_ID').agg({'GAME_COUNT': 'sum',
                                                 'AWAY_SCORE_CT': 'sum',
                                                 'HOME_SCORE_CT': 'sum'})

ump_run_400 = ump_run.GAME_COUNT > 400
ump_run = ump_run[ump_run_400]
ump_run['AVG_HOME'] = ump_run['HOME_SCORE_CT'] / ump_run['GAME_COUNT']
ump_run['AVG_VIS'] = ump_run['AWAY_SCORE_CT'] / ump_run['GAME_COUNT']
ump_run['AVG_GAME'] = ump_run['AVG_HOME'] + ump_run['AVG_VIS']
ump_run = ump_run.sort_values('AVG_GAME', ascending=False)

print(ump_run.nlargest(5, 'AVG_GAME'))
print(ump_run.nsmallest(5, 'AVG_GAME'))
print(ump_run.nlargest(10, 'AVG_HOME'))
print(ump_run.nlargest(10, 'AVG_VIS'))
print(ump_run.nsmallest(10, 'AVG_HOME'))
print(ump_run.nsmallest(10, 'AVG_VIS'))

day_attend = game_data.groupby('GAME_DY').agg(
    {'GAME_COUNT': 'sum', 'ATTEND_PARK_CT': 'sum'})

day_attend['AVG_ATTEND'] = (day_attend['ATTEND_PARK_CT'] /
                            day_attend['GAME_COUNT'])

day_attend = day_attend.sort_values('AVG_ATTEND', ascending=False)
days = day_attend.index.tolist()

mon_fig = figure(background_fill_color='gray',
                 background_fill_alpha=0.5,
                 border_fill_color='blue',
                 border_fill_alpha=0.25,
                 plot_height=500,
                 plot_width=800,
                 h_symmetry=True,
                 x_axis_label='Month',
                 x_range=month_names,
                 x_axis_location='below',
                 y_axis_label='Avg. HR / Game',
                 y_axis_type='linear',
                 y_axis_location='left',
                 y_range=(1.5, 2.25),
                 title='Avg. HR per game by Month, 1980-2017',
                 title_location='above',
                 toolbar_location=None)

mon_fig.xaxis.major_label_orientation = math.pi/4

mon_cds = ColumnDataSource(mon_hr)

mon_fig.line('MONTH_NAME', 'AVG_HR', color='#CE1141',
             source=mon_cds)

rate_label = LabelSet(x='MONTH_NAME', y='AVG_HR', text='MON_LABELS',
                      level='glyph', x_offset=5, y_offset=5, source=mon_cds)
mon_fig.add_layout(rate_label)

park_range = park_hr.index.tolist()
park_cds = ColumnDataSource(park_hr)
park_fig = figure(background_fill_color='gray',
                  background_fill_alpha=0.5,
                  border_fill_color='blue',
                  border_fill_alpha=0.25,
                  plot_height=800,
                  plot_width=1000,
                  h_symmetry=True,
                  x_axis_label='Ballpark',
                  x_axis_location='below',
                  x_range=park_range,
                  y_axis_label='Avg. HR / Game',
                  y_axis_type='linear',
                  y_axis_location='left',
                  y_range=(0, 4),
                  title='Avg. HR per game by Ballpark, 1980-2017',
                  title_location='above',
                  toolbar_location=None)

park_fig.xgrid.grid_line_color = None
park_fig.xaxis.major_label_orientation = math.pi/2
colorscheme = viridis(75)

park_fig.vbar(x='PARK_ID', top='AVG_HR', width=0.9, source=park_cds,
              line_color='white',
              fill_color=factor_cmap('PARK_ID',
                                     palette=colorscheme,
                                     factors=park_range))

ump_cds = ColumnDataSource(ump_run)

ump_fig = figure(background_fill_color='gray',
                 background_fill_alpha=0.5,
                 border_fill_color='blue',
                 border_fill_alpha=0.25,
                 plot_height=800,
                 plot_width=1000,
                 h_symmetry=True,
                 x_axis_label='Home Avg. Runs',
                 x_axis_type='linear',
                 x_axis_location='below',
                 x_range=(4, 5.25),
                 y_axis_label='Visitor Avg. Runs',
                 y_axis_type='linear',
                 y_axis_location='left',
                 y_range=(3.75, 5.25),
                 title='Home Plate Umpire Average Runs per game',
                 title_location='above',
                 toolbar_location=None)

ump_fig.circle('AVG_HOME', 'AVG_VIS', size=20, color='#006BB6',
               source=ump_cds)
slope = Slope(gradient=1, y_intercept=0, line_color='#CE1141',
              line_dash='dashed', line_width=3)
ump_fig.add_layout(slope)
chuck = Label(x=5, y=5.04, text='Chuck Meriwether')
ump_fig.add_layout(chuck)
doug = Label(x=4.08, y=3.76, text='Doug Harvey')
ump_fig.add_layout(doug)
joe = Label(x=4.55, y=4.31, text='Joe West')
# ump_fig.add_layout(joe)
alfonso = Label(x=4.8, y=4.09, text='Alfonso Marquez')
ump_fig.add_layout(alfonso)

attend_cds = ColumnDataSource(day_attend)
attend_fig = figure(background_fill_color='gray',
                    background_fill_alpha=0.5,
                    border_fill_color='blue',
                    border_fill_alpha=0.25,
                    plot_height=800,
                    plot_width=1000,
                    h_symmetry=True,
                    x_axis_label='Day of the Week',
                    x_axis_location='below',
                    x_range=days,
                    y_axis_label='Avg. Attendance',
                    y_axis_type='linear',
                    y_axis_location='left',
                    y_range=(24000, 33000),
                    title='Avg. Attendance by Day of the Week',
                    title_location='above',
                    toolbar_location=None)

attend_fig.xgrid.grid_line_color = None
attend_fig.xaxis.major_label_orientation = math.pi/4
colorscheme_attend = viridis(7)

attend_fig.vbar(x='GAME_DY', top='AVG_ATTEND', width=0.9,
                source=attend_cds, line_color='white',
                fill_color=factor_cmap('GAME_DY',
                                       palette=colorscheme_attend,
                                       factors=days))

mon_panel = Panel(child=mon_fig, title='HR by Month')
park_panel = Panel(child=park_fig, title='HR by Ballpark')
ump_panel = Panel(child=ump_fig, title='Umpire Runs')
day_panel = Panel(child=attend_fig, title='Avg. Attendance')

tabs = Tabs(tabs=[mon_panel, park_panel, ump_panel, day_panel])
show(tabs)
