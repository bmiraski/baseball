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

print(hofpitch.head())
print(hofpitch['WAR'].describe())

bfg = hofpitch.groupby('BFGroup')['Player'].count()
print(bfg)
warg = hofpitch.groupby('WARGroup')['Player'].count()
print(warg)

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

hofwar_fig.vbar(x=warlabels, width=0.9, top=warg, color='firebrick')

hofwar_panel = Panel(child=hofwar_fig, title='HOF Pitcher WAR')
hofbf_panel = Panel(child=hofbf_fig, title='HOF Batters Faced')
tabs = Tabs(tabs=[hofbf_panel, hofwar_panel])
show(tabs)
