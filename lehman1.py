"""Solve Chapter 1 of Analyzing Baseball in R, in python."""

from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
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
             plot_height=300,
             plot_width=500,
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

hr_data = teams.groupby('decade').agg({'G': 'sum', 'HR': 'sum', 'SO': 'sum'})

hr_data['G'] = hr_data['G'] / 2  # divide by 2 to not double count games
hr_data['HR Rate'] = hr_data['HR'] / hr_data['G']
hr_data['SO Rate'] = hr_data['SO'] / hr_data['G']
hr_data.reset_index()

hr_cds = ColumnDataSource(hr_data)

fig.line('decade', 'HR Rate',
         color='#CE1141', legend='Home Run Rate',
         source=hr_cds)
fig.line('decade', 'SO Rate',
         color='#006BB6', legend='Strikeout Rate',
         source=hr_cds)

fig.legend.location = 'top_left'

print(hr_data)
show(fig)
