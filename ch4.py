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

from itertools import product
import math
import numpy as np
import pandas as pd


def twenty_five(s):
    """Extract the 25% population value."""
    return(s.describe().loc['25%'])


def seventy_five(s):
    """Extract the 75% population value."""
    return(s.describe().loc['75%'])


def ir(rs, ra):
    """Determine incremental runs per win."""
    return(((rs ** 2 + ra ** 2) ** 2) /
           (2 * rs * ra ** 2))

output_file('chapter4.html', title='Chapter 4 Examples')
curdoc().theme = Theme('baseball_theme.json')

teams = pd.read_csv('data/lehman/baseballdatabank-master/core/Teams.csv')

columns = ['yearID', 'lgID', 'teamID', 'G', 'W', 'L', 'R', 'RA']
teams_short = teams.loc[:, columns].copy()

recent = teams_short['yearID'] >= 2001

recent_teams = teams_short[recent].copy().reset_index(drop=True)
recent_teams['WinPCT'] = round((recent_teams['W'] / recent_teams['G']), 3)
recent_teams['RunDiff'] = recent_teams['R'] - recent_teams['RA']

coeffs = np.polyfit(recent_teams['RunDiff'], recent_teams['WinPCT'], 1)
print(coeffs)

recent_teams['Predict'] = (coeffs[-2] * recent_teams['RunDiff']) + coeffs[-1]
recent_teams['Error'] = recent_teams['WinPCT'] - recent_teams['Predict']

RMSE = math.sqrt(np.mean(np.square(recent_teams['Error'])))
print(RMSE)

within_one = (abs(recent_teams['Error']) < RMSE).sum()
within_two = (abs(recent_teams['Error']) < (2 * RMSE)).sum()

within_one_pct = round(within_one / len(recent_teams), 3)
within_two_pct = round(within_two / len(recent_teams), 3)

print(len(recent_teams), within_one, within_two, within_one_pct, within_two_pct)

recent_teams['WPctPyt'] = (recent_teams['R'] ** 2) / ((recent_teams['R'] ** 2) +
                                                      (recent_teams['RA'] ** 2))
recent_teams['ErrPyt'] = recent_teams['WinPCT'] - recent_teams['WPctPyt']

RMSE_PYT = math.sqrt(np.mean(np.square(recent_teams['ErrPyt'])))
print(RMSE_PYT)

recent_teams['logWRatio'] = np.log(np.array(recent_teams['W'] / recent_teams['L']))
recent_teams['logRRatio'] = np.log(np.array(recent_teams['R'] / recent_teams['RA']))
print(recent_teams.head(30))

coeffs_pyt = np.polyfit(recent_teams['logRRatio'], recent_teams['logWRatio'], 1)
print(coeffs_pyt)
within_one_pyt = (abs(recent_teams['ErrPyt']) < RMSE).sum()
within_two_pyt = (abs(recent_teams['ErrPyt']) < (2 * RMSE)).sum()

within_one_pct_pyt = round(within_one_pyt / len(recent_teams), 3)
within_two_pct_pyt = round(within_two_pyt / len(recent_teams), 3)

print(len(recent_teams), within_one_pyt, within_two_pyt, within_one_pct_pyt,
      within_two_pct_pyt)

columns3 = pd.read_csv('data/general/game_log_header.csv').columns.to_list()
gamelist2011 = pd.read_csv('data/general/gl2011.txt', header=None)
gamelist2011.columns = columns3

bos_crit1 = gamelist2011['VisitingTeam'] == 'BOS'
bos_crit2 = gamelist2011['HomeTeam'] == 'BOS'
bos_crit = bos_crit1 | bos_crit2

keep_cols = ['VisitingTeam', 'HomeTeam', 'VisitorRunsScored', 'HomeRunsScore']
bos_games = gamelist2011.loc[bos_crit].copy()
bos_games = bos_games.loc[:, keep_cols].copy()

ht = bos_games['HomeTeam'].to_list()
vrs = bos_games['VisitorRunsScored'].to_list()
hrs = bos_games['HomeRunsScore'].to_list()
rundiff = []
for x in range(0, len(ht)):
    if ht[x] == 'BOS':
        diff = hrs[x] - vrs[x]
    else:
        diff = vrs[x] - hrs[x]
    rundiff.append(diff)

