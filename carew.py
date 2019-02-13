"""Determine the RE24 impact of a player's basestealing."""

from collections import defaultdict
from itertools import repeat
import pandas as pd


def calc_values(states):
    """Determine RE24 value from a base state / out situation.

    State tuple passed in should have the following arguements in this
    order: outs, base state, year, runs on play. rRuns on play should be
    0 for the starting state.
    """
    values = []
    for x in range(len(states)):
        if states[x][2] in range(1950, 1969):
            valuedf = base_value_1968
        elif states[x][2] in range(1969, 1993):
            valuedf = base_value_1992
        elif states[x][2] in range(1993, 2010):
            valuedf = base_value_2009
        elif states[x][2] in range(2010, 2016):
            valuedf = base_value_2015
        else:
            valuedf = base_value_2018

        if states[x][0] == 3:
            value = 0
        else:
            value = (round(valuedf.iloc[states[x][1], states[x][0]], 3) +
                     states[x][3])
        values.append(value)
    return values


columns = ['GAME_ID', 'OUTS_CT', 'EVENT_CD', 'EVENT_OUTS_CT', 'BASE1_RUN_ID',
           'BASE2_RUN_ID', 'BASE3_RUN_ID', 'RUN1_SB_FL', 'RUN2_SB_FL',
           'RUN3_SB_FL', 'RUN1_CS_FL', 'RUN2_CS_FL', 'RUN3_CS_FL',
           'RUN1_PK_FL', 'RUN2_PK_FL', 'RUN3_PK_FL', 'START_BASES_CD',
           'END_BASES_CD', 'EVENT_RUNS_CT']

base_value_2018 = pd.read_csv('data/general/base_state_neutral415.csv')
base_value_1968 = pd.read_csv('data/general/base_state_1968.csv')
base_value_1992 = pd.read_csv('data/general/base_state_1992.csv')
base_value_2009 = pd.read_csv('data/general/base_state_2009.csv')
base_value_2015 = pd.read_csv('data/general/base_state_2015.csv')
data1950 = pd.read_csv('data/retrosheet/allevent1950s.csv', usecols=columns)
data1960 = pd.read_csv('data/retrosheet/allevent1960s.csv', usecols=columns)
data1970 = pd.read_csv('data/retrosheet/allevent1970s.csv', usecols=columns)
data1980 = pd.read_csv('data/retrosheet/allevent1980s.csv', usecols=columns)
data1990 = pd.read_csv('data/retrosheet/allevent1990s.csv', usecols=columns)
data2000 = pd.read_csv('data/retrosheet/allevent2000s.csv', usecols=columns)

data = pd.concat([data1950, data1960, data1970, data1980,
                  data1990, data2000], ignore_index=True)
print(data.head())

gameids = data['GAME_ID'].to_list()
years = []
for item in gameids:
    year = int(item[3:7])
    years.append(year)
data['YEAR'] = years

columns2 = ['YEAR', 'OUTS_CT', 'EVENT_CD', 'EVENT_OUTS_CT', 'BASE1_RUN_ID',
            'BASE2_RUN_ID', 'BASE3_RUN_ID', 'RUN1_SB_FL', 'RUN2_SB_FL',
            'RUN3_SB_FL', 'RUN1_CS_FL', 'RUN2_CS_FL', 'RUN3_CS_FL',
            'RUN1_PK_FL', 'RUN2_PK_FL', 'RUN3_PK_FL', 'START_BASES_CD',
            'END_BASES_CD', 'EVENT_RUNS_CT']

sbdata = data.loc[:, columns2].copy()

