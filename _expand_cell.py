#!/usr/bin/python3

import numpy as np
from sys import argv
from random import sample
import re
from copy import copy

if len(argv) < 4:
    print("""Provide: 
            (  i) POSCAR file
            ( ii) number of flips
            (iii) flip-to atom symbol
            ( iv) flip only atoms of this type""")
    exit(-1)

POSCARname = argv[1]
flipped = int(argv[2])
symbol  = argv[3]
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
                numbers.append(np.int(n))
        elif i == 7:
            extranumbers = []
            for i,n in enumerate(numbers):
                for j in range(n):
                    extranumbers.append(i)
            data[1]=line
        else:
            if len(re.sub(r"\s+", "", line, flags=re.UNICODE)) != 0:
                lines.append(line)

extracomment = "    randomized sample #%d"%np.random.randint(2**20)
if flipper is None:
    mask = sample(range(len(lines)), flipped)
else:
    if flipper in elements:
        sumOfSmaller = int(np.sum(numbers[0:elements.index(flipper)]))
        mask = sample(range(sumOfSmaller,sumOfSmaller+numbers[elements.index(flipper)]), flipped)
        extracomment = "   Only "+flipper+" was flipped!"+extracomment
    else:
        mask = sample(range(len(lines)), flipped)
        extracomment = "   Wrong type of element-to-be-flipped!"+extracomment

NEWADDED = False
for m in mask:
    if symbol not in elements:
        numbers[extranumbers[m]] -= 1
        extranumbers[m] = len(elements)
        NEWADDED = True
    else:
        numbers[extranumbers[m]] -= 1
        extranumbers[m] = int(np.argwhere(np.array(elements)==symbol))
        numbers[extranumbers[m]] += 1

label = ""
if symbol not in elements:
    for e,n in zip(elements,numbers):
        label += "%s_%5.3f "%(e,float(n)/(1.0+np.sum(numbers)))
    label += "%s_%5.3f "%(symbol,1.0/(1.0+np.sum(numbers)))
else:
    for e,n in zip(elements,numbers):
        label += "%s_%5.3f "%(e,float(n)/np.sum(numbers))
print(label+extracomment)
print(data[0],end='')
print(3*" ",end='')

for e in elements:
    print(e,end=3*" ")
if symbol not in elements:
    print(symbol)    
else:
    print("")

print(3*" ",end='')
for n in numbers:
    print(n,end=3*" ")
if symbol not in elements:
    print(flipped)    
else:
    print("")

print(data[1])
for i,_ in enumerate(elements):
    for j,line in enumerate(lines):
        if extranumbers[j]==i:
            print(line)

if NEWADDED:
    for j,line in enumerate(lines):
        if extranumbers[j]==len(elements):
            print(line)