bos_games['ScoreDiff'] = rundiff
bos_games['W'] = (bos_games['ScoreDiff'] > 0).astype(int)

# print(bos_games.head(10))
# print(bos_games['HomeRunsScore'].describe())

bsum = bos_games.groupby('W')['ScoreDiff'].agg(['size', 'mean', 'std', 'min',
                                                twenty_five, 'median',
                                                seventy_five, 'max'])
bsum.columns = ['Count', 'Mean', 'StDev', 'P0', 'P25', 'P50', 'P75', 'P100']

# print(bsum)

results = gamelist2011.loc[:, keep_cols].copy()

results['VisWin'] = (
    results['VisitorRunsScored'] > results['HomeRunsScore']).astype(int)
results['HomeWin'] = (
    results['HomeRunsScore'] > results['VisitorRunsScored']).astype(int)
results['winner'] = np.maximum(results['VisWin'] * results['VisitingTeam'],
                               results['HomeWin'] * results['HomeTeam'])
results['diff'] = abs(results['VisitorRunsScored'] - results['HomeRunsScore'])
results = results.drop(['VisWin', 'HomeWin'], axis=1)

results['1-Run'] = (results['diff'] == 1).astype(int)
onerunwins = results.groupby('winner')['1-Run'].sum()

onerunwins = onerunwins.to_frame().reset_index().sort_values('winner')
onerunwins.columns = ['teamID', '1-Run']

print(onerunwins.head())

teams2011 = recent_teams['yearID'] == 2011
data2011 = recent_teams[teams2011].copy()

data_short = data2011[['teamID', 'WPctPyt', 'ErrPyt']].copy() \
                                                      .sort_values('teamID') \
                                                      .reset_index(drop=True)
data_short.loc[13, 'teamID'] = 'ANA'
data_short = data_short.sort_values('teamID').reset_index(drop=True)
data_short['1-Run'] = onerunwins['1-Run']

print(data_short)

pitching = pd.read_csv('data/lehman/baseballdatabank-master/core/Pitching.csv')

closer = (pitching['GF'] > 50) & (pitching['ERA'] < 2.5)

top_closers = pitching[closer].copy()
top_closers = top_closers[['playerID', 'yearID', 'teamID']].copy()
rec_top_closer = recent_teams.merge(top_closers, on=['yearID', 'teamID'])
close_error = rec_top_closer['ErrPyt'].describe()

print(close_error)
print(round(close_error['mean'] * 162, 3))

runlist = list((x / 2) for x in range(6, 13))

run_groups = list(product(runlist, repeat=2))

rg_df = pd.DataFrame(run_groups, columns=['RS', 'RA'])

rg_df['IR'] = ir(rg_df['RS'], rg_df['RA'])
ir_pivot = rg_df.pivot(index='RS', columns='RA', values='IR')
print(ir_pivot)

ds_cds = ColumnDataSource(data_short)
ds_tooltip = [('Team', '@teamID')]

ds_fig = figure(x_axis_label='One Run Wins',
                x_range=(17, 35),
                y_axis_label='Pythagorean Error',
                y_range=(-0.06, 0.06),
                title='2011 One Run Wins vs. Pythag Error',
                tools='hover',
                tooltips=ds_tooltip,
                toolbar_location=None)

ds_fig.circle(x='1-Run', y='ErrPyt', radius=0.3, alpha=0.5, color='#143913',
              source=ds_cds)

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

error_fig = figure(x_axis_label='Run Differential',
                   x_range=(-350, 310),
                   y_axis_label='Residual',
                   y_range=(-0.075, 0.09),
                   title='Residual Errors in Linear Regression',
                   tools='hover',
                   tooltips=tooltip,
                   toolbar_location=None)

error_fig.circle(x='RunDiff', y='Error', radius=2, alpha=0.5, color='#d71d1d',
                 source=rt_cds)

ds_panel = Panel(child=ds_fig, title='One Run Wins')
error_panel = Panel(child=error_fig, title='Regression Residuals')
winrun_panel = Panel(child=winrun_fig, title='Run Diff. vs. Win Pct.')
tabs = Tabs(tabs=[winrun_panel, error_panel, ds_panel])
show(tabs)
