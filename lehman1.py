"""Solve Chapter 1 of Analyzing Baseball in R, in python."""

from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Label, Span
from bokeh.models.widgets import Tabs, Panel
from bokeh.models.tickers import FixedTicker

import math
import pandas as pd


def custom_range(x, y, step):
    """Generate a list of numbers at a given interval."""
    ran = []
    while x <= y:
        ran.append(x)
        x += step
    return ran

output_file('chapter1_2.html')
fig = figure(background_fill_color='gray',
             background_fill_alpha=0.5,
             border_fill_color='blue',
             border_fill_alpha=0.25,
             plot_height=500,
             plot_width=800,
             h_symmetry=True,
             x_axis_label='Decade',
             x_axis_type='linear',
             x_axis_location='below',
             x_range=(1860, 2020),
             y_axis_label='Rate',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(0, 20),
             title='Rate of HR and SO per game by Decade',
             title_location='above',
             toolbar_location=None)

fig.xaxis.ticker = FixedTicker(ticks=custom_range(1860, 2020, 10))
fig.xaxis.major_label_orientation = math.pi/4

# master = pd.read_csv('data/lehman/baseballdatabank-master/core/Master.csv')

# columns = master.columns
# print(master.head(1))
# print(columns)

# batting = pd.read_csv('data/lehman/baseballdatabank-master/core/Batting.csv')
# columns_batting = batting.columns

# print(batting.head(1))
# print(columns_batting)

teams = pd.read_csv('data/lehman/baseballdatabank-master/core/Teams.csv')

teams['yearID'] = teams['yearID'].astype(float)

years = teams['yearID']

decades = []
for year in years:
    dec = math.floor(year / 10) * 10
    decades.append(dec)

teams['decade'] = decades

teams['yearID'] = teams['yearID'].astype(int)

hr_data = teams.groupby('decade').agg({'G': 'sum', 'HR': 'sum', 'SO': 'sum'})

hr_data['G'] = hr_data['G'] / 2  # divide by 2 to not double count games
hr_data['HR Rate'] = hr_data['HR'] / hr_data['G']
hr_data['SO Rate'] = hr_data['SO'] / hr_data['G']

hr_cds = ColumnDataSource(hr_data)

fig.line('decade', 'HR Rate',
         color='#CE1141', legend='Home Run Rate',
         source=hr_cds)
fig.line('decade', 'SO Rate',
         color='#006BB6', legend='Strikeout Rate',
         source=hr_cds)

fig.legend.location = 'top_left'

print(hr_data)
# show(fig)

# Begin solution to analyzing effect of DH on run scoring.

al_data = teams[teams['lgID'] == 'AL']
al_data = al_data.groupby('yearID').agg({'G': 'sum', 'R': 'sum'})
al_data['R per G'] = al_data['R'] / al_data['G']
# Note this is runs per team per game. Important for interleague play.

nl_data = teams[teams['lgID'] == 'NL']
nl_data = nl_data.groupby('yearID').agg({'G': 'sum', 'R': 'sum'})
nl_data['R per G'] = nl_data['R'] / nl_data['G']

run_data = figure(background_fill_color='gray',
                  background_fill_alpha=0.5,
                  border_fill_color='blue',
                  border_fill_alpha=0.25,
                  plot_height=500,
                  plot_width=800,
                  h_symmetry=True,
                  x_axis_label='Year',
                  x_axis_type='linear',
                  x_axis_location='below',
                  x_range=(1870, 2020),
                  y_axis_label='Runs per Team per Game',
                  y_axis_type='linear',
                  y_axis_location='left',
                  y_range=(2, 8),
                  title='Average Runs Scored per Game by Team, AL vs. NL',
                  title_location='above',
                  toolbar_location=None)

run_data.xaxis.major_label_orientation = math.pi/4

al_cds = ColumnDataSource(al_data)
nl_cds = ColumnDataSource(nl_data)

run_data.line('yearID', 'R per G',
              color='#CE1141', legend='American League',
              source=al_cds)
run_data.line('yearID', 'R per G',
              color='#006BB6', legend='National League',
              source=nl_cds)

dh = Span(location=1973, dimension='height', line_color='green',
          line_dash='dashed', line_width=3)
dh_label = Label(angle=90, angle_units='deg', text='DH Starts', x=1972,
                 x_offset=3, y=6)

run_data.add_layout(dh)
run_data.add_layout(dh_label)

hr_panel = Panel(child=fig, title='HR and SO by decade')
run_panel = Panel(child=run_data, title='Run Scoring by League')
tabs = Tabs(tabs=[hr_panel, run_panel])

show(tabs)
