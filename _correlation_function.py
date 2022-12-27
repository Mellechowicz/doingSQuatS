#!/usr/bin/python3

from sys import argv
import numpy as np
import os
import re

from spglib import get_symmetry_dataset

from JorGpi.POSCARloader import POSCARloader

from itertools import product

from counter import Counter

if len(argv) < 2:
    print('Feed me with:')
    print('(i)   name of  input directory')
    print('(ii)  radial correlation directory (optional)')
    print('(iii) radial correlation display   (optional)')
    exit(-1)

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
if len(argv) >= 3:
    radial_correlation={}
    full_correlation={}
    atom_identification={}
directory = os.fsencode(argv[1])
cntr = Counter(limit=len(os.listdir(directory)),PREFIX='Processed ',SUFFIX=' files.')
cntr.initiate()
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith(".vasp"):
        print("Omitting: "+argv[1]+'/'+filename+" (Is not a *.vasp file!)")
        cntr.iterate_position()
        continue
    loader = POSCARloader(argv[1]+'/'+filename)
    try:
        loader.parse()
    except (IndexError,TypeError) as e:
        print(e,end=': For ')
        print(filename, end='  ')
        print('('+argv[1]+'/'+filename+')')
        cntr.iterate_position()

    equivalents[filename] = len(set(get_symmetry_dataset(loader(0)['cellSymmetry'])['equivalent_atoms']))
    idealCorrelation = 0.0
    for population in loader(0)['cellAtoms']:
        idealCorrelation += np.power(population/np.sum(loader(0)['cellAtoms']),2)

    penalty = 0.0
    distances = {}
    max_distance = 1e300
    for direction in loader(0)['directions']:
        lattice_constant = np.linalg.norm(direction)
        if lattice_constant < max_distance:
            max_distance = lattice_constant

    radial_correlation[filename] = []
    atom_identification[filename] = []
    for atomID,atomI in enumerate(loader(0)['cell']):
        if len(argv) >= 3:
            local_correlation={}
            atom_identification[filename].append(atomI[0])
            atom_types = []
        for atomJ,i,j,k in product(loader(0)['cell'],[-1,0,1],[-1,0,1],[-1,0,1]):
            d = np.around(np.linalg.norm(atomI[1]-atomJ[1]-i*loader(0)['directions'][0]-j*loader(0)['directions'][1]-k*loader(0)['directions'][2]),decimals=3)
            if d > max_distance:
                continue
            if d in distances:
                distances[d][0] += localC(atomI[0],atomJ[0])
                distances[d][1] += 1
            else:
                distances[d] = [localC(atomI[0],atomJ[0]),1]
            if len(argv) < 3:
                continue
            atom_types.append(atomJ[0])
            atom_types = list(set(atom_types))
            if d in local_correlation:
                local_correlation[d][0] += localC(atomI[0],atomJ[0]) 
                local_correlation[d][1] += 1
            else:
                local_correlation[d] = [localC(atomI[0],atomJ[0]),1]
        if len(argv) >= 3:
            pointstyle = {symbol: i for i,symbol in enumerate(list(set(atom_types)))}
            for d in local_correlation.keys():
                radial_correlation[filename].append([d,float(local_correlation[d][0])/local_correlation[d][1],pointstyle[atomI[0]]])
    for i,d in enumerate(sorted(distances.keys())):
        if i == 0:
            full_correlation[filename] = [[1.0,1.0]]
            continue
        penalty += np.power(float(distances[d][0])/distances[d][1] - idealCorrelation,2)/np.power(i,pwr)
        full_correlation[filename].append([d,float(distances[d][0])/distances[d][1]])
    del distances
    result[filename]=penalty
    equivalentsresults[filename]=penalty*equivalents[filename]
    cntr.update()

with open(argv[1]+'/correlation_report_penalty.txt','w+') as corr:
    corr.write("#File Number_of_equivalent_atoms Penalty Effective_penalty\n")
    for name,_ in sorted(result.items(), key=lambda item: item[1]):
        corr.write(f'{name:40} {equivalents[name]:4d} {result[name]:6.3e} {equivalents[name]*result[name]:6.3e}\n')

with open(argv[1]+'/mod_correlation_report_penalty.txt','w+') as corr:
    corr.write("#File Number_of_equivalent_atoms Penalty Effective_penalty\n")
    for name,_ in sorted(equivalentsresults.items(), key=lambda item: item[1]):
        corr.write(f'{name:40} {equivalents[name]:4d} {result[name]:6.3e} {equivalents[name]*result[name]:6.3e}\n')

if len(argv) < 2:
    exit()

try:
    os.mkdir(argv[1]+'/'+argv[2])
except FileExistsError:
    print("Overwritting data in "+argv[2]+"!!!!!")
for filename in radial_correlation.keys():
    np.savetxt(argv[1]+'/'+argv[2]+'/'+'decomposed_'+filename[:-5]+'.txt',np.array(radial_correlation[filename]))
for filename in full_correlation.keys():
    np.savetxt(argv[1]+'/'+argv[2]+'/'+filename[:-5]+'.txt',np.array(full_correlation[filename]))

if len(argv) < 3:
    exit()

import matplotlib.pyplot as plt
types_of_points = ['o','*','s','p','P','H','^','X','D','v','+']
colours         = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan','k']

if '.png' in argv[3]:
    figname = argv[1]+'/'+argv[3]
else:
    figname = argv[1]+'/'+argv[2]+'/'+'radial.png'

fig,axs = plt.subplots(2,1)

for first,filename in enumerate(radial_correlation.keys()):
    data = np.array(radial_correlation[filename])
    for i,element in enumerate(list(set(atom_identification[filename]))):
        mask = np.argwhere(data[:,2]==i)
        axs[0].plot(data[mask,0],data[mask,1],types_of_points[i],c=colours[i],alpha=0.1,ms=8)
        if first == 0:
            axs[0].plot([],[],types_of_points[i],c='k',ms=13,label=element)
    data = np.array(full_correlation[filename])
    if first < 40:
        axs[1].plot(data[:,0],data[:,1],'o',label=filename[:-5],alpha=0.5,ms=9)
    else:
        axs[1].plot(data[:,0],data[:,1],'o',alpha=0.4,ms=9)

axs[0].legend()
axs[1].set_ylim((0.0,1.0))
axs[1].legend(fontsize=5,ncol=3)
prob = np.array((0.59,0.41))
ideal = np.sum(prob*prob)
axs[0].arrow(axs[0].get_xlim()[0],ideal,axs[0].get_xlim()[1]-axs[0].get_xlim()[0],0.0)
axs[1].arrow(axs[1].get_xlim()[0],ideal,axs[1].get_xlim()[1]-axs[1].get_xlim()[0],0.0)
axs[1].set_xlabel('coordination sphere radii, R (A)')
axs[0].set_ylabel('ideal value: '+str(ideal))
axs[1].set_ylabel('correlation function, C (1)')
#plt.show()
plt.savefig(figname,dpi=300)
