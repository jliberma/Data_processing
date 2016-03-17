#!/usr/bin/env python

import pandas as pd

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
print df[df.columns[4:7]].head()
