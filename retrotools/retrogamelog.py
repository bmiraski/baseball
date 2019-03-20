"""Process Retrosheet Game Log Files."""

from collections import defaultdict
import csv
import math
import sys

EXTRA_FIELDS = False


def extractBaseData(game):
    """Extract the main game data from each game line in file."""
    data_dict = defaultdict()
    game_data = game.split(',')
    if game_data[13] != '""':
        completion = ""
        for x in range(13, 18):
            completion += (game_data[x])
            if x != 17:
                completion += ","
        game_data[13] = completion
        del game_data[14:18]
    print(game_data)
    print(len(game_data))
    data_dict['GAME_ID'] = (game_data[3][1:4] + game_data[0][1:9] +
                            game_data[1][1:2])
    data_dict['GAME_DT'] = game_data[0][1:9]
    data_dict['GAME_CT'] = game_data[1][1:2]
    data_dict['GAME_DY'] = game_data[2][1:4]
    data_dict['START_GAME_TM'] = 0
    if (game_data[7][1:3] == 'AL') & (int(game_data[0][1:5]) >= 1973):
        data_dict['DH_FL'] = 'T'
    else:
        data_dict['DH_FL'] = 'F'
    data_dict['DAYNIGHT_PARK_CD'] = game_data[12][1:2]
    data_dict['AWAY_TEAM_ID'] = game_data[3][1:4]
    data_dict['HOME_TEAM_ID'] = game_data[6][1:4]
    data_dict['PARK_ID'] = game_data[16][1:6]
    data_dict['AWAY_START_PIT_ID'] = game_data[101][1:-1]
    data_dict['HOME_START_PIT_ID'] = game_data[103][1:-1]
    data_dict['BASE4_UMP_ID'] = game_data[77][1:-1]
    data_dict['BASE1_UMP_ID'] = game_data[79][1:-1]
    data_dict['BASE2_UMP_ID'] = game_data[81][1:-1]
    data_dict['BASE3_UMP_ID'] = game_data[83][1:-1]
    data_dict['LF_UMP_ID'] = game_data[85][1:-1]
    data_dict['RF_UMP_ID'] = game_data[87][1:-1]
    data_dict['ATTEND_PARK_ID'] = int(game_data[17])
    data_dict['MINUTES_GAME_CT'] = int(game_data[18])
    data_dict['INN_CT'] = int(math.ceil(int(game_data[11]) / 6))
    data_dict['AWAY_SCORE_CT'] = int(game_data[9])
    data_dict['HOME_SCORE_CT'] = int(game_data[10])
    data_dict['AWAY_HITS_CT'] = int(game_data[22])
    data_dict['HOME_HITS_CT'] = int(game_data[50])
    data_dict['AWAY_ERR_CT'] = int(game_data[45])
    data_dict['HOME_ERR_CT'] = int(game_data[73])
    data_dict['AWAY_LOB_CT'] = int(game_data[37])
    data_dict['HOME_LOB_CT'] = int(game_data[65])
    data_dict['WIN_PIT_ID'] = game_data[93][1:-1]
    data_dict['LOSE_PIT_ID'] = game_data[95][1:-1]
    data_dict['SAVE_PIT_ID'] = game_data[97][1:-1]
    data_dict['GWRBI_BAT_ID'] = game_data[99][1:-1]
    data_dict['AWAY_LINEUP1_BAT_ID'] = game_data[105][1:-1]
    data_dict['AWAY_LINEUP1_FLD_CD'] = int(game_data[107])
    data_dict['AWAY_LINEUP2_BAT_ID'] = game_data[108][1:-1]
    data_dict['AWAY_LINEUP2_FLD_CD'] = int(game_data[110])
    data_dict['AWAY_LINEUP3_BAT_ID'] = game_data[111][1:-1]
    data_dict['AWAY_LINEUP3_FLD_CD'] = int(game_data[113])
    data_dict['AWAY_LINEUP4_BAT_ID'] = game_data[114][1:-1]
    data_dict['AWAY_LINEUP4_FLD_CD'] = int(game_data[116])
    data_dict['AWAY_LINEUP5_BAT_ID'] = game_data[117][1:-1]
    data_dict['AWAY_LINEUP5_FLD_CD'] = int(game_data[119])
    data_dict['AWAY_LINEUP6_BAT_ID'] = game_data[120][1:-1]
    data_dict['AWAY_LINEUP6_FLD_CD'] = int(game_data[122])
    data_dict['AWAY_LINEUP7_BAT_ID'] = game_data[123][1:-1]
    data_dict['AWAY_LINEUP7_FLD_CD'] = int(game_data[125])
    data_dict['AWAY_LINEUP8_BAT_ID'] = game_data[126][1:-1]
    data_dict['AWAY_LINEUP8_FLD_CD'] = int(game_data[128])
    data_dict['AWAY_LINEUP9_BAT_ID'] = game_data[129][1:-1]
    data_dict['AWAY_LINEUP9_FLD_CD'] = int(game_data[131])
    data_dict['HOME_LINEUP1_BAT_ID'] = game_data[132][1:-1]
    data_dict['HOME_LINEUP1_FLD_CD'] = int(game_data[134])
    data_dict['HOME_LINEUP2_BAT_ID'] = game_data[135][1:-1]
    data_dict['HOME_LINEUP2_FLD_CD'] = int(game_data[137])
    data_dict['HOME_LINEUP3_BAT_ID'] = game_data[138][1:-1]
    data_dict['HOME_LINEUP3_FLD_CD'] = int(game_data[140])
    data_dict['HOME_LINEUP4_BAT_ID'] = game_data[141][1:-1]
    data_dict['HOME_LINEUP4_FLD_CD'] = int(game_data[143])
    data_dict['HOME_LINEUP5_BAT_ID'] = game_data[144][1:-1]
    data_dict['HOME_LINEUP5_FLD_CD'] = int(game_data[146])
    data_dict['HOME_LINEUP6_BAT_ID'] = game_data[147][1:-1]
    data_dict['HOME_LINEUP6_FLD_CD'] = int(game_data[149])
    data_dict['HOME_LINEUP7_BAT_ID'] = game_data[150][1:-1]
    data_dict['HOME_LINEUP7_FLD_CD'] = int(game_data[152])
    data_dict['HOME_LINEUP8_BAT_ID'] = game_data[153][1:-1]
    data_dict['HOME_LINEUP8_FLD_CD'] = int(game_data[155])
    data_dict['HOME_LINEUP9_BAT_ID'] = game_data[156][1:-1]
    data_dict['HOME_LINEUP9_FLD_CD'] = int(game_data[158])
    if EXTRA_FIELDS:
        extractExtraData(game_data, data_dict)
