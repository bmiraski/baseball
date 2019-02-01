"""Calculate Marcels for Merrifield."""
# merriwh01 is Whit Merrifield

import pandas as pd

batting = pd.read_csv('data/lehman/baseballdatabank-master/core/Batting.csv',
                      index_col='playerID')
people = pd.read_csv('data/lehman/baseballdatabank-master/core/Master.csv',
                     index_col='playerID')

player = 'russead02'

merrifield = batting.loc[player, :].copy().set_index('yearID')
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

print(merrifield)

pa_2016 = int(merrifield.loc[2016, 'PA'])  # 332
pa_2017 = int(merrifield.loc[2017, 'PA'])  # 630
pa_2018 = int(merrifield.loc[2018, 'PA'])  # 707

weighted_pa = (3 * pa_2016) + (4 * pa_2017) + (5 * pa_2018)
projected_pa = round(((0.5 * pa_2018) + (0.1 * pa_2017) + 200), 0)
print(f"Projected PAs: {projected_pa}")

projected_age = int(merrifield.loc[2018, 'Age']) + 1
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
    stat_2016 = int(merrifield.loc[2016, col])
    stat_2017 = int(merrifield.loc[2017, col])
    stat_2018 = int(merrifield.loc[2018, col])

    weighted_stat = (3 * stat_2016) + (4 * stat_2017) + (5 * stat_2018)
    # print(weighted_stat)

    lgstat_2016 = league_rate.loc[2016, col]
    lgstat_2017 = league_rate.loc[2017, col]
    lgstat_2018 = league_rate.loc[2018, col]

    lg_play_stat = ((lgstat_2016 * pa_2016 * 3) +
                    (lgstat_2017 * pa_2017 * 4) +
                    (lgstat_2018 * pa_2018 * 5))
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
            (0.720 * projected_stats[11]) + (.880 * projected_1b) +
            (1.247 * projected_stats[2]) + (1.578 * projected_stats[3]) +
            (2.031 * projected_stats[4]))

wOBA_den = (projected_ab + projected_stats[8] - projected_stats[14] +
            projected_stats[13] + projected_stats[11])

wOBA = round(wOBA_num / wOBA_den, 3)
print(f"wOBA(2018 weightings): {wOBA}")

wRAA = round(((wOBA - 0.315) / 1.226) * projected_pa, 2)
print(f"wRAA(2018 weightings): {wRAA}")
