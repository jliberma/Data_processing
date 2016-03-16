#!/usr/bin/env python

import pandas as pd
import numpy as np
import datetime

df = pd.read_csv('full_poss.csv')

df.info()
print df.describe()
print df.head()
