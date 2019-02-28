"""Recreate Exercises in Chapter 3 in Baseball in R."""

from bokeh.io import curdoc
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.models import Slope
from bokeh.models.widgets import Panel
from bokeh.models.widgets import Tabs
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.themes import Theme
import math
import numpy as np
import pandas as pd

output_file('ch3ex.html', title='HOF Pitching Exercises')
curdoc().theme = Theme('baseball_theme.json')
hofpitch = pd.read_csv('data/general/hofpitching.csv')

bins = [0, 10000, 15000, 20000, 30000]
labels = ['Less than 10,000', '10,000 - 15,000', '15,000 - 20,000',
          'More than 20,000']
warbins = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 200]
warlabels = ['Less than 20', '20 - 30', '30 - 40', '40 - 50',
             '50 - 60', '60 - 70', '70 - 80', '80 - 90', '90 - 100',
             '100 - 110', '110 - 120', '120 - 130', '130 - 140',
             'More than 140']

hofpitch['BFGroup'] = pd.cut(hofpitch['BF'], bins=bins, labels=labels)
hofpitch['WARGroup'] = pd.cut(hofpitch['WAR'], bins=warbins, labels=warlabels)
hofpitch['WAR/Yr'] = hofpitch['WAR'] / hofpitch['Yrs']
hofpitch['MidCareer'] = (hofpitch['From'] + hofpitch['To']) / 2
hofpitch['Player'] = hofpitch['Player'].str[:-4]

print(hofpitch.head())
print(hofpitch['WAR'].describe())

bfg = hofpitch.groupby('BFGroup')['Player'].count()
print(bfg)
warg = hofpitch.groupby('WARGroup')['Player'].count()
print(warg)

mid60 = hofpitch['MidCareer'] >= 1960
hofp1960 = hofpitch.loc[mid60].copy().sort_values('WAR/Yr')

hofbf_fig = figure(x_axis_label='Batters Faced',
                   x_range=labels,
                   y_axis_label='Number of Players',
                   y_axis_type='linear',
                   y_range=(5, 30),
                   title='Hall of Fame Batters Faced',
                   toolbar_location=None)

hofbf_fig.xaxis.major_label_orientation = math.pi/2

hofbf_fig.vbar(x=labels, width=0.9, top=bfg, color='firebrick')

hofwar_fig = figure(x_axis_label='WAR',
                    x_range=warlabels,
                    y_axis_label='Number of Players',
                    y_axis_type='linear',
                    y_range=(0, 20),
                    title='Hall of Fame Pitchers by WAR',
                    toolbar_location=None)

hofwar_fig.xaxis.major_label_orientation = math.pi/2

hofwar_fig.vbar(x=warlabels, width=0.9, top=warg, color='#1D4E8F')

hofpitch_cds = ColumnDataSource(hofpitch)
tooltip = [("Player", "@Player")]

waryr_fig = figure(x_axis_label='WAR Per Year',
                   x_range=(0, 8),
                   y_axis_label='Batters Faced',
                   y_range=labels,
                   title='WAR Per Year vs. Batters Faced for HOFers',
                   tools='hover',
                   tooltips=tooltip,
                   toolbar_location=None)

waryr_fig.circle(x='WAR/Yr', y='BFGroup', radius=.15, alpha=0.5,
                 color='#6140cf', source=hofpitch_cds)

p60_cds = ColumnDataSource(hofp1960)
players = hofp1960['Player'].to_list()
p60_fig = figure(x_axis_label='WAR Per Year',
                 x_range=(0, 6),
                 y_axis_label='Pitcher',
                 y_range=players,
                 title='Pitcher WAR per Year, post 1960',
                 toolbar_location=None)

p60_fig.circle(x='WAR/Yr', y='Player', radius=.08, alpha=0.9,
               color='#de9a16', source=p60_cds)

midwar_fig = figure(x_axis_label='Midyear of Career',
                    x_range=(1870, 1990),
                    y_axis_label='WAR per Year',
                    y_range=(0, 8),
                    title='WAR Per Year by MidCareer',
                    tools='hover',
                    tooltips=tooltip,
                    toolbar_location=None)

midwar_fig.circle(x='MidCareer', y='WAR/Yr', radius=1, alpha=0.6,
                  color='#aa167e', source=hofpitch_cds)

midwar_panel = Panel(child=midwar_fig, title='MidCareer WAR')
p60_panel = Panel(child=p60_fig, title="Post '60 WAR/Yr")
waryr_panel = Panel(child=waryr_fig, title='WAR/Yr vs. Batters Faced')
hofwar_panel = Panel(child=hofwar_fig, title='HOF Pitcher WAR')
hofbf_panel = Panel(child=hofbf_fig, title='HOF Batters Faced')
tabs = Tabs(tabs=[hofbf_panel, hofwar_panel, waryr_panel, p60_panel,
                  midwar_panel])
show(tabs)
