#!/usr/bin/env python

#import csv
import pandas as pd
#import numpy as np
#import datetime

# save the possession data in a
# dictionary object
#csvfile = open('full_poss.csv', 'rb')
#reader = csv.DictReader(csvfile)

#for row in reader:
#	print row

df = pd.read_csv('full_poss.csv')
df.info()
print df.describe()
print df.head()
