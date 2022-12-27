#!/usr/bin/python

from scipy.special import binom
from sys import argv

try:
    N=int(argv[1])
    M=int(argv[2])
except:
    print(1)
    exit()

if M > N//2:
    print(int(binom(N,M+1)))
else:
    print(int(binom(N,M-1)))
