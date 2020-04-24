#coding:utf-8
import sys
import os 



import pandas as pd
import numpy as np


df = pd.DataFrame(np.arange(12).reshape(3,4), columns=[chr(i) for i in range(97,101)])

print df
df.iloc[1,3] = '老王'

for index, row in df.iterrows():
        #print row["date"],index
    df.iloc[index,3] = '老王'

print df
for index, row in df.iterrows():
    row = dict(df.iloc[index])
    row['d'] = '老李'
    df.iloc[index] = pd.Series(row)

print df
