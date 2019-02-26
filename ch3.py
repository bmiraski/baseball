"""Recreate Chapter 3 in Baseball in R."""

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
import pandas as pd

output_file('hof.html', title='HOF Batting Exercises')
curdoc().theme = Theme('baseball_theme.json')

hofbat = pd.read_csv('data/general/hofbatting.csv')

hofbat['MidCareer'] = (hofbat['From'] + hofbat['To']) / 2
hofbat['HRRate'] = round((hofbat['HR'] / hofbat['AB']), 4)
print(hofbat.head())

bins = [1800, 1900, 1919, 1941, 1960, 1976, 1993, 2050]
labels = ['19th Century', 'Dead Ball', 'Lively Ball', 'Integration',
          'Expansion', 'Free Agency', 'Long Ball']
eras = pd.cut(hofbat['MidCareer'], bins=bins, labels=labels)
hofbat['Era'] = eras


era_count = hofbat.groupby('Era')['Player'].count()
print(era_count)

hofbat_fig = figure(x_axis_label='Era',
                    x_range=labels,
                    y_axis_label='Number of Players',
                    y_axis_type='linear',
                    y_range=(0, 50),
                    title='Hall of Fame Batters by Era',
                    toolbar_location=None)

hofbat_fig.xaxis.major_label_orientation = math.pi/2

hofbat_fig.vbar(x=labels, width=0.9, top=era_count, color='firebrick')

hofbat_cds = ColumnDataSource(hofbat)

hofops_fig = figure(x_axis_label='OPS',
                    x_axis_type='linear',
                    x_range=(0.4, 1.2),
                    y_axis_type='linear',
                    y_range=(0, 2),
                    title='Hall of Fame Batters OPS',
                    toolbar_location=None)

hofops_fig.scatter(x='OPS', y=1, marker='circle', color='firebrick',
                   source=hofbat_cds, fill_alpha=0.5)

x = range(4, 12, 1)
opsbins = [item / 10 for item in x]
hofops = pd.cut(hofbat['OPS'], bins=opsbins)
print(hofops)
hofbat['OPSBIN'] = hofops
hof_opsbin = hofbat.groupby('OPSBIN')['Player'].count()
print(hof_opsbin)

x_range = [item / 100 for item in range(45, 115, 10)]
y_range = list(hof_opsbin.values)

hofbin_fig = figure(x_axis_label='OPS',
                    x_axis_type='linear',
                    y_axis_type='linear',
                    title='Hall of Fame Batters OPS',
                    toolbar_location=None)

hofbin_fig.vbar(x=x_range, top=y_range, width=0.09, color='blue')

tooltip = [("Player", "@Player"),
           ("OPS", "@OPS"),
           ("HR Rate", "@HRRate")]
hofmid_fig = figure(x_axis_label='Midpoint Year',
                    x_axis_type='linear',
                    y_axis_label='OPS',
                    y_axis_type='linear',
                    title='Hall of Fame Batters OPS',
                    tools='hover',
                    tooltips=tooltip,
                    toolbar_location=None)

hofmid_fig.circle(x='MidCareer', y='OPS', color='green', radius=1,
                  alpha=0.75, source=hofbat_cds)

obpslg_fig = figure(x_axis_label='On Base Percentage',
                    x_axis_type='linear',
                    x_range=(0.25, 0.5),
                    y_axis_label='Slugging Percentage',
                    y_axis_type='linear',
                    y_range=(0.28, 0.75),
                    title='Hall of Fame OPS Components',
                    tools='hover',
                    tooltips=tooltip,
                    toolbar_location=None)

obpslg_fig.circle(x='OBP', y='SLG', radius=0.0025, alpha=0.5, color='blue',
                  source=hofbat_cds)

slope7 = Slope(gradient=-1, y_intercept=0.7, line_color='orange',
               line_width=1)
slope8 = Slope(gradient=-1, y_intercept=0.8, line_color='red',
               line_width=1)
slope9 = Slope(gradient=-1, y_intercept=0.9, line_color='white',
               line_width=1)
slope10 = Slope(gradient=-1, y_intercept=1.0, line_color='green',
                line_width=1)

obpslg_fig.add_layout(slope7)
obpslg_fig.add_layout(slope8)
obpslg_fig.add_layout(slope9)
obpslg_fig.add_layout(slope10)

erahrr_fig = figure(x_axis_label='Home Run Rate',
                    x_axis_type='linear',
                    x_range=(0, 0.09),
                    y_axis_label='Era',
                    y_range=labels,
                    title='Home Run Rates by Era',
                    tools='hover',
                    tooltips=tooltip,
                    toolbar_location=None)

erahrr_fig.circle('HRRate', 'Era', radius=0.0005, color='blue',
                  source=hofbat_cds)

erahrr_panel = Panel(child=erahrr_fig, title='Home Run Rate by Era')
obpslg_panel = Panel(child=obpslg_fig, title='HOF OBP vs. SLG')
hofmid_panel = Panel(child=hofmid_fig, title='Career OPS HOF')
hofbin_panel = Panel(child=hofbin_fig, title='HOF OPS Distribution')
hofbat_panel = Panel(child=hofbat_fig, title='HOF Batters by Era')
hofops_panel = Panel(child=hofops_fig, title='HOF Batters OPS')
tabs = Tabs(tabs=[hofbat_panel, hofops_panel, hofbin_panel, hofmid_panel,
                  obpslg_panel, erahrr_panel])
show(tabs)
