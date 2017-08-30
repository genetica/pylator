import pylator as pyl
import logging
import multiprocessing as mp
import ctypes
import numpy as np

# Constants

# Available loggers
crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

class MyScheduler(pyl.Scheduler):
    # This is temporary and should be generated automatically
    # by the simulator class.
    def create_sim_data(self):
        iteration = 0
        self.simData["/simulation/iteration"] = mp.RawValue(ctypes.c_int, iteration)
        
        longestDelay = 0.0
        self.simData["/simulation/longestDelay"] = mp.Value(ctypes.c_float, longestDelay)

        buffer_current = 0
        self.simData["/simulation/buffer_current"] = mp.RawValue(ctypes.c_int, buffer_current)
      
        # create shared array
        #base_ptr = mp.RawArray(ctypes.c_int64, N)
        #arr = np.frombuffer(base_ptr)
        #arr[:] = np.array(np.random.uniform(size=N)*1000, np.int64)
        #simData["array_ptr"] = base_ptr
        #simData["array"] = arr

        
# Simulator Input Variables
script_info = [
                 ["module1",        "./path/module1.py"],
                 ["module2",        "./path/module2.py"],
                 ["module3",        "./path/module3.py"],
                 ["module4",        "./path/module4.py"],
                 ]

simData = {}
connectivityMatrix = []
# Usage of these inputs are not complete in class yet thus in modules the following functions must be
# implemented manually
# def createModuleDictionary(self)
# def updateSimulationVariables(self):
# def updateInputVariables(self):
# def setOutputVariables(self):
# def updateOutputVariables(self):

# All modules should have the following function:
# def initialise(self, simData):
# def execute(self, simData):
# def finalise(self, simData):


# Create simulator
sim = MyScheduler(script_info, simData, connectivityMatrix)

if __name__ == "__main__":   
    #FATAL/DEBUG/INFO
    # Set logging of simulator
    sim.set_logging(logging.INFO)
    # Start simulation
    sim.run()
  