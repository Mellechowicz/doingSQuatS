#!/usr/bin/python3

from sys import argv
import os
from subprocess import check_output
import numpy as np
import counter

if os.path.isfile('/home/andrzej/andrzej/sSQSgenerator/_poscar_compare'):
    CMPR='/home/andrzej/andrzej/sSQSgenerator/_poscar_compare'
elif os.path.isfile('/home/andrzej/MEGAsync/sSQSgenerator/_poscar_compare'):
    CMPR='/home/andrzej/MEGAsync/sSQSgenerator/_poscar_compare'
elif os.path.isfile('/home/andrzej/alloys/sSQSgenerator/_poscar_compare'):
    CMPR='/home/andrzej/alloys/sSQSgenerator/_poscar_compare'
else:
    print("_poscar_compare not found!")
    exit(42)

found = []
statistics = {}
directory = os.fsencode('./')
listdir   = os.listdir(directory)
NMBR      = len(listdir)
cntr = counter.Counter(limit=NMBR,PREFIX='Processed ',SUFFIX=' files.')
cntr.initiate()
cntr.iterate_position()
cntr_offset = 0
del_cntr = counter.Counter(limit=NMBR,PREFIX='Deleted   ',SUFFIX=' files.')
del_cntr.initiate()
del_nmbr  = 0
for i,file in enumerate(listdir):
    to_be_deleted = []
    cntr.update(len(found)+cntr_offset)
    filename = os.fsdecode(file)
    if not filename.endswith(".vasp"):
        cntr_offset += 1
        continue
    if filename in found:
        continue
    found.append(filename)
    statistics[filename] = 1
    for file2 in listdir:
        filename2 = os.fsdecode(file2)
        if not filename2.endswith(".vasp"):
            continue
        if filename2 in found:
            continue
        result = check_output([CMPR,filename,filename2]) 
        if int(result) == 1:
            found.append(filename2)
            to_be_deleted.append(filename2)
            statistics[filename] += 1
    for redundant_file in to_be_deleted:
        if os.path.isfile(redundant_file):
            os.remove(redundant_file)
    del_nmbr+=len(to_be_deleted)
    del_cntr.update(del_nmbr+cntr_offset)
cntr.update(len(found)+cntr_offset)
print('')
print('')
with open('statistcs.txt','w+') as fl:
    for k in statistics.keys():
        fl.write('%s %d\n'%(k,statistics[k]))
