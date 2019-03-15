"""Complete Chapter 4 exercises."""

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

from itertools import product
import math
import numpy as np
import pandas as pd

output_file('chapter4ex.html', title='Chapter 4 Exercises')
curdoc().theme = Theme('baseball_theme.json')

teams = pd.read_csv('data/lehman/baseballdatabank-master/core/Teams.csv')

columns = ['yearID', 'lgID', 'teamID', 'G', 'W', 'L', 'R', 'RA']
teams_short = teams.loc[:, columns].copy()
teams_short['WinPCT'] = round(teams_short['W'] / teams_short['G'], 3)
teams_short['RunDiff'] = teams_short['R'] - teams_short['RA']

sixty = (teams_short['yearID'] > 1960) & (teams_short['yearID'] <= 1970)
seventy = (teams_short['yearID'] > 1970) & (teams_short['yearID'] <= 1980)
eighty = (teams_short['yearID'] > 1980) & (teams_short['yearID'] <= 1990)
ninety = (teams_short['yearID'] > 1990) & (teams_short['yearID'] <= 2000)
aughts = (teams_short['yearID'] > 2000) & (teams_short['yearID'] <= 2010)

teams_sixty = teams_short[sixty].copy()
teams_seventy = teams_short[seventy].copy()
teams_eighty = teams_short[eighty].copy()
teams_ninety = teams_short[ninety].copy()
teams_aughts = teams_short[aughts].copy()

dfs = [teams_sixty, teams_seventy, teams_eighty, teams_ninety, teams_aughts]
coeffs = []
for df in dfs:
    coeff = tuple(np.polyfit(df['RunDiff'], df['WinPCT'], 1))
    coeffs.append(coeff)

index = ['1960s', '1970s', '1980s', '1990s', '2000s']
fit_df = pd.DataFrame(coeffs, columns=['slope', 'y-int'], index=index)
fit_df['10Run'] = round(fit_df['slope'] * 10 + fit_df['y-int'], 3)
fit_df['W'] = round(fit_df['10Run'] * 162, 0)

print(fit_df)

cent19 = teams_short['yearID'] < 1901
old_teams = teams_short[cent19].copy()

old_coeff = np.polyfit(old_teams['RunDiff'], old_teams['WinPCT'], 1)
print(old_coeff)
old_teams['Predict'] = round((old_coeff[-2] * old_teams['RunDiff']) +
                             old_coeff[-1], 3)
old_teams['PytErr'] = old_teams['WinPCT'] - old_teams['Predict']

team80 = (teams_short['yearID'] >= 1980) & (teams_short['yearID'] < 1990)
teams80 = teams_short[team80].copy()

teams80['logWRatio'] = np.log(np.array(teams80['W'] / teams80['L']))
teams80['logRRatio'] = np.log(np.array(teams80['R'] / teams80['RA']))

coeffs_pyt = np.polyfit(teams80['logRRatio'], teams80['logWRatio'], 1)
print(coeffs_pyt)

game_data = pd.read_csv('data/retrosheet/allgameex1980s.csv')
# print(game_data.head())
# print(game_data.tail())

columns_80 = ['AWAY_SCORE_CT', 'HOME_SCORE_CT', 'AWAY_MANAGER_ID',
              'AWAY_MANAGER_NAME_TX', 'HOME_MANAGER_ID',
              'HOME_MANAGER_NAME_TX']

short_80 = game_data.loc[:, columns_80].copy()
print(short_80['AWAY_MANAGER_ID'].describe())
print(short_80.head())


old_cds = ColumnDataSource(old_teams)

tooltips = [('Year', '@yearID'),
            ('Team', '@teamID'),
            ('Run Diff', '@RunDiff'),
            ('Win Pct.', '@WinPCT')]

old_fig = figure(x_axis_label='Run Differential',
                 x_range=(-750, 500),
                 y_axis_label='Residual',
                 y_range=(-0.4, 0.22),
                 tools='hover',
                 tooltips=tooltips,
                 toolbar_location=None)

old_fig.circle(x='RunDiff', y='PytErr', radius=10, alpha=0.5, color='#7d4b93',
               source=old_cds)

# show(old_fig)
