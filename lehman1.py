import math
import pandas as pd
from collections import defaultdict




# master = pd.read_csv('data/lehman/baseballdatabank-master/core/Master.csv')

# columns = master.columns
# print(master.head(1))
# print(columns)

# batting = pd.read_csv('data/lehman/baseballdatabank-master/core/Batting.csv')
# columns_batting = batting.columns

# print(batting.head(1))
# print(columns_batting)

teams = pd.read_csv('data/lehman/baseballdatabank-master/core/Teams.csv')

teams['yearID'] = teams['yearID'].astype(float)

years = teams['yearID']

decades = []
for year in years:
    dec = math.floor(year / 10) * 10
    decades.append(dec)

teams['decade'] = decades

hr_data = teams.groupby('decade').agg({'G': 'sum', 'HR': 'sum', 'SO': 'sum'})

hr_data['G'] = hr_data['G'] / 2  # divide by 2 to not double count games
hr_data['HR Rate'] = hr_data['HR'] / hr_data['G']
hr_data['SO Rate'] = hr_data['SO'] / hr_data['G']

print(hr_data)
