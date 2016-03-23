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

# convert min:sec columns to sec
full_poss[['H1','H2','Total']] = full_poss[['H1','H2','Total']].applymap(to_seconds)

# split match results into two data frames
full_poss['side'] = np.tile([1,2],len(full_poss.index)/2)
team1 = full_poss[full_poss.side == 1].reset_index(drop=True)
team2 = full_poss[full_poss.side == 2].reset_index(drop=True)

# subtract team 2 points and possession from team 1 points and possession
poss_diff = team1[['Points','H1','H2','Total']] - team2[['Points','H1','H2','Total']]

# calculate Pearson correlation coefficient and p-value
pc = stats.pearsonr(poss_diff['Points'], poss_diff['Total'])

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
plt.title("Scoring and time of possession in rugby 7s")
plt.savefig("7s_poss_scoring.png")

# Calculate win frequency for teams with time of possession advantage
total_win = ((poss_diff['Points'] > 0) & (poss_diff['Total'] > 0) | (poss_diff['Points'] < 0) & (poss_diff['Total'] < 0))
h1_win = ((poss_diff['Points'] > 0) & (poss_diff['H1'] > 0) | (poss_diff['Points'] < 0) & (poss_diff['H1'] < 0))
h2_win = ((poss_diff['Points'] > 0) & (poss_diff['H2'] > 0) | (poss_diff['Points'] < 0) & (poss_diff['H2'] < 0))
#print "Total: %s" % len(poss_diff[total_win])
#print "1st half %s" % len(poss_diff[h1_win])
#print "2nd half: %s" % len(poss_diff[h2_win])

# count ties
#tie = poss_diff['Points'] == 0
#print len(poss_diff[tie])

# TODO: add percentage calculations
# only %54.8 of teams with possession advantage won
# TODO: plot again without non-core teams
