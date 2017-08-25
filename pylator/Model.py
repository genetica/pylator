import ctypes
import logging
import multiprocessing as mp
import time

from contextlib import closing

import numpy as np

info = mp.get_logger().info

class Model(mp.Process):
    __count = 0
    def __init__(self, name, args):
        mp.Process.__init__(self)
        
        flags, simData, connectivityMatrix = args

        
        #self.crit = logs[0]#mp.get_logger().critical
        
        self.name = name
        self.id = Model.__count
        self.simData = simData
        self.connectivityMatrix = connectivityMatrix
        self.flags = flags
        Model.__count += 1
        self.createModuleDictionary()
        info("Initialised {}".format(self.name))

    def createModuleDictionary(self):
        self.moduleData = {}

        # simulation specific
        self.moduleData['iteration'] = int(self.simData["iteration"].value)
        
        # constants
        if (self.name == "A"):
            self.simData["start"] = self.simData["a_start"].value

        if (self.name == "B"):
            self.simData["start"] = self.simData["b_start"].value

        self.moduleData['start'] = self.simData['start']

        # input outputs
        self.moduleData["array"] = np.frombuffer(self.simData["array_ptr"])

    
    def updateSimulationVariables(self):
        self.moduleData['iteration'] = int(self.simData["iteration"].value)

    def updateInputOutputVariables(self):
        self.moduleData["array"] = np.frombuffer(self.simData["array_ptr"])

    def updateVariables(self):
        self.updateSimulationVariables()
        self.updateInputOutputVariables()
    
    def run(self):
        info("Run")
        #model = model_class(name, simData, connectivityMatrix)

        #modelData = model.createModuleDictionary(simData)

        while self.flags["simulation_active"].is_set():

            self.flags["simulation_next"].wait()
            
            t1 = time.time()
            self.updateVariables()
            
            self.execute(self.moduleData)

            t2 = time.time()
            info(t2 - t1)

            self.flags["Module_done"].wait()
            self.flags["simulation_result"].wait()



        #self.execute(self.moduleData)

    def execute(self, simData):
        raise ValueError(self.name, "No Model has been instantiated.")

if __name__ == '__main__':

    #  NOT valid test currently


    logger = mp.log_to_stderr()
    #logger.setLevel(logging.CRITICAL)
    logger.setLevel(logging.INFO)


    N, M = 15000, 11
    base_ptr = mp.RawArray(ctypes.c_double, N)
    arr = np.frombuffer(base_ptr)
    arr[:] = np.array(np.random.uniform(size=N)*1000, np.int)
    arr_orig = arr.copy()


    M1 = Model("test", "path", "cent")
    M1.execute()
    M2 = Model("test", "path", "cent")
    M2.execute()
