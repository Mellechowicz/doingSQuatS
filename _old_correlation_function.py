#!/usr/bin/python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
import os
import re

from spglib import get_symmetry_dataset

from JorGpi.POSCARloader import POSCARloader

from itertools import product

from counter import Counter

def correl(*args, p=1):
    corr = 0.0
    for i,arg in enumerate(args):
        corr += 0.0
    return 0
    
def localC(*args):
    for argI,argJ in product(args,repeat=2):
        if argI != argJ:
            return 0.0
    return 1.0

pwr = 1.0
result={}
equivalents={}
equivalentsresults={}
cntr = Counter(limit=len(argv[1:]),PREFIX="",SUFFIX=" files done.")
cntr.initiate()
for arg in argv[1:]:
    loader = POSCARloader(arg)
    loader.parse()
    equivalents[arg] = len(set(get_symmetry_dataset(loader(0)['cellSymmetry'])['equivalent_atoms']))
    idealCorrelation = 0.0
    for population in loader(0)['cellAtoms']:
        idealCorrelation += np.power(population/np.sum(loader(0)['cellAtoms']),2)

    penalty = 0.0
    distances = {}
    for atomI in loader(0)['cell']:
        for atomJ,i,j,k in product(loader(0)['cell'],[-1,0,1],[-1,0,1],[-1,0,1]):
            d = np.around(np.linalg.norm(atomI[1]-atomJ[1]-i*loader(0)['directions'][0]-j*loader(0)['directions'][1]-k*loader(0)['directions'][2]),decimals=3)
            if d in distances:
                distances[d][0] += localC(atomI[0],atomJ[0])
                distances[d][1] += 1
            else:
                distances[d] = [localC(atomI[0],atomJ[0]),1]
    for i,d in enumerate(sorted(distances.keys())):
        if i == 0:
            continue
        penalty += np.power(float(distances[d][0])/distances[d][1] - idealCorrelation,2)/np.power(i,pwr)
    del distances
    result[arg]=penalty
    equivalentsresults[arg]=penalty*equivalents[arg]
    cntr.update()

with open('correlation_report_penalty.txt','w+') as corr:
    corr.write("#File Number_of_equivalent_atoms Penalty Effective_penalty\n")
    for name,_ in sorted(result.items(), key=lambda item: item[1]):
        corr.write(f'{name:40} {equivalents[name]:4d} {result[name]:6.3e} {equivalents[name]*result[name]:6.3e}\n')

with open('mod_correlation_report_penalty.txt','w+') as corr:
    corr.write("#File Number_of_equivalent_atoms Penalty Effective_penalty\n")
    for name,_ in sorted(equivalentsresults.items(), key=lambda item: item[1]):
        corr.write(f'{name:40} {equivalents[name]:4d} {result[name]:6.3e} {equivalents[name]*result[name]:6.3e}\n')

exit()