ids = ['ageet101', 'aloms101', 'aloum101', 'baked002', 'bayld001', 'belam101',
       'blaip101', 'bondb101', 'bowal001', 'bretg001', 'brocl102', 'buckb001',
       'bufod101', 'bumba001', 'cabee001', 'campb101', 'cardj101', 'carer001',
       'cedec001', 'clarh101', 'colld001', 'concd001', 'cruzj001', 'cruzj002',
       'daviw102', 'dawsa001', 'dejei001', 'dernb001', 'dilom001', 'dried001',
       'gantj001', 'garcd001', 'garnp001', 'garrr101', 'gibsk001', 'grifa001',
       'grifk001', 'harpt101', 'harrt001', 'hendr001', 'herrt001', 'jackr001',
       'joner002', 'kellp101', 'lacyl001', 'landk001', 'lansc001', 'law-r001',
       'leflr101', 'leonj001', 'loped001', 'lowej001', 'maddg001', 'madlb001',
       'mannr001', 'mattg001', 'mazzl001', 'mcbrb101', 'mccrt102', 'milne001',
       'molip001', 'moreo001', 'morgj001', 'mosel001', 'mumpj001', 'murcb101',
       'murpd001', 'nelsd101', 'nortb101', 'otisa001', 'parkd001', 'patef101',
       'puhlt001', 'raint001', 'randl101', 'randw001', 'remyj001', 'richg001',
       'rivem001', 'rosep001', 'roysj001', 'russb001', 'schmm001', 'scotr101',
       'smitl002', 'smito001', 'smitr101', 'tavef101', 'tempg001', 'thomd001',
       'thond001', 'tolab101', 'tovac101', 'trama001', 'washc001', 'whitl001',
       'whitf001', 'whitr101', 'willb101', 'wilsm001', 'wilsw001', 'winfd001',
       'wynnj101', 'yastc101', 'younr001']
# merrifield = merrw001, carew = carer001

stealers = defaultdict(float)
redifflist = []

for id in ids:
    playerid = id
    playercrit1 = sbdata['BASE1_RUN_ID'] == playerid
    playercrit1a = sbdata['RUN1_SB_FL'] == 'T'
    playercrit1b = sbdata['RUN1_CS_FL'] == 'T'
    playercrit1c = sbdata['RUN1_PK_FL'] == 'T'
    playercrit1t = playercrit1 & (playercrit1a | playercrit1b | playercrit1c)
    playercrit2 = sbdata['BASE2_RUN_ID'] == playerid
    playercrit2a = sbdata['RUN2_SB_FL'] == 'T'
    playercrit2b = sbdata['RUN2_CS_FL'] == 'T'
    playercrit2c = sbdata['RUN2_PK_FL'] == 'T'
    playercrit2t = playercrit2 & (playercrit2a | playercrit2b | playercrit2c)
    playercrit3 = sbdata['BASE3_RUN_ID'] == playerid
    playercrit3a = sbdata['RUN3_SB_FL'] == 'T'
    playercrit3b = sbdata['RUN3_CS_FL'] == 'T'
    playercrit3c = sbdata['RUN3_PK_FL'] == 'T'
    playercrit3t = playercrit3 & (playercrit3a | playercrit3b | playercrit3c)

    tcrit = playercrit1t | playercrit2t | playercrit3t

    sbdataplayer = sbdata.loc[tcrit].copy()

    year = sbdataplayer['YEAR'].to_list()
    start_outs = sbdataplayer['OUTS_CT'].to_list()
    start_base = sbdataplayer['START_BASES_CD'].to_list()
    runs_on_play = sbdataplayer['EVENT_RUNS_CT'].to_list()

    out_change = sbdataplayer['EVENT_OUTS_CT'].to_list()
    end_base = sbdataplayer['END_BASES_CD'].to_list()

    start_situation = list(zip(start_outs, start_base, year, repeat(0)))

    end_outs = []
    for x in range(len(start_outs)):
        a = start_outs[x]
        b = out_change[x]
        end_out = a + b
        end_outs.append(end_out)

    end_situation = list(zip(end_outs, end_base, year, runs_on_play))

    start_values = calc_values(start_situation)
    end_values = calc_values(end_situation)

    diffs = []
    for x in range(len(start_values)):
        start = start_values[x]
        end = end_values[x]
        diff = end - start
        diffs.append(diff)

    total_diff = round(sum(diffs), 3)
    stealers[id] = total_diff
    redifflist.append(total_diff)
#    print(f'{id}: {total_diff}')

stealdf = pd.read_csv('carew.csv')
stealdf['REdiff'] = redifflist

stealdf.to_excel('stealdf.xlsx')