#     print(data_dict)
    return data_dict


def extractExtraData(game, data):
    """Extract the extra data fields for a game if necessary."""
    data['AWAY_TEAM_LEAGUE_ID'] = game[4][1:3]
    data['HOME_TEAM_LEAGUE_ID'] = game[7][1:3]
    data['AWAY_TEAM_GAME_CT'] = int(game[5])
    data['HOME_TEAM_GAME_CT'] = int(game[8])
    data['OUTS_CT'] = int(game[11])
    data['COMPLETION_TX'] = game[13][1:-1]
    data['FORFEIT_TX'] = game[14][1:-1]
    data['PROTEST_TX'] = game[15][1:-1]
    data['AWAY_LINE_TX'] = str(game[19][1:-1])
    data['HOME_LINE_TX'] = str(game[20][1:-1])
    data['AWAY_AB_CT'] = int(game[21])
    data['AWAY_2B_CT'] = int(game[23])
    data['AWAY_3B_CT'] = int(game[24])
    data['AWAY_HR_CT'] = int(game[25])
    data['AWAY_BI_CT'] = int(game[26])
    data['AWAY_SH_CT'] = int(game[27])
    data['AWAY_SF_CT'] = int(game[28])
    data['AWAY_HP_CT'] = int(game[29])
    data['AWAY_BB_CT'] = int(game[30])
    data['AWAY_IBB_CT'] = int(game[31])
    data['AWAY_SO_CT'] = int(game[32])
    data['AWAY_SB_CT'] = int(game[33])
    data['AWAY_CS_CT'] = int(game[34])
    data['AWAY_GDP_CT'] = int(game[35])
    data['AWAY_XI_CT'] = int(game[36])
    data['AWAY_PITCHER_CT'] = int(game[38])
    data['AWAY_ER_CT'] = int(game[39])
    data['AWAY_TER_CT'] = int(game[40])
    data['AWAY_WP_CT'] = int(game[41])
    data['AWAY_BK_CT'] = int(game[42])
    data['AWAY_PO_CT'] = int(game[43])
    data['AWAY_A_CT'] = int(game[44])
    data['AWAY_PB_CT'] = int(game[46])
    data['AWAY_DP_CT'] = int(game[47])
    data['AWAY_TP_CT'] = int(game[48])
    data['HOME_AB_CT'] = int(game[49])
    data['HOME_2B_CT'] = int(game[51])
    data['HOME_3B_CT'] = int(game[52])
    data['HOME_HR_CT'] = int(game[53])
    data['HOME_BI_CT'] = int(game[54])
    data['HOME_SH_CT'] = int(game[55])
    data['HOME_SF_CT'] = int(game[56])
    data['HOME_HP_CT'] = int(game[57])
    data['HOME_BB_CT'] = int(game[58])
    data['HOME_IBB_CT'] = int(game[59])
    data['HOME_SO_CT'] = int(game[60])
    data['HOME_SB_CT'] = int(game[61])
    data['HOME_CS_CT'] = int(game[62])
    data['HOME_GDP_CT'] = int(game[63])
    data['HOME_XI_CT'] = int(game[64])
    data['HOME_PITCHER_CT'] = int(game[66])
    data['HOME_ER_CT'] = int(game[67])
    data['HOME_TER_CT'] = int(game[68])
    data['HOME_WP_CT'] = int(game[69])
    data['HOME_BK_CT'] = int(game[70])
    data['HOME_PO_CT'] = int(game[71])
    data['HOME_A_CT'] = int(game[72])
    data['HOME_PB_CT'] = int(game[74])
    data['HOME_DP_CT'] = int(game[75])
    data['HOME_TP_CT'] = int(game[76])
    data['UMP_HOME_NAME_TX'] = game[78][1:-1]
    data['UMP_1B_NAME_TX'] = game[80][1:-1]
    data['UMP_2B_NAME_TX'] = game[82][1:-1]
    data['UMP_3B_NAME_TX'] = game[84][1:-1]
    data['UMP_LF_NAME_TX'] = game[86][1:-1]
    data['UMP_RF_NAME_TX'] = game[88][1:-1]
    data['AWAY_MANAGER_ID'] = game[89][1:-1]
    data['AWAY_MANAGER_NAME_TX'] = game[90][1:-1]
    data['HOME_MANAGER_ID'] = game[91][1:-1]
    data['HOME_MANAGER_NAME_TX'] = game[92][1:-1]
    data['WIN_PIT_NAME_TX'] = game[94][1:-1]
    data['LOSE_PIT_NAME_TX'] = game[96][1:-1]
    data['SAVE_PIT_NAME_TX'] = game[98][1:-1]
    data['GOAHEAD_RBI_NAME_TX'] = game[100][1:-1]
    data['AWAY_LINEUP1_BAT_NAME_TX'] = game[106][1:-1]
    data['AWAY_LINEUP2_BAT_NAME_TX'] = game[109][1:-1]
    data['AWAY_LINEUP3_BAT_NAME_TX'] = game[112][1:-1]
    data['AWAY_LINEUP4_BAT_NAME_TX'] = game[115][1:-1]
    data['AWAY_LINEUP5_BAT_NAME_TX'] = game[118][1:-1]
    data['AWAY_LINEUP6_BAT_NAME_TX'] = game[121][1:-1]
    data['AWAY_LINEUP7_BAT_NAME_TX'] = game[124][1:-1]
    data['AWAY_LINEUP8_BAT_NAME_TX'] = game[127][1:-1]
    data['AWAY_LINEUP9_BAT_NAME_TX'] = game[130][1:-1]
    data['HOME_LINEUP1_BAT_NAME_TX'] = game[133][1:-1]
    data['HOME_LINEUP2_BAT_NAME_TX'] = game[136][1:-1]
    data['HOME_LINEUP3_BAT_NAME_TX'] = game[139][1:-1]
    data['HOME_LINEUP4_BAT_NAME_TX'] = game[142][1:-1]
    data['HOME_LINEUP5_BAT_NAME_TX'] = game[145][1:-1]
    data['HOME_LINEUP6_BAT_NAME_TX'] = game[148][1:-1]
    data['HOME_LINEUP7_BAT_NAME_TX'] = game[151][1:-1]
    data['HOME_LINEUP8_BAT_NAME_TX'] = game[154][1:-1]
    data['HOME_LINEUP9_BAT_NAME_TX'] = game[157][1:-1]
    data['ADD_INFO_TX'] = game[159][1:-1]
    data['ACQ_INFO_TX'] = game[160][1:-2]


