"""Follow along with some additional data exercises."""

from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.models import ColumnDataSource, Label, Span
from bokeh.models.widgets import Tabs, Panel
from bokeh.models.tickers import FixedTicker

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

mantle_panel = Panel(child=mantle_fig, title='Mantle HR Rates')
career_panel = Panel(child=careers_fig, title='Long Career Rates')
tabs = Tabs(tabs=[mantle_panel, career_panel])

show(tabs)
