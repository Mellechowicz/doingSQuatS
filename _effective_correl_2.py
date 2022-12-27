#!/usr/bin/python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
import os
import re

from JorGpi.POSCARloader import POSCARloader

from itertools import product

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

pwr = 0.2
result={}
for arg in argv[1:]:
    loader = POSCARloader(arg)
    loader.parse()
    deviations = [ ]
    ALL=np.sum(loader(0)['cellAtoms'])
    idealCorrelation = 0.0
    for population in loader(0)['cellAtoms']:
        idealCorrelation += np.power(population/ALL,2)

    for population in loader(0)['cellAtoms'][:-1]:
        deviations.append(np.linspace(population-4,population+4,1001))

    distances = {}
    for atomI,atomJ,i,j,k in product(loader(0)['cell'],loader(0)['cell'],[-1,0,1],[-1,0,1],[-1,0,1]):
        d = np.around(np.linalg.norm(atomI[1]-atomJ[1]-i*loader(0)['directions'][0]-j*loader(0)['directions'][1]-k*loader(0)['directions'][2]),decimals=1)
        if d in distances:
            distances[d][0] += localC(atomI[0],atomJ[0])
            distances[d][1] += 1
        else:
            distances[d] = [localC(atomI[0],atomJ[0]),1]

    result[arg]=[]
    for deviation in product(*deviations,np.linspace(-0.1,0.1,201)):
        dev = np.array(deviation)
        dev[-1] += ALL - np.sum(dev[:-1])
        idealCorrelation = 0.0
        for d in dev:
            idealCorrelation += np.power(d/np.sum(dev),2)
	
        penalty = 0.0
        for i,d in enumerate(sorted(distances.keys())):
            if i == 0 or i > 8:
                continue
            penalty += np.power(float(distances[d][0])/distances[d][1] - idealCorrelation,2)/np.power(i,pwr)
        result[arg].append(np.array([*dev,penalty]))
    result[arg] = np.array(result[arg])
    print('%30s  %2.5f  %2.5f'%(arg,*(ALL*result[arg][np.argmin(result[arg][:,2])][:-1]/np.sum(result[arg][np.argmin(result[arg][:,2])][:-1])),))

#result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
#for name in result:
#    print(name,result[name])
