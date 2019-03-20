
import pandas as pd

# games80 = pd.read_csv('game_data.csv')
# print(games80.head())
# print(games80.tail())

# print(games80['AWAY_MANAGER_NAME_TX'].value_counts())

files = ['game_data_1980.csv', 'game_data_1981.csv', 'game_data_1982.csv',
         'game_data_1983.csv', 'game_data_1984.csv', 'game_data_1985.csv',
         'game_data_1986.csv', 'game_data_1987.csv', 'game_data_1988.csv',
         'game_data_1989.csv']

x = 0
for file in files:
    with open(file, 'r') as f:
        if x == 0:
            file_data = f.readlines()
        else:
            file_data = f.readlines()
            del file_data[0]
        print(f'Processing {file}')

        with open('game_data_dec.csv', mode="a") as gdd:
            for line in range(0, len(file_data)):
                gdd.write(file_data[line])
    x += 1
