"""Determine Bonds data."""

from bokeh.core.properties import value
from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.models import ColumnDataSource, Label
from bokeh.models import Span
# from bokeh.models.widgets import Panel
# from bokeh.models.widgets import Tabs

import math
import pandas as pd


def classify_ibb(df):
    """Separate intentional walks by base state."""
    df_ibb = df[df['EVENT_CD'] == 15]

    not_first = df_ibb.BASE1_RUN_ID.isna()
    not_second = df_ibb.BASE2_RUN_ID.isna()
    not_third = df_ibb.BASE3_RUN_ID.isna()

    empty = not_first & not_second & not_third
    first = ~not_first & not_second & not_third
    second = not_first & ~not_second & not_third
    third = not_first & not_second & ~not_third
    firstsecond = ~not_first & ~not_second & not_third
    secondthird = not_first & ~not_second & ~not_third
    firstthird = ~not_first & not_second & ~not_third
    full = ~not_first & ~not_second & ~not_third

    empty_ibb = df_ibb[empty]
    first_ibb = df_ibb[first]
    second_ibb = df_ibb[second]
    third_ibb = df_ibb[third]
    firstsecond_ibb = df_ibb[firstsecond]
    secondthird_ibb = df_ibb[secondthird]
    firstthird_ibb = df_ibb[firstthird]
    full_ibb = df_ibb[full]

    walk_set = [len(empty_ibb), len(first_ibb), len(second_ibb),
                len(third_ibb), len(firstsecond_ibb), len(secondthird_ibb),
                len(firstthird_ibb), len(full_ibb)]

    return walk_set


output_file('bonds.html')

ohone = pd.read_csv('data/retrosheet/allevent2001.csv', index_col='BAT_ID')
bonds2001 = ohone.loc['bondb001']

ibb_2001 = classify_ibb(bonds2001)
print(ibb_2001)

ohtwo = pd.read_csv('data/retrosheet/allevent2002.csv', index_col='BAT_ID')
bonds2002 = ohtwo.loc['bondb001']

ibb_2002 = classify_ibb(bonds2002)
print(ibb_2002)

ohthree = pd.read_csv('data/retrosheet/allevent2003.csv', index_col='BAT_ID')
bonds2003 = ohthree.loc['bondb001']

ibb_2003 = classify_ibb(bonds2003)
print(ibb_2003)

ohfour = pd.read_csv('data/retrosheet/allevent2004.csv', index_col='BAT_ID')
bonds2004 = ohfour.loc['bondb001']

ibb_2004 = classify_ibb(bonds2004)
print(ibb_2004)

x_label = ['Empty', 'First', 'Second', 'Third', 'First & Second',
           'Second & Third', 'First & Third', 'Bases Loaded']
years = ['2001', '2002', '2003', '2004']
colors = ['#006BB6', '#CE1141', '#00FF00', '#FFA500']

data = {'bases': x_label,
        '2001': ibb_2001,
        '2002': ibb_2002,
        '2003': ibb_2003,
        '2004': ibb_2004}

bonds_fig = figure(background_fill_color='gray',
                   background_fill_alpha=0.5,
                   border_fill_color='blue',
                   border_fill_alpha=0.25,
                   plot_height=500,
                   plot_width=800,
                   h_symmetry=True,
                   x_axis_label='Runners On',
                   x_axis_location='below',
                   x_range=x_label,
                   y_axis_label='Intentional Walks',
                   y_axis_type='linear',
                   y_axis_location='left',
                   y_range=(0, 130),
                   title='Barry Bonds Intentional Walks, 2001 - 2004',
                   title_location='above',
                   toolbar_location=None)

bonds_fig.xaxis.major_label_orientation = math.pi/2

bonds_fig.vbar_stack(years, x='bases', width=0.9, color=colors,
                     source=data, legend=[value(x) for x in years])

bonds_fig.legend.location = 'top_right'

show(bonds_fig)