base_fields = ['GAME_ID', 'GAME_DT', 'GAME_CT', 'GAME_DY', 'START_GAME_TM',
               'DH_FL', 'DAYNIGHT_PARK_CD', 'AWAY_TEAM_ID', 'HOME_TEAM_ID',
               'PARK_ID', 'AWAY_START_PIT_ID', 'HOME_START_PIT_ID',
               'BASE4_UMP_ID', 'BASE1_UMP_ID', 'BASE2_UMP_ID', 'BASE3_UMP_ID',
               'LF_UMP_ID', 'RF_UMP_ID', 'ATTEND_PARK_ID', 'MINUTES_GAME_CT',
               'INN_CT', 'AWAY_SCORE_CT', 'HOME_SCORE_CT', 'AWAY_HITS_CT',
               'HOME_HITS_CT', 'AWAY_ERR_CT', 'HOME_ERR_CT', 'AWAY_LOB_CT',
               'HOME_LOB_CT', 'WIN_PIT_ID', 'LOSE_PIT_ID', 'SAVE_PIT_ID',
               'GWRBI_BAT_ID', 'AWAY_LINEUP1_BAT_ID', 'AWAY_LINEUP1_FLD_CD',
               'AWAY_LINEUP2_BAT_ID', 'AWAY_LINEUP2_FLD_CD',
               'AWAY_LINEUP3_BAT_ID', 'AWAY_LINEUP3_FLD_CD',
               'AWAY_LINEUP4_BAT_ID', 'AWAY_LINEUP4_FLD_CD',
               'AWAY_LINEUP5_BAT_ID', 'AWAY_LINEUP5_FLD_CD',
               'AWAY_LINEUP6_BAT_ID', 'AWAY_LINEUP6_FLD_CD',
               'AWAY_LINEUP7_BAT_ID', 'AWAY_LINEUP7_FLD_CD',
               'AWAY_LINEUP8_BAT_ID', 'AWAY_LINEUP8_FLD_CD',
               'AWAY_LINEUP9_BAT_ID', 'AWAY_LINEUP9_FLD_CD',
               'HOME_LINEUP1_BAT_ID', 'HOME_LINEUP1_FLD_CD',
               'HOME_LINEUP2_BAT_ID', 'HOME_LINEUP2_FLD_CD',
               'HOME_LINEUP3_BAT_ID', 'HOME_LINEUP3_FLD_CD',
               'HOME_LINEUP4_BAT_ID', 'HOME_LINEUP4_FLD_CD',
               'HOME_LINEUP5_BAT_ID', 'HOME_LINEUP5_FLD_CD',
               'HOME_LINEUP6_BAT_ID', 'HOME_LINEUP6_FLD_CD',
               'HOME_LINEUP7_BAT_ID', 'HOME_LINEUP7_FLD_CD',
               'HOME_LINEUP8_BAT_ID', 'HOME_LINEUP8_FLD_CD',
               'HOME_LINEUP9_BAT_ID', 'HOME_LINEUP9_FLD_CD']

