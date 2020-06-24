import pandas as pd
import json
import os
import sys
import time
import numpy as np

if(len(sys.argv) != 4):
    print('Usage: combine_hdf5.py [input file name (no index or extension)] [lower run number] [upper run number]')
    sys.exit()

df = pd.read_hdf('{}_{}.hdf5'.format(sys.argv[1],sys.argv[2]))
print(sys.argv[2])

for i in range(int(sys.argv[2])+1,int(sys.argv[3])+1):
    df = df.append(pd.read_hdf('{}_{}.hdf5'.format(sys.argv[1],i)), ignore_index=True)
    print(i)

print('Resetting indices ...')
df = df.reset_index(drop=True)

print('Saving combined file ...')
df.to_hdf('{}.hdf5'.format(sys.argv[1]), key='procdf', mode='w')

print('Done.')
