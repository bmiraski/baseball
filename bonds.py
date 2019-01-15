"""Determine Bonds data."""

from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.models import ColumnDataSource, Label
from bokeh.models import Span
# from bokeh.models.widgets import Panel
# from bokeh.models.widgets import Tabs

import math
import pandas as pd

output_file('bonds.html')

# ohone = pd.read_csv('data/retrosheet/allevent2001.csv', index_col='BAT_ID')
# bonds2001 = ohone.loc['bondb001']

# bonds2001_ibb = bonds2001[bonds2001['EVENT_CD'] == 15]

# not_first = bonds2001_ibb.BASE1_RUN_ID.isna()
# not_second = bonds2001_ibb.BASE2_RUN_ID.isna()
# not_third = bonds2001_ibb.BASE3_RUN_ID.isna()

# empty = not_first & not_second & not_third
# full = ~not_first & ~not_second & ~not_third

# empty_ibb = bonds2001_ibb[empty]
# full_ibb = bonds2001_ibb[full]

# print(len(empty_ibb), len(full_ibb))

ohfour = pd.read_csv('data/retrosheet/allevent2004.csv', index_col='BAT_ID')
bonds2004 = ohfour.loc['bondb001']

bonds2004_ibb = bonds2004[bonds2004['EVENT_CD'] == 15]

not_first = bonds2004_ibb.BASE1_RUN_ID.isna()
not_second = bonds2004_ibb.BASE2_RUN_ID.isna()
not_third = bonds2004_ibb.BASE3_RUN_ID.isna()

empty = not_first & not_second & not_third
first = ~not_first & not_second & not_third
second = not_first & ~not_second & not_third
third = not_first & not_second & ~not_third
firstsecond = ~not_first & ~not_second & not_third
secondthird = not_first & ~not_second & ~not_third
firstthird = ~not_first & not_second & ~not_third
full = ~not_first & ~not_second & ~not_third


empty_ibb = bonds2004_ibb[empty]
first_ibb = bonds2004_ibb[first]
second_ibb = bonds2004_ibb[second]
third_ibb = bonds2004_ibb[third]
firstsecond_ibb = bonds2004_ibb[firstsecond]
secondthird_ibb = bonds2004_ibb[secondthird]
firstthird_ibb = bonds2004_ibb[firstthird]
full_ibb = bonds2004_ibb[full]

x_label = ['Empty', 'First', 'Second', 'Third', 'First & Second',
           'Second & Third', 'First & Third', 'Bases Loaded']

top_values = [len(empty_ibb), len(first_ibb), len(second_ibb),
              len(third_ibb), len(firstsecond_ibb), len(secondthird_ibb),
              len(firstthird_ibb), len(full_ibb)]

print(top_values)

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
                   y_range=(0, 55),
                   title='Barry Bonds Intentional Walks, 2004',
                   title_location='above',
                   toolbar_location=None)

bonds_fig.xaxis.major_label_orientation = math.pi/2

bonds_fig.vbar(x=x_label, top=top_values, fill_color='#FFA500', width=0.9)

show(bonds_fig)