extra_field = ['AWAY_TEAM_LEAGUE_ID', 'HOME_TEAM_LEAGUE_ID',
               'AWAY_TEAM_GAME_CT', 'HOME_TEAM_GAME_CT', 'OUTS_CT',
               'COMPLETION_TX', 'FORFEIT_TX', 'PROTEST_TX', 'AWAY_LINE_TX',
               'HOME_LINE_TX', 'AWAY_AB_CT', 'AWAY_2B_CT', 'AWAY_3B_CT',
               'AWAY_HR_CT', 'AWAY_BI_CT', 'AWAY_SH_CT', 'AWAY_SF_CT',
               'AWAY_HP_CT', 'AWAY_BB_CT', 'AWAY_IBB_CT', 'AWAY_SO_CT',
               'AWAY_SB_CT', 'AWAY_CS_CT', 'AWAY_GDP_CT', 'AWAY_XI_CT',
               'AWAY_PITCHER_CT', 'AWAY_ER_CT', 'AWAY_TER_CT', 'AWAY_WP_CT',
               'AWAY_BK_CT', 'AWAY_PO_CT', 'AWAY_A_CT', 'AWAY_PB_CT',
               'AWAY_DP_CT', 'AWAY_TP_CT', 'HOME_AB_CT', 'HOME_2B_CT',
               'HOME_3B_CT', 'HOME_HR_CT', 'HOME_BI_CT', 'HOME_SH_CT',
               'HOME_SF_CT', 'HOME_HP_CT', 'HOME_BB_CT', 'HOME_IBB_CT',
               'HOME_SO_CT', 'HOME_SB_CT', 'HOME_CS_CT', 'HOME_GDP_CT',
               'HOME_XI_CT', 'HOME_PITCHER_CT', 'HOME_ER_CT', 'HOME_TER_CT',
               'HOME_WP_CT', 'HOME_BK_CT', 'HOME_PO_CT', 'HOME_A_CT',
               'HOME_PB_CT', 'HOME_DP_CT', 'HOME_TP_CT', 'UMP_HOME_NAME_TX',
               'UMP_1B_NAME_TX', 'UMP_2B_NAME_TX', 'UMP_3B_NAME_TX',
               'UMP_LF_NAME_TX', 'UMP_RF_NAME_TX', 'AWAY_MANAGER_ID',
               'AWAY_MANAGER_NAME_TX', 'HOME_MANAGER_ID',
               'HOME_MANAGER_NAME_TX', 'WIN_PIT_NAME_TX', 'LOSE_PIT_NAME_TX',
               'SAVE_PIT_NAME_TX', 'GOAHEAD_RBI_ID', 'GOAHEAD_RBI_NAME_TX',
               'AWAY_LINEUP1_BAT_NAME_TX', 'AWAY_LINEUP2_BAT_NAME_TX',
               'AWAY_LINEUP3_BAT_NAME_TX', 'AWAY_LINEUP4_BAT_NAME_TX',
               'AWAY_LINEUP5_BAT_NAME_TX', 'AWAY_LINEUP6_BAT_NAME_TX',
               'AWAY_LINEUP7_BAT_NAME_TX', 'AWAY_LINEUP8_BAT_NAME_TX',
               'AWAY_LINEUP9_BAT_NAME_TX', 'HOME_LINEUP1_BAT_NAME_TX',
               'HOME_LINEUP2_BAT_NAME_TX', 'HOME_LINEUP3_BAT_NAME_TX',
               'HOME_LINEUP4_BAT_NAME_TX', 'HOME_LINEUP5_BAT_NAME_TX',
               'HOME_LINEUP6_BAT_NAME_TX', 'HOME_LINEUP7_BAT_NAME_TX',
               'HOME_LINEUP8_BAT_NAME_TX', 'HOME_LINEUP9_BAT_NAME_TX',
               'ADD_INFO_TX', 'ACQ_INFO_TX']


if len(sys.argv) > 1:
    if '-x' in sys.argv:
        EXTRA_FIELDS = True

with open(sys.argv[1], 'r') as f:
    rawdata = f.readlines()

# test_game = rawdata[0]
with open('game_data.csv', mode='w') as game_file:
    if EXTRA_FIELDS:
        field_names = base_fields + extra_field
        writer = csv.DictWriter(game_file, fieldnames=field_names)
    else:
        writer = csv.DictWriter(game_file, fieldnames=base_fields)

    writer.writeheader()
    for game in rawdata:
        writer.writerow(extractBaseData(game))
