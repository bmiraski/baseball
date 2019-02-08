"""Follow along with some additional data exercises."""

from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.plotting import show

from bokeh.models.widgets import Panel
from bokeh.models.widgets import Tabs

import math
import pandas as pd

output_file('chapter2.html')


def getPlayerNames(idlist, masterdf):
    """Retrieve the full player names from the Master Data file."""
    player_names = []
    for player in idlist:
        name = (str(masterdf.loc[player].nameFirst) + " " +
                str(masterdf.loc[player].nameLast))
        player_names.append(name)
    return player_names


master = pd.read_csv('data/lehman/baseballdatabank-master/core/Master.csv',
                     index_col='playerID')
batting = pd.read_csv('data/lehman/baseballdatabank-master/core/Batting.csv',
                      index_col="playerID")

cols = ['yearID', 'AB', 'HR']
mantle = batting.loc['mantlmi01', cols].copy()

# mantle was born in Oct. so birth year is moved to 1932.
mantle['Age'] = mantle['yearID'] - 1932
mantle['HRrate'] = round((mantle['HR'] / mantle['AB']) * 100, 2)
print(mantle)

mantle_fig = figure(background_fill_color='gray',
                    background_fill_alpha=0.5,
                    border_fill_color='blue',
                    border_fill_alpha=0.25,
                    plot_height=500,
                    plot_width=800,
                    h_symmetry=True,
                    x_axis_label='Age',
                    x_axis_type='linear',
                    x_axis_location='below',
                    x_range=(19, 37),
                    y_axis_label='Home Run Rate',
                    y_axis_type='linear',
                    y_axis_location='left',
                    y_range=(2, 11),
                    title='Mantle HR Rate by Age',
                    title_location='above',
                    toolbar_location=None)

mantle_cds = ColumnDataSource(mantle)
mantle_fig.line('Age', 'HRrate', color='#006BB6', source=mantle_cds)

batting2 = pd.read_csv('data/lehman/baseballdatabank-master/core/Batting.csv')

years = batting2['yearID'].astype(float)

decades = []
for year in years:
    dec = math.floor(year / 10) * 10
    decades.append(dec)

batting2['Decade'] = decades


dec_hr = (batting2.groupby(['Decade', 'playerID']).agg({'HR': 'sum'}))
dec_hr = dec_hr.sort_values(['Decade', 'HR'], ascending=False).reset_index()
dec_hr_top = dec_hr.drop_duplicates('Decade')

players = dec_hr_top['playerID']

player_names = getPlayerNames(players, master)

dec_hr_top['playerName'] = player_names
print(dec_hr_top)

# long careers

careers = batting.groupby('playerID').agg({'AB': 'sum', 'HR': 'sum',
                                           'SO': 'sum'})
long = careers['AB'] >= 5000

careers_long = careers.loc[long].copy()
careers_long['HRrate'] = careers_long['HR'] / careers_long['AB']
careers_long['SOrate'] = careers_long['SO'] / careers_long['AB']
career_players = careers_long.index.values
career_names = getPlayerNames(career_players, master)
careers_long['Name'] = career_names
print(careers_long.head())

careers_cds = ColumnDataSource(careers_long)
careers_title = """Comparison of HR to K Rates for Long Careers"""
tooltip = [("Player", "@Name"),
           ("Career At Bats", "@AB"),
           ("Career Home Runs", "@HR"),
           ("Career Strikeouts", "@SO"),
           ("Home Run Rate", "@HRrate"),
           ("Strike Out Rate", "@SOrate")]
careers_fig = figure(background_fill_color='gray',
                     background_fill_alpha=0.5,
                     border_fill_color='blue',
                     border_fill_alpha=0.25,
                     plot_height=500,
                     plot_width=800,
                     h_symmetry=True,
                     x_axis_label='Home Run Rate',
                     x_axis_type='linear',
                     x_axis_location='below',
                     x_range=(0, 0.1),
                     y_axis_label='Strike Out Rate',
                     y_axis_type='linear',
                     y_axis_location='left',
                     y_range=(0, 0.4),
                     title=careers_title,
                     title_location='above',
                     tools='hover',
                     tooltips=tooltip,
                     toolbar_location=None)

careers_fig.circle('HRrate', 'SOrate', color='#CE1141', size=10, alpha=0.25,
                   source=careers_cds)

# Begin Hall of Fame Stolen Base fun.
players = ['Rickey Henderson', 'Lou Brock', 'Ty Cobb', 'Eddie Collins',
           'Max Carey', 'Joe Morgan', 'Luis Aparicio', 'Paul Molitor',
           'Roberto Alomar']
sb = [1406, 938, 897, 741, 738, 689, 506, 504, 474]
cs = [335, 307, 212, 195, 109, 162, 136, 131, 114]
games = [3081, 2616, 3034, 2826, 2476, 2649, 2599, 2683, 2379]

