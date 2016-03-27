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
fp = pd.read_csv('https://raw.githubusercontent.com/jliberma/Data_processing/master/data/full_poss.csv')

# convert min:sec columns to sec
fp[['H1','H2','Total']] = fp[['H1','H2','Total']].applymap(to_seconds)

# split match results into two data frames
fp['side'] = np.tile([1,2],len(fp.index)/2)
t1 = fp[fp.side == 1].reset_index(drop=True)
t2 = fp[fp.side == 2].reset_index(drop=True)

# subtract team 2 points and possession from team 1 points and possession
pd2 = t1[['Points','H1','H2','Total']] - t2[['Points','H1','H2','Total']]

# find the slope and intercept of the best fit line
slope,intercept = np.polyfit(pd2['Total'],pd2['Points'],1)

# create a list of values for the best fit line
ablineValues = slope * pd2[['Total']] + intercept

# plot the best fit line over the values
plt.scatter(pd2['Total'],pd2['Points'],c=".5")
etframes.add_dot_dash_plot(plt.gca(), ys=pd2['Points'], xs=pd2['Total'])
#plt.plot(pd2['Total'], ablineValues, 'b', c="k")

# label the graph
plt.ylabel("Point differential")
plt.xlabel("Possession differential (seconds)")
plt.title("Scoring and time of possession in rugby 7s")

# annotate graph with Pearson correlation coefficient and p-value
pc = stats.pearsonr(pd2['Points'], pd2['Total'])
#plt.annotate('correlation coefficient: %s' % round(pc[0],4), xy=(0,0), xytext=(150, -45))
#plt.annotate('p-value: %s' % pc[1], xy=(0,0), xytext=(150, -50))

# save the graph
#plt.savefig("7s_poss_scoring.png")

# Calculate win frequency for teams with time of possession advantage
# boolean indexing: http://pandas.pydata.org/pandas-docs/stable/indexing.html#boolean-indexing
total = (pd2.Points * pd2.Total > 0).sum()
pct = round(float(total.sum())/len(pd2.index),2)

print('%s%% of matches were won by the team with more possession (%s/%s)' % 
    (int(100*pct), total, len(pd2.index)))

# TODO: plot again without non-core teams
# TODO: gather non-core teams programatically
noncore = ['BELGIUM','BRAZIL','RUSSIA','HONG KONG','ZIMBABWE','AMERICAN SAMOA','PAPUA NEW GUINEA']
t1.columns=['Match','Event','T1','P1','T1H1','T1H2','T1T','side1']
t2.columns=['Match','Event','T2','P2','T2H1','T2H2','T2T','side2']
t3 = pd.merge(t1,t2,on=['Match','Event'])
t3 = t3[-t3['T1'].isin(noncore)&-t3['T2'].isin(noncore)]
p = t3.P1 - t3.P2
t = t3.T1T - t3.T2T
nct = sum(t*p>0)
ncpct = round(float(nct.sum())/len(t3.index),2)
print('%s%% of matches were won by teams with more possession (core vs core only) (%s/%s)' % 
    (int(100*ncpct), nct, len(t3.index)))
plt.scatter(t,p,c="r")
plt.show()
