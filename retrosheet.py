"""Solve Retrosheet Exercises."""

from bokeh.io import output_file
from bokeh.palettes import viridis
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models.widgets import Tabs, Panel
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

game_data['PARK_ID'] = game_data['PARK_ID'].replace(parknames)

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
print(park_hr.head())
print(park_hr.nlargest(5, 'AVG_HR'))
print(park_hr.nsmallest(5, 'AVG_HR'))


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

mon_panel = Panel(child=mon_fig, title='HR by Month')
park_panel = Panel(child=park_fig, title='HR by Ballpark')

tabs = Tabs(tabs=[mon_panel, park_panel])
show(tabs)
