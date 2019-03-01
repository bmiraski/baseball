"""Solve Chapter 1 Lehman of Analyzing Baseball in R, in python."""

from bokeh.io import curdoc
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.models import Label
from bokeh.models import Span
from bokeh.models.tickers import FixedTicker
from bokeh.models.widgets import Panel
from bokeh.models.widgets import Tabs
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.themes import Theme
import math
import pandas as pd


output_file('chapter1_2.html', title='Lehman Data Set Exercises')
curdoc().theme = Theme('baseball_theme.json')
master = pd.read_csv('data/lehman/baseballdatabank-master/core/Master.csv',
                     index_col='playerID')
# Begin Home Run Chase reproduction


def addAges(df):
    """Calculate and add player age to dataframe."""
    playerid = df.index[0]
    birthyear = master.loc[playerid].birthYear
    birthmonth = master.loc[playerid].birthMonth
    if birthmonth >= 7:
        birthyear += 1
    df['Age'] = df['yearID'] - birthyear
    return df


batting = pd.read_csv('data/lehman/baseballdatabank-master/core/Batting.csv',
                      index_col='playerID')

ruth = batting.loc['ruthba01'].copy()
aaron = batting.loc['aaronha01'].copy()
bonds = batting.loc['bondsba01'].copy()
arod = batting.loc['rodrial01'].copy()
pujols = batting.loc['pujolal01'].copy()

ruth = addAges(ruth)
aaron = addAges(aaron)
bonds = addAges(bonds)
arod = addAges(arod)
pujols = addAges(pujols)

# Add cumulative HR column. Changed to use pandas builtin function
ruth['Cumulative HR'] = ruth['HR'].cumsum()
aaron['Cumulative HR'] = aaron['HR'].cumsum()
bonds['Cumulative HR'] = bonds['HR'].cumsum()
arod['Cumulative HR'] = arod['HR'].cumsum()
pujols['Cumulative HR'] = pujols['HR'].cumsum()

hr_king = figure(x_axis_label='Age',
                 x_axis_type='linear',
                 x_range=(16, 43),
                 y_axis_label='Career HR',
                 y_axis_type='linear',
                 y_range=(0, 775),
                 title='Race to be the Home Run King',
                 toolbar_location=None)

hr_king.xaxis.major_label_orientation = math.pi/4

ruth_cds = ColumnDataSource(ruth)
aaron_cds = ColumnDataSource(aaron)
bonds_cds = ColumnDataSource(bonds)
arod_cds = ColumnDataSource(arod)
pujols_cds = ColumnDataSource(pujols)

hr_king.line('Age', 'Cumulative HR', color='#000000',
             legend='Babe Ruth', source=ruth_cds)
hr_king.line('Age', 'Cumulative HR', color='#006BB6',
             legend='Hank Aaron', source=aaron_cds)
hr_king.line('Age', 'Cumulative HR', color='#FFA500',
             legend='Barry Bonds', source=bonds_cds)
hr_king.line('Age', 'Cumulative HR', color='#CE1141',
             legend='Alex Rodriguez', source=arod_cds)
hr_king.line('Age', 'Cumulative HR', color='green',
             legend='Albert Pujols', source=pujols_cds)

hr_king.legend.location = 'bottom_right'

# Begin Question #1 solution

fig = figure(x_axis_label='Decade',
             x_axis_type='linear',
             x_range=(1860, 2020),
             y_axis_label='Rate',
             y_axis_type='linear',
             y_range=(0, 20),
             title='Rate of HR and SO per game by Decade',
             toolbar_location=None)

# Make the x-axis look a little nicer.
fig.xaxis.ticker = FixedTicker(ticks=list(range(1860, 2030, 10)))
fig.xaxis.major_label_orientation = math.pi/4


teams = pd.read_csv('data/lehman/baseballdatabank-master/core/Teams.csv')

# Cast yearID to a Float to facilitate math
teams['yearID'] = teams['yearID'].astype(float)

