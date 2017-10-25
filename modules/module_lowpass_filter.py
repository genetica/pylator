import sys
import pylator as pyl
import logging
import numpy as np
import multiprocessing as mp
import ctypes
import time
import socket
import os
from collections import deque


crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

class Module(pyl.Model):
    #Temporary function should be internal
    def createModuleDictionary(self):
        self.moduleData = {}
        # simulation specific
        self.moduleData["/simulation/continuous"] = False
        self.moduleData["/simulation/iteration"] = self.simData["/simulation/iteration"].value
        self.moduleData["/simulation/time_step"] = self.simData["/simulation/time_step"].value
        self.moduleData["/simulation/buffer_current"] = self.simData["/simulation/buffer_current"].value


        # Constants as defined from global variables.
        self.moduleData["/inputs/frequency"]  = self.simData["/user/signal/frequency"].value
        self.moduleData["/inputs/amplitude"]  = self.simData["/user/signal/amplitude"].value
        self.moduleData["/inputs/sampling_period"] = self.simData["/user/signal/sampling_period"].value
        
        self.moduleData["/inputs/signal_type"] = "sine"
        # Inputs
        self.moduleData["/inputs/keypress"] = self.simData["/control/outputs/keypress"][1].value

        self.conn = self.connectivityMatrix["/" + self.__name__ + "/inputs/signal"]
        self.moduleData["/inputs/signal"]  = self.simData[self.conn][1].value
        
        # Outputs
        self.moduleData["/outputs/signal"] = self.simData["/" + self.__name__ + "/outputs/signal"][1].value

    def updateInputVariables(self):
        # check what buffer frame input to use
        buff_frame = self.moduleData["/simulation/buffer_current"]
        if buff_frame == 0:
            buff_frame = 1
        else:
            buff_frame = 0
        self.moduleData["/inputs/keypress"] = self.simData["/control/outputs/keypress"][buff_frame].value
        self.moduleData["/inputs/signal"] = self.simData[self.conn][buff_frame].value
    def assignOutputVariables(self):
        # Assign pointer to output shared memory.
        buff_frame = self.moduleData["/simulation/buffer_current"]
        self.moduleData["/outputs/signal"] = self.simData["/" + self.__name__ + "/outputs/signal"][buff_frame].value
    def updateOutputVariables(self):
        #Set value for shared variables that is not matrices, maybe not necessary
        buff_frame = self.moduleData["/simulation/buffer_current"]       
        self.simData["/" + self.__name__ + "/outputs/signal"][buff_frame].value = self.moduleData["/outputs/signal"]
        

    def initialise(self, simData):
        # Inputs using default values, set as constants (Generated)

        # User data
        simData["/self/previous_output"] = 0

        
        self.buffer = deque()
        for i in range(5):
            self.buffer.append(0)

    def execute(self, simData):
        
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))


        self.buffer.append(simData["/inputs/signal"])
        simData["/outputs/signal"] = (np.array(self.buffer)[:-1]*np.array([1 , 2, 3, 2, 1])).sum()/9
        self.buffer.popleft()
        
