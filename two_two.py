"""Working with some additional pitching and SB data."""

from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.plotting import show

import pandas as pd


def getPlayerNames(idlist, masterdf):
    """Retrieve the full player names from the Master Data file."""
    player_names = []
    for player in idlist:
        name = (str(masterdf.loc[player].nameFirst) + " " +
                str(masterdf.loc[player].nameLast))
        player_names.append(name)
    return player_names


output_file('sb300.html')
master = pd.read_csv('data/lehman/baseballdatabank-master/core/Master.csv',
                     index_col='playerID')

outcomes = ['Single', 'Out', 'Out', 'Single', 'Double', 'Out', 'Walk',
            'Out', 'Single']

outcome_df = pd.DataFrame()
outcome_df['outcome'] = outcomes
gtob = ['Out', 'Walk', 'Single', 'Double']
outcome_df['outcome'] = pd.Categorical(outcome_df['outcome'], categories=gtob,
                                       ordered=True)

out_gb = outcome_df.groupby('outcome').agg('size')

# print(out_gb)

pitching = pd.read_csv('data/lehman/baseballdatabank-master/core/Pitching.csv')

pitching_gb = pitching.groupby('playerID').agg({'W': 'sum', 'L': 'sum',
                                                'SO': 'sum', 'BB': 'sum',
                                                'IPouts': 'sum',
                                                'yearID': 'median'})
criteria = pitching_gb['W'] >= 350
pitching_350 = pitching_gb.loc[criteria].copy()
last = ['Alexander', 'Clemens', 'Galvin', 'Johnson', 'Maddux', 'Mathewson',
        'Nichols', 'Spahn', 'Young']
pitching_350['LastName'] = last
pitching_350['WinPct'] = round(pitching_350['W'] / (pitching_350['W'] +
                                                    pitching_350['L']) * 100,
                               2)
pitching_350['SOBBRatio'] = round(pitching_350['SO'] / pitching_350['BB'], 2)

print(pitching_350)

win_350 = (pitching_350[['LastName', 'W', 'L', 'WinPct']]
           .sort_values('WinPct', ascending=False)
           .reset_index(drop=True))
print(win_350)

so_bb = pitching_350[['LastName', 'SO', 'BB', 'SOBBRatio']].copy()
criteria2 = so_bb['SOBBRatio'] >= 2.8
so_bb = so_bb.loc[criteria2].sort_values('BB').reset_index(drop=True)
print(so_bb)

batting = pd.read_csv('data/lehman/baseballdatabank-master/core/Batting.csv')
batting_gb = batting.groupby('playerID').agg({'SB': 'sum', 'CS': 'sum',
                                              'G': 'sum', 'yearID': 'min'})
sbcriteria1 = batting_gb['SB'] >= 300
sbcriteria2 = batting_gb['CS'] > 0
sbcriteria3 = batting_gb['yearID'] >= 1951
total_criteria = sbcriteria1 & sbcriteria2 & sbcriteria3
sb300 = batting_gb.loc[total_criteria].copy()
sbnames = sb300.index.values
sb300.insert(loc=0, column='Name', value=getPlayerNames(sbnames, master))
sb300['Attempts'] = sb300['SB'] + sb300['CS']
sb300['SBPct'] = round((sb300['SB'] / sb300['Attempts']) * 100, 2)
sb300['SBpG'] = round(sb300['SB'] / sb300['G'], 3)

print(sb300.head())

sb_cds = ColumnDataSource(sb300)
tooltip = [("Player", "@Name"),
           ("Career Stolen Bases", "@SB"),
           ("SB per Game", "@SBpG"),
           ("Success Rate", "@SBPct")]
sb_fig = figure(background_fill_color='gray',
                background_fill_alpha=0.5,
                border_fill_color='blue',
                border_fill_alpha=0.25,
                plot_height=500,
                plot_width=800,
                h_symmetry=True,
                x_axis_label='SB per Game',
                x_axis_type='linear',
                x_axis_location='below',
                x_range=(0, .5),
                y_axis_label='Success Rate',
                y_axis_type='linear',
                y_axis_location='left',
                y_range=(50, 100),
                title='Stolen Base Comparisons',
                title_location='above',
                tools='hover',
                tooltips=tooltip,
                toolbar_location=None)

sb_fig.circle('SBpG', 'SBPct', color='#CE1141', size=10, alpha=0.25,
              source=sb_cds)

# show(sb_fig)

carewcrit1 = batting_gb['yearID'] >= 1960
carewcrit2 = batting_gb['yearID'] < 1981
carewcrit = carewcrit1 & carewcrit2

carew = batting_gb.loc[carewcrit].copy()
cwnames = carew.index.values
carew.insert(loc=0, column='Name', value=getPlayerNames(cwnames, master))
carew['Attempts'] = carew['SB'] + carew['CS']
carew['SBPct'] = round((carew['SB'] / carew['Attempts']) * 100, 2)
carew['SBpG'] = round(carew['SB'] / carew['G'], 3)
carew = carew.dropna()
carewcrit3 = carew['Attempts'] >= 200
carew = carew.loc[carewcrit3]

print(carew)
print(carew['SBPct'].describe())
# Output shows how bad Carew was at stealing bases compared to his peers.
carew.to_excel('carew.xlsx')
