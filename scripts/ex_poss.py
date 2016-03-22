#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# make Tufte-style display
plt.style.use('ggplot')

def to_seconds(mmss):
    seconds= 0
    for sect in mmss.split(':'):
        seconds = seconds * 60 + int(sect)
    return seconds

# TODO: add link to online data source
df = pd.read_csv('full_poss.csv')

# TODO: submit to stack exchange for review, why can't I do this?
#df[['H1','H2','Total']] = df[['H1','H2','Total']].map(to_seconds)

# convert the time series to seconds
df['H1'] = df['H1'].map(to_seconds)
df['H2'] = df['H2'].map(to_seconds)
df['Total'] = df['Total'].map(to_seconds)

# split into two data frames
df['side'] = np.tile([1,2],len(df.index)/2)
df1 = df[df.side == 1].reset_index(drop=True)
df2 = df[df.side == 2].reset_index(drop=True)

# subtract df1 total from df2 total
df3 = df1[['Points','Total']] - df2[['Points','Total']]

# find the slope and intercept of the best fit line
slope,intercept = np.polyfit(df3['Total'],df3['Points'],1)

# TODO: calculate Pearson correlation coefficient

# create a list of values for the best fit line
ablineValues = slope * df3[['Total']] + intercept

# plot the best fit line over the values
plt.scatter(df3['Total'],df3['Points'])
plt.plot(df3['Total'], ablineValues, 'b')
plt.title(slope)
plt.show()
#plt.savefig("temp.png")

# TODO: calculate frequencies
# win with total, H1, H2 advantage
