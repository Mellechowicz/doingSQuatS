#!/usr/bin/python3

import os
from sys import argv
from subprocess import check_output
import numpy as np
import counter

localpath   = os.getcwd()
possibility = []
while localpath != '/home':
    possibility.append(localpath+'/poscar_compare.x')
    localpath = os.path.dirname(localpath)

CMPR = None
for path in possibility:
    if os.path.isfile(path):
        print(path)
        CMPR=path
        break

if CMPR is None:
    if len(argv) > 1:
        CMPR=argv[1]
    else:
        print("poscar_compare not found!")
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
