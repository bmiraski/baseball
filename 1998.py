"""Track 1998 HR battle."""

from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Label, Span
from bokeh.models.widgets import Tabs, Panel
from bokeh.models.tickers import FixedTicker

import math
import pandas as pd

output_file('chapter1_3.html')

event1998 = pd.read_csv('data/retrosheet/unzipped/1998eve/all1998.csv')
event1998['GAME_DATE'] = event1998['GAME_ID'].str.slice(3, 11)
event1998['GAME_DATE'] = pd.to_datetime(event1998['GAME_DATE'],
                                        infer_datetime_format=True)

# print(event1998.head())
# print(event1998.tail())

sosa = event1998[event1998['BAT_ID'] == 'sosas001']
sosa = sosa.sort_values(['GAME_DATE', 'EVENT_ID'])
sosa_hr = sosa[sosa['EVENT_CD'] == 23]
sosa_hr['CUM'] = list(range(1, 67))

# print(sosa.head())
# print(sosa.tail())

# print(sosa_hr)

mcgwire = event1998[event1998['BAT_ID'] == 'mcgwm001']
mcgwire = mcgwire.sort_values(['GAME_DATE', 'EVENT_ID'])
mcgwire_hr = mcgwire[mcgwire['EVENT_CD'] == 23]
mcgwire_hr['CUM'] = list(range(1, 71))

# print(mcgwire_hr)

hr_figure = figure(background_fill_color='gray',
                   background_fill_alpha=0.5,
                   border_fill_color='blue',
                   border_fill_alpha=0.25,
                   plot_height=500,
                   plot_width=800,
                   h_symmetry=True,
                   x_axis_label='Date',
                   x_axis_type='datetime',
                   x_axis_location='below',
                   y_axis_label='Season HR',
                   y_axis_type='linear',
                   y_axis_location='left',
                   y_range=(0, 72),
                   title='1998 HR Chase',
                   title_location='above',
                   toolbar_location=None)

hr_figure.xaxis.major_label_orientation = math.pi/4
maris = Span(location=61, dimension='width', line_color='green',
             line_dash='dashed', line_width=3)

hr_figure.add_layout(maris)

ss_cds = ColumnDataSource(sosa_hr)
mm_cds = ColumnDataSource(mcgwire_hr)

hr_figure.step('GAME_DATE', 'CUM', color='#006BB6',
               legend='Sammy Sosa', source=ss_cds)
hr_figure.step('GAME_DATE', 'CUM', color='#CE1141',
               legend='Mark McGwire', source=mm_cds)

hr_figure.legend.location = 'bottom_right'


show(hr_figure)
