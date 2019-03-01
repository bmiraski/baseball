"""Follow Chapter 4 examples."""

from bokeh.io import curdoc
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.models import Slope
from bokeh.models.widgets import Panel
from bokeh.models.widgets import Tabs
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.themes import Theme
from bokeh.transform import dodge

import math
import numpy as np
import pandas as pd

output_file('chapter4.html', title='Chapter 4 Examples')
curdoc().theme = Theme('baseball_theme.json')

teams = pd.read_csv('data/lehman/baseballdatabank-master/core/Teams.csv')

columns = ['yearID', 'lgID', 'teamID', 'G', 'W', 'L', 'R', 'RA']
teams_short = teams.loc[:, columns].copy()

recent = teams_short['yearID'] >= 2001

recent_teams = teams_short[recent].copy().reset_index()
recent_teams['WinPCT'] = round((recent_teams['W'] / recent_teams['G']), 3)
recent_teams['RunDiff'] = recent_teams['R'] - recent_teams['RA']

coeffs = np.polyfit(recent_teams['RunDiff'], recent_teams['WinPCT'], 1)
print(coeffs)

tooltip = [('Year', '@yearID'),
           ('Team', '@teamID'),
           ('Winning PCT', '@WinPCT'),
           ('Run Diff.', '@RunDiff')]
rt_cds = ColumnDataSource(recent_teams)

winrun_fig = figure(x_axis_label='Run Differential',
                    x_range=(-350, 310),
                    y_axis_label='Winning Percentage',
                    y_range=(0.25, 0.725),
                    title='Winning Percentage vs. Run Differential',
                    tools='hover',
                    tooltips=tooltip,
                    toolbar_location=None)

winrun_fig.circle(x='RunDiff', y='WinPCT', radius=2, alpha=0.5,
                  color='#d71d1d', source=rt_cds)

bf_line = Slope(gradient=coeffs[-2], y_intercept=coeffs[-1],
                line_color='#400987', line_width=2)
winrun_fig.add_layout(bf_line)

winrun_panel = Panel(child=winrun_fig, title='Run Diff. vs. Win Pct.')
tabs = Tabs(tabs=[winrun_panel])

show(tabs)
