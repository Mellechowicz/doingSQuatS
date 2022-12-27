#!/usr/bin/python3

from counter import Counter
from time import sleep


A=Counter(position=3)
A.initiate()
print('Placeholder')
print('Placeholder')

for i in range(100):
    A.update()
    sleep(0.1)