# Use yearID to determine Decade.
years = teams['yearID']

decades = []
for year in years:
    dec = math.floor(year / 10) * 10
    decades.append(dec)

teams['decade'] = decades

# Cast yearID back to integer
teams['yearID'] = teams['yearID'].astype(int)

hr_data = teams.groupby('decade').agg({'G': 'sum', 'HR': 'sum', 'SO': 'sum'})

hr_data['G'] = hr_data['G'] / 2  # divide by 2 to not double count games
hr_data['HR Rate'] = hr_data['HR'] / hr_data['G']
hr_data['SO Rate'] = hr_data['SO'] / hr_data['G']

hr_cds = ColumnDataSource(hr_data)

fig.line('decade', 'HR Rate',
         color='#CE1141', legend='Home Run Rate',
         source=hr_cds)
fig.line('decade', 'SO Rate',
         color='#006BB6', legend='Strikeout Rate',
         source=hr_cds)

fig.legend.location = 'top_left'

print(hr_data)

# Begin solution to analyzing effect of DH on run scoring.

al_data = teams[teams['lgID'] == 'AL']
al_data = al_data.groupby('yearID').agg({'G': 'sum', 'R': 'sum'})
al_data['R per G'] = al_data['R'] / al_data['G']
# Note this is runs per team per game. Important for interleague play.

nl_data = teams[teams['lgID'] == 'NL']
nl_data = nl_data.groupby('yearID').agg({'G': 'sum', 'R': 'sum'})
nl_data['R per G'] = nl_data['R'] / nl_data['G']

run_data = figure(x_axis_label='Year',
                  x_axis_type='linear',
                  x_range=(1870, 2020),
                  y_axis_label='Runs per Team per Game',
                  y_axis_type='linear',
                  y_range=(2, 8),
                  title='Average Runs Scored per Game by Team, AL vs. NL',
                  toolbar_location=None)

run_data.xaxis.major_label_orientation = math.pi/4

al_cds = ColumnDataSource(al_data)
nl_cds = ColumnDataSource(nl_data)

run_data.line('yearID', 'R per G',
              color='#CE1141', legend='American League',
              source=al_cds)
run_data.line('yearID', 'R per G',
              color='#006BB6', legend='National League',
              source=nl_cds)

dh = Span(location=1973, dimension='height', line_color='green',
          line_dash='dashed', line_width=3)
dh_label = Label(angle=90, angle_units='deg', text='DH Starts', x=1972,
                 x_offset=3, y=6)

run_data.add_layout(dh)
run_data.add_layout(dh_label)

# Begin starting pitcher question

pitch = pd.read_csv('data/lehman/baseballdatabank-master/core/Pitching.csv')

start_pitch = pitch[pitch['GS'] > 0]

start_pitch = start_pitch.groupby('yearID').agg({'GS': 'sum', 'CG': 'sum'})

start_pitch['CG Pct'] = start_pitch['CG'] / start_pitch['GS']

print(start_pitch.head())
print(start_pitch.tail())

pitch_fig = figure(x_axis_label='Year',
                   x_axis_type='linear',
                   x_range=(1870, 2020),
                   y_axis_label='Complete Game Percentage',
                   y_axis_type='linear',
                   y_range=(0, 1),
                   title='Percentage of games completed by starters per Year',
                   toolbar_location=None)

pitch_fig.xaxis.major_label_orientation = math.pi/4

pitch_cds = ColumnDataSource(start_pitch)

pitch_fig.line('yearID', 'CG Pct', color='#006BB6', source=pitch_cds)

# Begin graphing panels

king_panel = Panel(child=hr_king, title='Home Run King')
hr_panel = Panel(child=fig, title='HR and SO by decade')
run_panel = Panel(child=run_data, title='Run Scoring by League')
start_panel = Panel(child=pitch_fig, title='Complete Game Percentage')
tabs = Tabs(tabs=[king_panel, hr_panel, run_panel, start_panel])

show(tabs)
