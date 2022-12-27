#!/usr/bin/python3

from counter import Counter
from time import sleep

A = Counter(10)
A.initiate()

for i in range(10):
    A.update()
    sleep(0.2)
