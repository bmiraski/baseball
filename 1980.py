import pandas as pd

col_names = ['GAME_ID', 'AWAY_TEAM_ID', 'INN_CT', 'BAT_HOME_ID', 'OUTS_CT', 'BALLS-CT', 'STRIKES_CT', 'PITCH_SEQ_TX', 'AWAY_SCORE_CT', 'HOME_SCORE_CT', 'BAT_ID', 'BAT_HAND_CD', 'RESP_BAT_ID', 'RESP_BAT_HAND_CD', 'PIT_CD', 'PIT_HAND_CD', 'RESP_PIT_ID', 'RESP_PIT_HAND_CD', 'PS2_FLD_ID', 'POS3_FLD_ID', 'POS4_FLD_ID', 'POS5_FLD_ID', 'POS6_FLD_ID', 'POS7_FLD_ID', 'POS8_FLD_ID', 'POS9_FLD_ID', 'BASE1_RUN_ID', 'BASE2_RUN_ID', 'BASE3_RUN_ID', 'EVENT_TX', 'LEADOFF_FL', 'PH_FL', 'BAT_FLD_CD', 'BAT_LINEUP_ID', 'EVENT_CD', 'BAT_EVENT_FL', 'AB_FL', 'H_FL', 'SH_FL', 'SF_FL', 'EVENT_OUTS_CT', 'DP_FL', 'TP_FL', 'RBI_CT', 'WP_FL', 'PB_FL', 'FLD_CD', 'BATTEDBALL_CD', 'BUNT_FL', 'FOUL_FL', 'BATTEDBALL_LOC_TX', 'ERR_CT', 'ERR1_FLD_CD', 'ERR1_CD', 'ERR2_FLD_CD', 'ERR2_CD', 'ERR3_FLD_CD', 'ERR3_CD', 'BAT_DEST_ID', 'RUN1_DEST_ID', 'RUN2_DEST_ID', 'RUN3_DEST_ID', 'BAT_PLAY_TX', 'RUN1_PLAY_TX', 'RUN2_PLAY_TX', 'RUN3_PLAY_TX', 'RUN1_SB_FL', 'RUN2_SB_FL', 'RUN3_SB_FL', 'RUN1_CS_FL', 'RUN2_CS_FL', 'RUN3_CS_FL', 'RUN1_PK_FL', 'RUN2_PK_FL', 'RUN3_PK_FL', 'RUN1_RESP_PIT_ID', 'RUN2_RESP_PIT_ID', 'RUN3_RESP_PIT_ID', 'GAME_NEW_FL', 'GAME_END_FL', 'PR_RUN1_FL', 'PR_RUN2_FL', 'PR_RUN3_FL', 'REMOVED_FOR_PR_RUN1_ID', 'REMOVED_FOR_PR_RUN2_ID', 'REMOVED_FOR_PR_RUN3_ID', 'REMOVED_FOR_PH_BAT_ID', 'REMOVED_FOR_PH_BAT_FLD_CD', 'PO1_FLD_CD', 'PO2_FLD_CD', 'PO3_FLD_CD', 'ASS1_FLD_CD', 'ASS2_FLD_CD', 'ASS3_FLD_CD', 'ASS4_FLD_CD', 'ASS5_FLD_CD', 'EVENT_ID']


eighty = pd.read_csv('data/retrosheet/unzipped/1980eve/all1980.csv',
                     names=col_names)

print(eighty.head())
print(eighty.tail())
