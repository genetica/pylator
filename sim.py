import pylator as pyl
import logging
import numpy as np
import multiprocessing as mp
import ctypes
import time

N = int(1e7)

crit = mp.get_logger().critical
info = mp.get_logger().info


# This is the base 
class Module(pyl.Model):
    def execute(self, simData):

        self.info("Executing my Model {} Iteration {}".format(self.name, simData["iteration"]))

        data = simData["array"]

        offset = int(simData["start"])
        count = 0
        
        while count <= data.size//2:
            count += 1
            if count <= data.size//2 - 1:
                #info('P1 %d', count)
                data[count + offset] = count# + simData["iteration"]#(count * np.sqrt(count )) ** (2.0/ 3.0 ) 

        # #info(data)
        
        # crit("MyModel")
        # info(simData)

def create_sim_data(simData):
    global N
    simData["iteration"] = mp.RawValue(ctypes.c_int, iteration)

    
    a_start = 0
    b_start = N//2

    simData["start"] = "None"
    simData["a_start"] = mp.RawValue(ctypes.c_int, a_start)
    simData["b_start"] = mp.RawValue(ctypes.c_int, b_start)
    
    
    # create shared array
    base_ptr = mp.RawArray(ctypes.c_int64, N)
    arr = np.frombuffer(base_ptr)
    arr[:] = np.array(np.random.uniform(size=N)*1000, np.int64)
    simData["array_ptr"] = base_ptr
    simData["array"] = arr

    return simData



if __name__ == "__main__":
    

    logger = mp.log_to_stderr()
    logger.setLevel(logging.INFO)

    flags = {}
    flags["simulation_active"] = mp.Event()
    flags["simulation_next"] = mp.Barrier(3)

    flags["Module_done"] = mp.Barrier(3)
    flags["simulation_result"] = mp.Barrier(3)

    flags["simulation_active"].set()

    iteration = 0

    simData = {}
    simData = create_sim_data(simData)   

    
    connectivityMatrix = []


    #p1 = mp.Process(name="A", target=Model, args=(Model, flags, "A", simData, connectivityMatrix,))
    p1 = Module(name="A", args=(flags, simData, connectivityMatrix,))
    p2 = Module(name="B", args=(flags, simData, connectivityMatrix,))
    #p2 = mp.Process(name="B", target=ModeltartModule, args=(Model, flags, "B", simData, connectivityMatrix,))
    info("Processes created")
    p1.start()
    p2.start()
    info("Processes started")
    #simData["array"] = np.frombuffer(simData["array_ptr"])

    flags["simulation_next"].wait()
    t1 = time.time()
    for i in range(3):
        flags["Module_done"].wait()
        t2 = time.time()
        info(t2 - t1)
        info(simData["array"][1])
        info(simData["array"][int(N//2-1)])
        info(simData["array"][int(N//2+1)])
        info(simData["array"][int(N - 1)])
        flags["simulation_result"].wait()
        
        simData["iteration"].value += 1

        flags["simulation_next"].wait()
        t1 = time.time()

    flags["simulation_active"].clear()
    flags["Module_done"].wait()
    flags["simulation_result"].wait()
    #A = startModule(Model, "A", logs, simData, connectivityMatrix)
    #B = startModule(Model, "B", logs, simData, connectivityMatrix)

    #A.execute()
    #B.execute()