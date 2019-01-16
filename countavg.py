"""Determine Batting Average by count."""

from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.plotting import show

import math
import pandas as pd


def get_averages(dataframe):
    """Determine averages by count."""
    counts = ['0-0', '0-1', '0-2', '1-0', '1-1', '1-2', '2-0', '2-1', '2-2',
              '3-0', '3-1', '3-2']
    hits = [20, 21, 22, 23]
    averages = []
    for count in counts:
        print(count)
        ab = dataframe.loc[count]
        ab_num = len(ab)
        print(ab_num)
        ab_hit = ab.EVENT_CD.isin(hits)
        hit = len(ab[ab_hit])
        print(hit)
        average = round(hit / ab_num, 3)
        print(average)
        averages.append(average)
    return(averages)


output_file('avgcount.html')
data = pd.read_csv('data/retrosheet/allevent2018.csv')

counts = ['0-0', '0-1', '0-2', '1-0', '1-1', '1-2', '2-0', '2-1', '2-2',
          '3-0', '3-1', '3-2']

data['B_STR'] = data['BALLS_CT'].astype('str')
data['S_STR'] = data['STRIKES_CT'].astype('str')

columns = ['GAME_ID', 'AB_FL', 'B_STR', 'S_STR', 'EVENT_CD']
data_small = data.loc[:, columns]

count = data_small.B_STR.str.cat(data_small['S_STR'], sep='-')
data_small['COUNT'] = count
data_by_count = data_small.set_index('COUNT')

ab_event = data_by_count.AB_FL == 'T'
data_ab = data_by_count[ab_event]

averages = get_averages(data_ab)
print(averages)

average_fig = figure(background_fill_color='gray',
                     background_fill_alpha=0.5,
                     border_fill_color='blue',
                     border_fill_alpha=0.25,
                     plot_height=500,
                     plot_width=800,
                     h_symmetry=True,
                     x_axis_label='Count',
                     x_axis_location='below',
                     x_range=counts,
                     y_axis_label='Batting Average',
                     y_axis_type='linear',
                     y_axis_location='left',
                     y_range=(0, .4),
                     title='Batting Average by Count',
                     title_location='above',
                     toolbar_location=None)

average_fig.xaxis.major_label_orientation = math.pi/2

average_fig.line(x=counts, y=averages, color='#116BB6')

show(average_fig)
