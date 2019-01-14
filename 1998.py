"""Track 1998 HR battle."""

from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Label, Span
from bokeh.models.widgets import Tabs, Panel
from bokeh.models.tickers import FixedTicker

import math
import pandas as pd

output_file('1998.html')

# Read in Retrosheet data from 1998, and add GameDate col as a datetime.
event1998 = pd.read_csv('data/retrosheet/unzipped/1998eve/all1998.csv')
event1998['GAME_DATE'] = event1998['GAME_ID'].str.slice(3, 11)
event1998['GAME_DATE'] = pd.to_datetime(event1998['GAME_DATE'],
                                        infer_datetime_format=True)
event1998 = event1998.set_index('BAT_ID')
event1998_sorted = event1998.sort_index()
print(event1998_sorted.head())


# Extract Sosa/McGwire data and narrow to only HR events. Number events.

sosa = event1998_sorted.loc['sosas001']
sosa = sosa.sort_values(['GAME_DATE', 'EVENT_ID'])
sshr = sosa.EVENT_CD == 23
sosa_hr = sosa[sshr]
sosa_hr.loc[:, 'CUM'] = list(range(1, 67))

mcgwire = event1998_sorted.loc['mcgwm001']
mcgwire = mcgwire.sort_values(['GAME_DATE', 'EVENT_ID'])
mmhr = mcgwire.EVENT_CD == 23
mcgwire_hr = mcgwire[mmhr]
mcgwire_hr.loc[:, 'CUM'] = list(range(1, 71))

# Create graph of results. Maris line sits at 61.
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

# Determine who was better with runners on
ss_first = sosa_hr.BASE1_RUN_ID.isna()
ss_second = sosa_hr.BASE2_RUN_ID.isna()
ss_third = sosa_hr.BASE3_RUN_ID.isna()
ss_empty = ss_first & ss_second & ss_third
ss_runner = ~ss_empty

mm_first = mcgwire_hr.BASE1_RUN_ID.isna()
mm_second = mcgwire_hr.BASE2_RUN_ID.isna()
mm_third = mcgwire_hr.BASE3_RUN_ID.isna()
mm_empty = mm_first & mm_second & mm_third
mm_runner = ~mm_empty

sosa_empty = sosa_hr[ss_empty]
sosa_runner = sosa_hr[ss_runner]
mcgwire_empty = mcgwire_hr[mm_empty]
mcgwire_runner = mcgwire_hr[mm_runner]

print(len(sosa_empty), len(sosa_runner), len(mcgwire_empty),
      len(mcgwire_runner))

x_labels = ['Sosa Empty', 'McGwire Empty', 'Sosa Runners On',
            'McGwire Runners On']

runners_fig = figure(background_fill_color='gray',
                     background_fill_alpha=0.5,
                     border_fill_color='blue',
                     border_fill_alpha=0.25,
                     plot_height=500,
                     plot_width=800,
                     h_symmetry=True,
                     x_axis_location='below',
                     x_range=x_labels,
                     y_axis_label='Home Runs',
                     y_axis_type='linear',
                     y_axis_location='left',
                     y_range=(25, 40),
                     title='Home Run Runners On vs. Empty',
                     title_location='above',
                     toolbar_location=None)

runners_fig.xaxis.major_label_orientation = math.pi/2
top_values = [len(sosa_empty), len(mcgwire_empty), len(sosa_runner),
              len(mcgwire_runner)]
      
runners_fig.vbar(x=x_labels, top=top_values,
                 fill_color=['#006BB6', '#CE1141', '#006BB6', '#CE1141'],
                 width=0.9)

race_panel = Panel(child=hr_figure, title='Home Run Race')
runner_panel = Panel(child=runners_fig, title='Runners on vs. Empty')
tabs = Tabs(tabs=[race_panel, runner_panel])

show(tabs)
