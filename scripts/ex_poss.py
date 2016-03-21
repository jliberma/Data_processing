#!/usr/bin/env python

import pandas as pd
pd.set_option('display.max_rows', 1000)
import numpy as np
import matplotlib.pyplot as plt
#matplotlib.style.use('ggplot')

def to_seconds(mmss):
	seconds= 0
	for sect in mmss.split(':'):
		seconds = seconds * 60 + int(sect)
	return seconds

df = pd.read_csv('full_poss.csv')

# why can't I do this?
#df[['H1','H2','Total']] = df[['H1','H2','Total']].map(to_seconds)

# convert the time series to seconds
df['H1'] = df['H1'].map(to_seconds)
df['H2'] = df['H2'].map(to_seconds)
df['Total'] = df['Total'].map(to_seconds)
print df.head(8)
#print len(df.index)
#df.info()
#print df[df.columns[4:7]].head()

# split into two data frames
df['side'] = np.tile([1,2],len(df.index)/2)
df1 = df[df.side == 1]
df2 = df[df.side == 2]

# do I need to find winner?
# for correlation,
# subtract df1 total from df2 total
# subtract df1 points from df2 points
# correlate, plot
print sum(df1['Points'].ge(df2['Points']))
print sum(df1['Points'].lt(df2['Points']))
#plt.figure()
df['Points'].plot()
#plt.show()
#plt.savefig("temp.png")
