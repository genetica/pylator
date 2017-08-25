import ctypes
import logging
import multiprocessing as mp
import time

from contextlib import closing

import numpy as np

t1 = time.time()

N, M = 15000, 11

arr = np.random.uniform(size=N)
#arr_orig = arr.copy()
count = 0
while count < arr.size//2:
    count += 1
    lst = []
    for i in range(count):
        if (i%2 == 0):
            lst.append(i)
    arr[count] = (count * np.sqrt(count )) ** (2.0/3.0)

count = 0
while count  < arr.size//2:
    count += 1
    lst = []
    for i in range(count):
        if (i%2 == 0):
            lst.append(i)
    arr[count + arr.size//2 - 1] = (count * np.sqrt(count )) ** (2.0/3.0)

t2 = time.time()
print(t2 - t1)
        