hofsb = pd.DataFrame(index=players,
                     columns=['SB', 'CS', 'Games'])
hofsb['SB'] = sb
hofsb['CS'] = cs
hofsb['Games'] = games
hofsb['Attempts'] = hofsb['SB'] + hofsb['CS']
hofsb['SuccessRate'] = round(hofsb['SB'] / hofsb['Attempts'], 4) * 100

hofsb['SBpG'] = round(hofsb['SB'] / hofsb['Games'], 3)
print(hofsb)

sb_cds = ColumnDataSource(hofsb)
tooltip = [("Player", "@index"),
           ("Career Stolen Bases", "@SB"),
           ("SB per Game", "@SBpG"),
           ("Success Rate", "@SuccessRate")]
sb_fig = figure(background_fill_color='gray',
                background_fill_alpha=0.5,
                border_fill_color='blue',
                border_fill_alpha=0.25,
                plot_height=500,
                plot_width=800,
                h_symmetry=True,
                x_axis_label='SB per Game',
                x_axis_type='linear',
                x_axis_location='below',
                x_range=(0, .5),
                y_axis_label='Success Rate',
                y_axis_type='linear',
                y_axis_location='left',
                y_range=(50, 100),
                title='Hall of Fame Stolen Base Comparisons',
                title_location='above',
                tools='hover',
                tooltips=tooltip,
                toolbar_location=None)

sb_fig.circle('SBpG', 'SuccessRate', color='#CE1141', size=10, alpha=0.25,
              source=sb_cds)

pitching = pd.read_csv('data/lehman/baseballdatabank-master/core/Pitching.csv')

pitching_gb = pitching.groupby('playerID').agg({'W': 'sum', 'L': 'sum',
                                                'SO': 'sum', 'BB': 'sum',
                                                'IPouts': 'sum',
                                                'yearID': 'median'})
criteria = pitching_gb['W'] >= 350
pitching_350 = pitching_gb.loc[criteria].copy()
last = ['Alexander', 'Clemens', 'Galvin', 'Johnson', 'Maddux', 'Mathewson',
        'Nichols', 'Spahn', 'Young']
pitching_350['LastName'] = last
pitching_350['WinPct'] = round(pitching_350['W'] / (pitching_350['W'] +
                                                    pitching_350['L']) * 100,
                               2)
pitching_350['SOBBRatio'] = round(pitching_350['SO'] / pitching_350['BB'], 2)

print(pitching_350)

win_350 = (pitching_350[['LastName', 'W', 'L', 'WinPct']]
           .sort_values('WinPct', ascending=False)
           .reset_index(drop=True))
print(win_350)

so_bb = pitching_350[['LastName', 'SO', 'BB', 'SOBBRatio']].copy()
criteria2 = so_bb['SOBBRatio'] >= 2.8
so_bb = so_bb.loc[criteria2].sort_values('BB').reset_index(drop=True)
print(so_bb)

criteria3 = pitching_gb['IPouts'] >= 10000
career10000 = pitching_gb.loc[criteria3].copy()
idlist = career10000.index.values
names = getPlayerNames(idlist, master)
career10000['Name'] = names
career10000['SOBBRatio'] = round(career10000['SO'] / career10000['BB'], 2)
career10000 = career10000.reset_index(drop=True)
print(career10000.head())

pitch10k_cds = ColumnDataSource(career10000)
tooltipp = [("Player", "@Name"),
            ("Career Strikeouts", "@SO"),
            ("Career Walks", "@BB")]
pitch10k_fig = figure(background_fill_color='gray',
                      background_fill_alpha=0.5,
                      border_fill_color='blue',
                      border_fill_alpha=0.25,
                      plot_height=500,
                      plot_width=800,
                      h_symmetry=True,
                      x_axis_label='Median Year of Career',
                      x_axis_type='linear',
                      x_axis_location='below',
                      x_range=(1870, 2018),
                      y_axis_label='SO / BB Ratio',
                      y_axis_type='linear',
                      y_axis_location='left',
                      y_range=(0, 8),
                      title="Long Career SO/BB Ratios",
                      title_location='above',
                      tools='hover',
                      tooltips=tooltipp,
                      toolbar_location=None)

pitch10k_fig.circle('yearID', 'SOBBRatio', color='#006BB6', size=10,
                    alpha=0.65, source=pitch10k_cds)

# Create display format here.
mantle_panel = Panel(child=mantle_fig, title='Mantle HR Rates')
career_panel = Panel(child=careers_fig, title='Long Career Rates')
sb_panel = Panel(child=sb_fig, title='Hall of Fame Stolen Bases')
pitch10k_panel = Panel(child=pitch10k_fig, title='Long Career SO/BB Rates')
tabs = Tabs(tabs=[mantle_panel, career_panel, sb_panel, pitch10k_panel])

show(tabs)
