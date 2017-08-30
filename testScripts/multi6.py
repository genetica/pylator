import ctypes
import logging
import multiprocessing as mp
import time

from contextlib import closing

import numpy as np

t1 = time.time()

info = mp.get_logger().info
crit = mp.get_logger().critical

#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import weakref



def main():
    logger = mp.log_to_stderr()
    logger.setLevel(logging.CRITICAL)
    #logger.setLevel(logging.FATAL)

    # create shared array
    N, M = int(1e6), 11
    base_ptr = mp.RawArray(ctypes.c_int64, N)
    arr = np.frombuffer(base_ptr)
    arr[:] = np.array(np.random.uniform(size=N)*1000, np.int64)
    #arr_orig = arr.copy()

    #print("info")
    #print(repr(arr))
    #print(repr(base_ptr))
    #print(id(arr))
    #print(id(base_ptr))
    #print("done")

    lst_event = []
    for i in range(5):
        lst_event.append(mp.Event())

    lst_event[0].set()



    ptr_lst = {}
    ptr_lst["array"] = base_ptr
    ptr_lst["events"] = lst_event


    #ptr_lst = []
    #ptr_lst.append(base_ptr)
    #ptr_lst.append(lst_event)

    p1 = mp.Process(target=exec1, args=(ptr_lst,))
    p2 = mp.Process(target=exec2, args=(ptr_lst,))

    t = time.time()

    exec1(ptr_lst)
    exec2(ptr_lst)

    #info(arr)
    #arr = np.frombuffer(ptr_lst[0])
    arr = np.frombuffer(ptr_lst["array"])
    #print(weakref.ref(arr))
    #crit(arr[1])
    #crit(arr[arr.size//2-1])
    #crit(arr[arr.size//2])
    #crit(arr[arr.size//2+1])
    #crit(arr[arr.size-1])
    
    return t


def exec1(ptr_lst):
    #base_ptr = ptr_lst[0]
    #flags = ptr_lst[1]

    base_ptr = ptr_lst["array"]
    flags = ptr_lst["events"]

    

    flags[3].set()
    info('Exec1 Started')
    count = 0
    data = np.frombuffer(base_ptr)

    #crit(id(base_ptr))
    #crit(id(data))

    while count <= data.size//2:
        count += 1
        if count <= data.size//2 - 1:
            #info('P1 %d', count)
            data[count] = count#(count * np.sqrt(count )) ** (2.0/3.0)
    #info(data)

def exec2(ptr_lst):
    #base_ptr = ptr_lst[0]
    #flags = ptr_lst[1]
    
    base_ptr = ptr_lst["array"]
    flags = ptr_lst["events"]

    flags[4].set()

    info('Exec2 Started')
    count = 0
    data = np.frombuffer(base_ptr)

    #crit(id(base_ptr))
    #crit(id(data))

    while count <= data.size//2:
        count += 1
        if count <= data.size//2 - 1:
            #info('P1 %d', count)
            data[count + data.size//2] = count#(count * np.sqrt(count )) ** (2.0/ 3.0 ) 
    #info(data)

if __name__ == '__main__':
    #mp.freeze_support()
    for i in range(5):
        t1 = main()
        t2 = time.time()
        print(t2 - t1)