import sys
import pylator as pyl
import logging
import numpy as np
import multiprocessing as mp
import ctypes
import time
import socket
import os

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

class Module(pyl.Model):
    def createModuleDictionary(self):
        self.moduleData = {}
        # simulation specific
        self.moduleData["/simulation/continuous"] = False
        self.moduleData['/simulation/iteration'] = int(self.simData["/simulation/iteration"].value)
        self.moduleData['/simulation/buffer_current'] = int(self.simData["/simulation/buffer_current"].value)
        #inputs/outputs
        self.moduleData['/moduleName/inputs/someArray'] = self.simData["/anotherModule/outputs/someArray"][1]
        self.moduleData['/moduleName/outputs/someArray'] = np.frombuffer(self.simData["/moduleName/outputs/someArray"][1])
    def updateInputVariables(self):
        # check what buffer frame input to use
        buff_frame = self.moduleData['/simulation/buffer_current']
        if buff_frame == 0:
            buff_frame = 1
        else:
            buff_frame = 0
        self.moduleData['/moduleName/inputs/someArray'] = self.simData["/rxData/outputs/someArray"][buff_frame]
    def setOutputVariables(self):
        # check what buffer frame output to use
        buff_frame = self.moduleData['/simulation/buffer_current']
        self.moduleData['/moduleName/outputs/someArray'] = np.frombuffer(self.simData["/moduleName/outputs/someArray"][buff_frame])


    def someFunction(self, array):
        return array*10

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        longData = simData["/moduleName/inputs/someArray"]
        simData["/moduleName/outputs/someArray"][:] = np.array(self.someFunction(longData), np.int64)


