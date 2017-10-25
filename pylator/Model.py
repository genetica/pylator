"""

    Model class:
    This class are used to create a Module to be used by the
    pylator scheduler.


    Original Created: Gene Stoltz
    Original Date: 25-07-2017

"""

import ctypes
import logging
import multiprocessing as mp
import time

from contextlib import closing

import numpy as np

#logger = mp.log_to_stderr()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger.handlers[0].setFormatter(formatter)
debug = mp.get_logger().debug
info = mp.get_logger().info
crit = mp.get_logger().critical

class Model(mp.Process):
    __count = 0
    def __init__(self, name, args):
        mp.Process.__init__(self)
        
        flags, simData, connectivityMatrix = args
      
        #self.crit = logs[0]#mp.get_logger().critical
        
        self.__name__ = name
        self.name = name
        self.id = Model.__count
        self.simData = simData
        self.connectivityMatrix = connectivityMatrix
        self.flags = flags

        self.p_longestDelay = 0.0
        Model.__count += 1

        self.createModuleDictionary()
        info("Initialised {}".format(self.name))

    def initialise(self, simData):
        pass

    def finalise(self, simData):
        pass


    def createModuleDictionary(self):
        # Need to be generic dictionary specific for module
        self.moduleData = {}
        crit("ERROR createModuleDictionary")
        pass
    
    def updateSimulationVariables(self):
        self.moduleData['/simulation/iteration'] = int(self.simData["/simulation/iteration"].value)
        self.moduleData['/simulation/buffer_current'] = int(self.simData["/simulation/buffer_current"].value)
        self.moduleData['/simulation/longestDelay'] = self.simData["/simulation/longestDelay"].value

        buff_frame = self.moduleData['/simulation/buffer_current']
        if buff_frame == 0:
            buff_frame = 1
        else:
            buff_frame = 0
    
        self.moduleData["/control/inputs/keypress"] = int(self.simData["/control/outputs/keypress"][buff_frame].value)
        self.moduleData["/control/outputs/keypress"] = 0

    def setSimulationVariables(self):
        buff_frame = self.moduleData['/simulation/buffer_current']
        if (self.moduleData["/control/outputs/keypress"] != 255) and (self.moduleData["/control/outputs/keypress"] != 0):
            self.simData["/control/outputs/keypress"][buff_frame].value = self.moduleData["/control/outputs/keypress"]
        self.moduleData["/control/inputs/keypress"] = 0


    def updateInputVariables(self):
        # Need to be generic dictionary specific for module
        buff_frame = self.moduleData['/simulation/buffer_current']
        if buff_frame == 0:
            buff_frame = 1
        else:
            buff_frame = 0
        
        crit("ERROR updateVariables")
        pass

            
    def assignOutputVariable(self):
        self.setOutputVariables()
        
    def setOutputVariables(self):
        # check what buffer frame output to use
        buff_frame = self.moduleData['/simulation/buffer_current']       
        # Need to be generic dictionary specific for module
        #crit("ERROR setOutputVariables")
        pass

    def updateOutputVariables(self):
        # might need to reupdated shared dictionary, depends... Uhmmm.
        buff_frame = self.moduleData['/simulation/buffer_current']
        pass        
        

    def preExecutionUpdateVariables(self):
        self.updateSimulationVariables()
        self.updateInputVariables()
        self.setOutputVariables()

    def postExecutionUpdateVariables(self):
        self.setSimulationVariables()
        self.updateOutputVariables()
        
    
    def run(self):
        info("Run")       
        self.initialise(self.moduleData)

        

        while self.flags["simulation_active"].is_set():

            self.flags["simulation_next"].wait()

            t1 = time.time()
            self.preExecutionUpdateVariables()
            if (self.moduleData["/simulation/continuous"]):
                tc1 = time.time()
                self.execute(self.moduleData)
                tc2 = time.time()
                td = tc2 - tc1
                #info("{:.3f}".format(td))
                self.setSimulationVariables()
                if (self.p_longestDelay > 0.001):
                    delay = td
                    while delay + 2*td < self.p_longestDelay:
                        tc1 = time.time()
                        self.execute(self.moduleData)
                        tc2 = time.time()
                        td = tc2 - tc1
                        delay += td
                        self.setSimulationVariables()

                self.postExecutionUpdateVariables()
                t2 = time.time()
                info("{:.3f}".format(t2 - t1))
            else:
                self.execute(self.moduleData)
                self.postExecutionUpdateVariables()
                t2 = time.time()
                td = t2 - t1
                info("{:.3f}".format(td))

            if td > self.simData["/simulation/longestDelay"].value:
                self.simData["/simulation/longestDelay"].value = td 

            self.flags["Module_done"].wait()
            self.p_longestDelay = self.simData["/simulation/longestDelay"].value
            self.flags["simulation_result"].wait()

            

        self.finalise(self.moduleData)

        #self.execute(self.moduleData)

    def execute(self, simData):
        raise ValueError(self.name, "No Model has been instantiated.")

if __name__ == '__main__':

    #  NOT valid test currently

    logger = mp.log_to_stderr()
    #logger.setLevel(logging.CRITICAL)
    logger.setLevel(logging.INFO)