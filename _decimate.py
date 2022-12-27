#!/usr/bin/python3

import numpy as np
import os
import counter
from sys import argv

if len(argv) < 2:
    print('Feed me with:')
    print('(i)  name of filecide directory')
    print('(ii) probability of removal (optional; 0-1; default: 0.1')
    exit(-1)

try:
    PROBABILITY = np.float64(argv[2])
except IndexError:
    PROBABILITY = 0.1

directory = os.fsencode(argv[1])
cntr = counter.Counter(limit=len(os.listdir(directory)),PREFIX='',SUFFIX=' files.')
cntr.PREFIX  = 'Processed '+counter.colors.FONT['green']+counter.colors.STYLE['bold']
cntr.initiate()
cntr.iterate_position()
del_cntr = counter.Counter(limit=len(os.listdir(directory)),PREFIX='Deleted   ',SUFFIX=' files.')
del_cntr.initiate()

files = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".vasp"):
        files.append(argv[1]+'/'+filename)
    else:
        cntr.iterate_position()
        del_cntr.iterate_position()
        print(filename+" is not a '*.vasp' file!")
    cntr.update()
files = np.array(files)
mask  = np.where(np.random.random(files.size) <= PROBABILITY)

for fname in files[mask]:
    os.remove(fname)
    del_cntr.update()
