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
    #logger.setLevel(logging.CRITICAL)
    logger.setLevel(logging.INFO)
    #logger.setLevel(logging.FATAL)

    # create shared array
    mgr = mp.Manager()
    #d = mgr.dict()
    d = {}

    N, M = 15000, 11
    #base_ptr = mp.RawArray(ctypes.c_double, N)
    #arr = tonumpyarray(base_ptr)
    #arr[:] = np.array(np.random.uniform(size=N)*1000, np.int)
    #arr_orig = arr.copy()

    arr = np.array(np.random.uniform(size=N)*1000, np.int)

    tmp = np.ctypeslib.as_ctypes(arr)
    shared_arr = mp.RawArray(tmp._type_, tmp)
    print(shared_arr)
    d["array"] = shared_arr


    lst_event = []
    for i in range(5):
        lst_event.append(mp.Event())

    lst_event[0].set()


    value_ptr = mp.RawArray(ctypes.c_int, 2)
    value_ptr[0] = 0
    value_ptr[1] = 0

    d["value"] = [0 , 0]







    p1 = mp.Process(target=exec1, args=(d, lst_event,))
    p2 = mp.Process(target=exec2, args=(d, lst_event,))

    t = time.time()
    p1.start()
    p2.start()

    info("Starting")
    lst_event[3].wait()
    lst_event[4].wait()
    info("All Started")

    lst_event[0].clear()


    lst_event[1].wait()
    lst_event[2].wait()

    time.sleep(1)

    arr = np.ctypeslib.as_array(d["array"])
    #info(arr)
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
    data = np.frombuffer(np.ctypeslib.as_array(ptr_lst["array"]))
    #flags = ptr_lst["flag"]
    flags[3].set()
    info('Exec1 Started')
    count = 0
    #data = tonumpyarray(base_ptr)

    while flags[0].is_set():
        count += 1
        if count <= data.size//2 - 1:
            #info('P1 %d', count)
            data[count] = count#(count * np.sqrt(count )) ** (2.0/3.0)
            
        else:
            #flags[1].set()
            count -= 1
    #ptr_lst["array"] = data
    flags[1].set()
    info(data[0])

def exec2(ptr_lst, flags):
    data = np.ctypeslib.as_array(ptr_lst["array"])
    #flags = ptr_lst["flags"]
    
    flags[4].set()

    info('Exec2 Started')
    count = 0
    #data = tonumpyarray(base_ptr)

    while flags[0].is_set():
        count += 1
        if count <= data.size//2 - 1:
            #info('P2 %d', count)
            data[count + data.size//2] = count#(count * np.sqrt(count )) ** (2.0/ 3.0 ) 
        else:
            #flags[2].set()
            count -= 1
    #ptr_lst["array"] = 0
    #ptr_lst["array"] = data
    
    flags[2].set()
    #info(data)

if __name__ == '__main__':
    #mp.freeze_support()
    for i in range(1):
        t1 = main()
        t2 = time.time()
        print(t2 - t1)