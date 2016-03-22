#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# make Tufte-style display dot-dash graph
# etframes is available from: https://github.com/ahupp/etframes/blob/master/etframes.py
import etframes
plt.style.use('ggplot')

# function to convert min:sec to sec
def to_seconds(mmss):
    seconds= 0
    for sect in mmss.split(':'):
        seconds = seconds * 60 + int(sect)
    return seconds

# read the possession data to a csv
full_poss = pd.read_csv('https://raw.githubusercontent.com/jliberma/Data_processing/master/data/full_poss.csv')

# TODO: submit to stack exchange for review, why can't I do this?
#df[['H1','H2','Total']] = df[['H1','H2','Total']].map(to_seconds)

# convert min:sec columns to sec
full_poss['H1'] = full_poss['H1'].map(to_seconds)
full_poss['H2'] = full_poss['H2'].map(to_seconds)
full_poss['Total'] = full_poss['Total'].map(to_seconds)

# split match results into two data frames
full_poss['side'] = np.tile([1,2],len(full_poss.index)/2)
team1 = full_poss[full_poss.side == 1].reset_index(drop=True)
team2 = full_poss[full_poss.side == 2].reset_index(drop=True)

# subtract team 2 points and possession from team 1 points and possession
poss_diff = team1[['Points','Total']] - team2[['Points','Total']]

# calculate number of ties
#tie = poss_diff['Points'] == 0
#print len(poss_diff[tie])

# calculate Pearson correlation coefficient and p-value
pc = stats.pearsonr(poss_diff['Points'], poss_diff['Total'])
print(pc)

# find the slope and intercept of the best fit line
slope,intercept = np.polyfit(poss_diff['Total'],poss_diff['Points'],1)

# create a list of values for the best fit line
ablineValues = slope * poss_diff[['Total']] + intercept

# plot the best fit line over the values
plt.scatter(poss_diff['Total'],poss_diff['Points'],c=".5")
etframes.add_dot_dash_plot(plt.gca(), ys=poss_diff['Points'], xs=poss_diff['Total'])
plt.plot(poss_diff['Total'], ablineValues, 'b', c="k")

# label and save the graph
plt.ylabel("Point differential")
plt.xlabel("Possession differential (seconds)")
plt.title("Scoring by time of possession differential")
plt.savefig("7s_poss_scoring.png")

# TODO: calculate frequencies
# win with total, H1, H2 advantage
# if team1.pts > team2.pts && team1.total > team2.total || if team2.pts > team1.pts && team2.total > team1.total

# TODO: plot again without non-core teams
# this could be a separate study
