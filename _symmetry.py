#!/usr/bin/python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import re
import counter

from JorGpi.POSCARloader import POSCARloader
import spglib

if len(argv) < 3:
    print('Feed me with:')
    print('(i)  name of  input directory')
    print('(ii) name of output directory')
    exit(-1)

sameSymmetries = {}

directory = os.fsencode(argv[1])
cntr = counter.Counter(limit=len(os.listdir(directory)),PREFIX='Processed ',SUFFIX=' files.')
cntr.initiate()
if len(argv) >= 4:
    cntr2 = counter.Counter(PREFIX='Removed   ',SUFFIX=' 1.P1 files.')
    cntr2.initiate()
    cntr.iterate_position()

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith(".vasp"):
        continue
    loader = POSCARloader(argv[1]+'/'+filename)
    try:
        loader.parse()
    except (IndexError,TypeError) as e:
        print(e,end=': For ')
        print(filename, end='  ')
        print('('+argv[1]+'/'+filename+')')
        cntr.iterate_position()
        if len(argv) >= 4:
            cntr2.iterate_position()
        continue
    stdCell = spglib.standardize_cell(loader(0)['cellSymmetry'], to_primitive=1, no_idealize=0, symprec=1e-2)
    o = spglib.get_symmetry_dataset(stdCell)
    local_key = str(o['number'])+'_'+o['international']
    local_key = re.sub('[^-0-9a-zA-Z]','.',local_key)
    
    if len(argv) >= 4:
        if local_key == '1.P1':
            os.remove(argv[1]+'/'+filename)
            cntr2.update()
            cntr.update()
            continue

    local_key += '_%05d'%len(set(o['equivalent_atoms']))

    if local_key not in sameSymmetries:
        sameSymmetries[local_key]  = [filename]
        print('Found new symmetry:',local_key, "(equivalent atoms)")
        cntr.iterate_position()
        if len(argv) >= 4:
            cntr2.iterate_position()
    else:
        sameSymmetries[local_key].append(filename)
    cntr.update()

#print('All symmetries:')
os.mkdir(argv[2])
for k in sameSymmetries.keys():
    print(k)
    name=argv[2]+'/'+k
    os.mkdir(name)
    for f in sameSymmetries[k]:
        shutil.copy2(argv[1]+'/'+f,name+'/')
