#!/usr/bin/python3

import numpy as np
from sys import argv
from random import sample
import re
from copy import copy

if len(argv) < 4:
    print("""Provide: 
            (  i) POSCAR file
            ( ii) gaussian sigma directions
            (iii) gaussian sigma positions""")
    exit(-1)

POSCARname = argv[1]
sigmaD = float(argv[2])
sigmaP = float(argv[3])

data = ["",""]
directions = []
elements = []
numbers  = []
extranumbers = None
lines    = []
comment  = ""
with open(POSCARname,'r+') as poscar:
    for i,line in enumerate(poscar.read().split('\n')):
        if i == 0:
            comment = re.sub(r"\n", "", line, flags=re.UNICODE)
        elif i == 1:
            data[0]=line
        elif i < 5:
            directions.append(np.fromstring(line,sep=" "))
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
                lines.append(np.fromstring(line,sep=" "))

extracomment = "    randomized sample #%d"%np.random.randint(2**20)
label = ""
for e,n in zip(elements,numbers):
    label += "%s_%5.3f "%(e,float(n)/np.sum(numbers))
print(label+extracomment+" || OLD: "+comment)
print(data[0])

for direction in directions:
    print(''.join(["  % 15.8f"%f for f in direction+np.random.normal(0.0,sigmaD,3)]))

print(3*" ",end='')

for e in elements:
    print(e,end=3*" ")
else:
    print("")

print(3*" ",end='')
for n in numbers:
    print(n,end=3*" ")
else:
    print("")

print(data[1])
for i,elements in enumerate(elements):
    for j,line in enumerate(lines):
        print(''.join(["  % 15.8f"%f for f in line+np.random.normal(0.0,sigmaP,3)]))

