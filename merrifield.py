"""Calculate Marcels for Merrifield."""
# merriwh01 is Whit Merrifield

import pandas as pd

batting = pd.read_csv('data/lehman/baseballdatabank-master/core/Batting.csv',
                      index_col='playerID')
people = pd.read_csv('data/lehman/baseballdatabank-master/core/People.csv',
                     index_col='playerID')
lgavg = pd.read_csv('data/lgavg162.csv')


def sub_player_data(data, m):
    """Sub in league average data if player missing data."""
    age_m = m - birth_year
    if age_m <= 25:
        age_block = 25
    elif age_m <= 30:
        age_block = 30
    elif age_m <= 35:
        age_block = 35
    else:
        age_block = 36
    sub_data_m = lgavg[lgavg['Year'] == m]
    sub_data_age = sub_data_m[sub_data_m['Age'] == age_block].copy()
    print(sub_data_age)
    sub_data_age['stint'] = 1
    sub_data_age['Age'] = age_m
    sub_data_age['PA'] = (sub_data_age['AB'] + sub_data_age['BB'] + sub_data_age['SF'] +
                          sub_data_age['SH'] + sub_data_age['HBP'])
    sub_data_age = sub_data_age.set_index(['Year'])
    print(sub_data_age)
    data = pd.concat([data, sub_data_age])
    return data


player = 'troutmi01'
# harpebr03
# troutmi01
# rendoan01
# merriwh01
merrifield = batting.loc[[player]].copy().set_index('yearID')
merrifield = merrifield.groupby('yearID').sum()
league_rate = pd.read_csv('pa_rate.csv', index_col='Year')
years = merrifield.index.values
birth_year = people.loc[player, 'birthYear']
birth_month = people.loc[player, 'birthMonth']
if birth_month >= 7:
    birth_year += 1

ages = []
for year in years:
    age = year - birth_year
    ages.append(age)

merrifield['PA'] = (merrifield['AB'] + merrifield['BB'] + merrifield['SF'] +
                    merrifield['SH'] + merrifield['HBP'])
merrifield['Age'] = ages

merrifield_years = list(merrifield.index.values)

model_year = 2020
m3 = model_year - 3
m2 = model_year - 2
m1 = model_year - 1

if m3 not in merrifield_years:
    merrifield = sub_player_data(merrifield, m3)

if m2 not in merrifield_years:
    merrifield = sub_player_data(merrifield, m2)

if m1 not in merrifield_years:
    merrifield = sub_player_data(merrifield, m1)

print(merrifield.sort_values(by=['Age']))
pa_m3 = int(merrifield.loc[m3, 'PA'])
pa_m2 = int(merrifield.loc[m2, 'PA'])
pa_m1 = int(merrifield.loc[m1, 'PA'])
weighted_pa = (3 * pa_m3) + (4 * pa_m2) + (5 * pa_m1)
projected_pa = round(((0.5 * pa_m1) + (0.1 * pa_m2) + 200), 0)
print(f"Projected PAs: {projected_pa}")

projected_age = int(merrifield.loc[m1, 'Age']) + 1
if projected_age > 30:
    age_adjustment = (29 - projected_age) * 0.003
elif projected_age < 30:
    age_adjustment = (29 - projected_age) * 0.006
else:
    age_adjustment = 0

columns = ['R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'GIDP',
           'HBP', 'SH', 'SF', 'IBB']

projected_stats = []
for col in columns:
    stat_m3 = int(merrifield.loc[m3, col])
    stat_m2 = int(merrifield.loc[m2, col])
    stat_m1 = int(merrifield.loc[m1, col])

    weighted_stat = (3 * stat_m3) + (4 * stat_m2) + (5 * stat_m1)
    # print(weighted_stat)

    lgstat_m3 = league_rate.loc[m3, col]
    lgstat_m2 = league_rate.loc[m2, col]
    lgstat_m1 = league_rate.loc[m1, col]

    lg_play_stat = ((lgstat_m3 * pa_m3 * 3) +
                    (lgstat_m2 * pa_m2 * 4) +
                    (lgstat_m1 * pa_m1 * 5))
    # print(lg_play_stat)

    lps_1200 = (lg_play_stat * 1200) / weighted_pa
    # print(lps_1200)

    tot_stat = weighted_stat + lps_1200
    tot_pa = weighted_pa + 1200
    expected_rate = tot_stat / tot_pa
    # print(expected_rate)

    base_projection = projected_pa * expected_rate

    end_projection = round(base_projection * (1 + age_adjustment), 0)
    projected_stats.append(end_projection)

print(columns)
print(projected_stats)

projected_ab = projected_pa - (projected_stats[8] + projected_stats[11] +
                               projected_stats[12] + projected_stats[13])
print(f"Projected ABs: {projected_ab}")
projected_avg = round((projected_stats[1] / projected_ab), 3)
projected_obp = round(((projected_stats[1] + projected_stats[8] +
                       projected_stats[11]) / projected_pa), 3)
projected_1b = projected_stats[1] - (projected_stats[2] + projected_stats[3] +
                                     projected_stats[4])
projected_tb = (projected_1b + (projected_stats[2] * 2) +
                (projected_stats[3] * 3) + (projected_stats[4] * 4))
projected_slg = round((projected_tb / projected_ab), 3)

print(f"Projected Slash Line: {projected_avg}/{projected_obp}/{projected_slg}")

wOBA_num = ((0.690 * (projected_stats[8] - projected_stats[14])) +
            (0.719 * projected_stats[11]) + (.870 * projected_1b) +
            (1.217 * projected_stats[2]) + (1.529 * projected_stats[3]) +
            (1.940 * projected_stats[4]))

wOBA_den = (projected_ab + projected_stats[8] - projected_stats[14] +
            projected_stats[13] + projected_stats[11])

wOBA = round(wOBA_num / wOBA_den, 3)
print(f"wOBA(2019 weightings): {wOBA}")

wRAA = round(((wOBA - 0.320) / 1.157) * projected_pa, 2)
print(f"wRAA(2019 weightings): {wRAA}")
