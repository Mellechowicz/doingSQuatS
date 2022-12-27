#!/usr/bin/python3

import numpy  as np
import pandas as pd

from sys import argv
from itertools import product

data = pd.read_csv(argv[1],sep='\s+')

try:
    col  = argv[2]
except IndexError:
    print(data)
    exit()

sortedArgs = np.argsort(data[col])
for arg in sortedArgs:
    for field in data:
        print(data[field][arg],end=' ')
    print('')
