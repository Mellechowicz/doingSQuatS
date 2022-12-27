#!/usr/bin/python3

import numpy as np
from sys import argv
from random import sample
import re
from copy import copy
from os import mkdir

if len(argv) < 2:
    print("""Provide: 
            (  i) POSCAR file
            ( ii) number of new structures""")
    exit(-1)

POSCARname = argv[1]
DIRNAME=argv[1]+'.dir'
try:
    mkdir(DIRNAME)
except FileExistsError:
    pass
RANDOMID = str(np.random.randint(100000,999999))

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

for i in range(int(argv[2])):
    _numbers      = copy(numbers)
    _extranumbers = copy(extranumbers)
    index = '000000'+str(i)
    index = index[-7:]
    out = open(DIRNAME+'/'+RANDOMID+'_'+index+'.vasp','w+')
    extracomment = ""
    mask = np.array(range(np.sum(numbers)))
    np.random.shuffle(mask)
    
    NEWADDED = False
   
    label = ""
    for e,n in zip(elements,_numbers):
        label += "%s_%5.3f "%(e,float(n)/np.sum(_numbers))
    out.write(label+'\n')
    out.write(data[0])
    out.write(3*" ")
    
    for e in elements:
        out.write(e+3*" ")
    out.write("\n")
    
    out.write(3*" ")
    for n in _numbers:
        out.write(str(n)+3*" ")
    out.write("\n")
    
    out.write(data[1]+'\n')
    for m in mask:
        out.write(lines[m]+'\n')

    out.close()
