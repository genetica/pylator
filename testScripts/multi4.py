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

def main():
    logger = mp.log_to_stderr()
    logger.setLevel(logging.CRITICAL)
    #logger.setLevel(logging.FATAL)

    # create shared array
    mgr = mp.Manager()
    d = mgr.dict()
    d = {}

    N, M = int(1e7), 11
    base_ptr = mp.RawArray(ctypes.c_double, N)
    arr = tonumpyarray(base_ptr)
    arr[:] = np.array(np.random.uniform(size=N)*1000, np.int)
    arr_orig = arr.copy()

    d["array"] = np.array(np.random.uniform(size=N)*1000, np.int)


    base_ptr2 = mp.RawArray(ctypes.c_double, N)
    arr2 = tonumpyarray(base_ptr2)
    arr2[:] = np.array(np.random.uniform(size=N), np.int)
    arr_orig2 = arr2.copy()

    base_ptr3 = mp.RawArray(ctypes.c_double, N)
    arr3 = tonumpyarray(base_ptr3)
    arr3[:] = np.random.uniform(size=N)
    arr_orig3 = arr3.copy()


    lst_event = []
    for i in range(5):
        lst_event.append(mp.Event())

    lst_event[0].set()

    flag_ptr = mp.RawArray(ctypes.c_bool, 5)
    flag = [0,0,0,0,0]
    flag[0] = True
    flag[1] = False
    flag[2] = False
    flag[3] = False
    flag[4] = False

    #d["flag"] = lst_event

    flag_ptr2 = mp.RawArray(ctypes.c_bool, 5)
    flag2 = flag_ptr2
    flag2[0] = True
    flag2[1] = False
    flag2[2] = False
    flag2[3] = False
    flag2[4] = False

    flag_ptr3 = mp.RawArray(ctypes.c_bool, 5)
    flag3 = flag_ptr3
    flag3[0] = True
    flag3[1] = False
    flag3[2] = False
    flag3[3] = False
    flag3[4] = False


    value_ptr = mp.RawArray(ctypes.c_int, 2)
    value_ptr[0] = 0
    value_ptr[1] = 0

    d["value"] = [0 , 0]

    ptr_lst = []
    ptr_lst.append(base_ptr)
    ptr_lst.append(lst_event)
    ptr_lst.append(value_ptr)

    ptr_lst2 = []
    ptr_lst2.append(base_ptr2)
    ptr_lst2.append(flag_ptr2)
    ptr_lst2.append(value_ptr)
    
    ptr_lst3 = []
    ptr_lst3.append(base_ptr3)
    ptr_lst3.append(flag_ptr3)
    ptr_lst3.append(value_ptr)





    #p1 = mp.Process(target=exec1, args=(d, lst_event,))
    #p2 = mp.Process(target=exec2, args=(d, lst_event,))
    #p3 = mp.Process(target=exec1, args=(ptr_lst2,))
    #p4 = mp.Process(target=exec2, args=(ptr_lst2,))
    #p5 = mp.Process(target=exec1, args=(ptr_lst3,))
    #p6 = mp.Process(target=exec2, args=(ptr_lst3,))
    t = time.time()

    exec1(d, lst_event)
    exec2(d, lst_event)
    #p3.start()
    #p4.start()
    #p5.start()
    #p6.start()

    #p1.join()
    #p2.join()

    #info(arr)
    arr = d["array"]
    crit(arr[0])
    crit(arr[arr.size//2-1])
    crit(arr[arr.size//2])
    crit(arr[arr.size-1])
    
    # write to arr from different processes
    # with closing(mp.Pool(initializer=init, initargs=(shared_arr,))) as p:
    #     # many processes access the same slice
    #     stop_f = N // 10
    #     p.map_async(f, [slice(stop_f)]*M)

    #     # many processes access different slices of the same array
    #     assert M % 2 # odd
    #     step = N // 10
    #     p.map_async(g, [slice(i, i + step) for i in range(stop_f, N, step)])
    # p.join()
    # assert np.allclose(((-1)**M)*tonumpyarray(shared_arr), arr_orig)
    return t

def tonumpyarray(mp_arr):
    return np.frombuffer(mp_arr)

def exec1(ptr_lst, flags):
    data = ptr_lst["array"]
    #flags = ptr_lst["flag"]
    flags[3].set()
    info('Exec1 Started')
    
    #data = tonumpyarray(base_ptr)

    for count in range(data.size//2):
        if count <= data.size//2 - 1:

            #info('P1 %d', count)
            # lst = []
            # for i in range(count):
            #     if (i%2 == 0):
            #         lst.append(i)
            data[count] = count#(count * np.sqrt(count )) ** (2.0/3.0)

    #info(ptr_lst["array"])

def exec2(ptr_lst, flags):
    data = ptr_lst["array"]
    #flags = ptr_lst["flags"]
    
    flags[4].set()

    info('Exec2 Started')
    
    #data = tonumpyarray(base_ptr)

    for count in range(data.size//2):
        if count <= data.size//2 - 1:
            #info('P2 %d', count)
            # lst = []
            # for i in range(count):
            #     if (i%2 == 0):
            #         lst.append(i)

            data[count + data.size//2] = count#(count * np.sqrt(count )) ** (2.0/ 3.0 ) 
    #info(ptr_lst["array"])

if __name__ == '__main__':
    #mp.freeze_support()
    for i in range(1):
        t1 = main()
        t2 = time.time()
        print(t2 - t1)