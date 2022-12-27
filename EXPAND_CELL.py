#!/usr/bin/python3

import numpy as np
from sys import argv
from random import sample
import re
from copy import copy
from os import mkdir
from scipy.special import comb as binomial
import itertools as it

if len(argv) < 5:
    print("""Provide: 
            (  i) POSCAR file
            ( ii) number of flips
            (iii) flip-to atom symbol
            ( iv) flip only atoms of this type
            (  v) number of new structures
            ( vi) directory name #optional""")
    exit(-1)

POSCARname = argv[1]
try:
    DIRNAME=argv[6]
except KeyError:
    DIRNAME=argv[1]+'.dir'
try:
    mkdir(DIRNAME)
except FileExistsError:
    pass
flipped = int(argv[2])
symbol  = argv[3]
RANDOMID = str(np.random.randint(100000,999999))
if len(argv) == 4:
    flipper = None
else:
    flipper = argv[4]

data = ["",""]
elements = []
numbers  = []
extranumbers = None
lines    = []
comment  = ""
with open(POSCARname,'r+') as poscar:
    for i,line in enumerate(poscar.read().split('\n')):
        if i == 0:
            comment = re.sub(r"\n", "", line, flags=re.UNICODE)
        elif i < 5:
            data[0]+=line+'\n'
        elif i == 5:
            for e in line.split():
                elements.append(e)
        elif i == 6:
            for n in line.split():
                numbers.append(int(n))
        elif i == 7:
            extranumbers = []
            for i,n in enumerate(numbers):
                for j in range(n):
                    extranumbers.append(i)
            data[1]=line
        else:
            if len(re.sub(r"\s+", "", line, flags=re.UNICODE)) != 0:
                lines.append(line)

NUM_2B_FLIPPED = 0
for e,n in zip(elements,numbers):
    if e in flipper:
        NUM_2B_FLIPPED += n

sumOfSmaller = None
if flipper in elements:
    sumOfSmaller = int(np.sum(numbers[0:elements.index(flipper)]))
    
all_combinations = binomial(NUM_2B_FLIPPED,flipped,exact=True)
loc_combinations = int(argv[5])
if all_combinations <= loc_combinations:
    print("WARNING: total number of combinations is smaller than requested! Using deterministic approach with N="+str(all_combinations)+" files.")
    if sumOfSmaller is not None:
        iteration_over = enumerate(it.combinations(range(sumOfSmaller,sumOfSmaller+numbers[elements.index(flipper)]), flipped))
    else:
        iteration_over = enumerate(it.combinations(range(len(lines)), flipped))
else:
    iteration_over = zip(range(loc_combinations),it.repeat(None))

for i,combination in iteration_over:
    _numbers      = copy(numbers)
    _extranumbers = copy(extranumbers)
    index = '000000'+str(i)
    index = index[-7:]
    out = open(DIRNAME+'/'+RANDOMID+'_'+index+'.vasp','w+')
    extracomment = ""

    if combination is None:
        if sumOfSmaller is not None:
            mask = sample(range(sumOfSmaller,sumOfSmaller+numbers[elements.index(flipper)]), flipped)
        else:
            mask = sample(range(len(lines)), flipped)
    else:
        mask = combination
    
    NEWADDED = False
    for m in mask:
        if symbol not in elements:
            _numbers[_extranumbers[m]] -= 1
            _extranumbers[m] = len(elements)
            NEWADDED = True
        else:
            _numbers[_extranumbers[m]] -= 1
            _extranumbers[m] = int(np.argwhere(np.array(elements)==symbol))
            _numbers[_extranumbers[m]] += 1
    
    label = ""
    if symbol not in elements:
        for e,n in zip(elements,_numbers):
            label += "%s_%5.3f "%(e,float(n)/(1.0+np.sum(_numbers)))
        label += "%s_%5.3f "%(symbol,1.0/(1.0+np.sum(_numbers)))
    else:
        for e,n in zip(elements,_numbers):
            label += "%s_%5.3f "%(e,float(n)/np.sum(_numbers))
    out.write(label+'\n')
    out.write(data[0])
    out.write(3*" ")
    
    for e in elements:
        out.write(e+3*" ")
    if symbol not in elements:
        out.write(symbol+'\n')
    else:
        out.write("\n")
    
    out.write(3*" ")
    for n in _numbers:
        out.write(str(n)+3*" ")
    if symbol not in elements:
        out.write(str(flipped)+'\n')
    else:
        out.write("\n")
    
    out.write(data[1]+'\n')
    for i,_ in enumerate(elements):
        for j,line in enumerate(lines):
            if _extranumbers[j]==i:
                out.write(line+'\n')
    
    if NEWADDED:
        for j,line in enumerate(lines):
            if _extranumbers[j]==len(elements):
                out.write(line+'\n')
    out.close()
