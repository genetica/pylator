"""

    Scheduler class:
    The class are used to instantiate a simulation with
    created modules and execute the scheduler in controlling
    data flow and simultanuous execution of modules.

    Original Created: Gene Stoltz
    Original Date: 30-08-2017

"""

import importlib.util
import sys
import pylator as pyl
import logging
import numpy as np
import multiprocessing as mp
import ctypes
import time
import os

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

class Scheduler(object):
    def set_logging(self, level):
        #level = logging.INFO / logging.DEBUG logging.FATAL
        self.logger = mp.log_to_stderr()
        self.logger.setLevel(level)

    def __init__(self, script_info, simData, connectivity_matrix):
        self.script_info = script_info
        self.inputSimData = simData
        self.connectivity_matrix = connectivity_matrix
        self.scripts = []
        # Load all scripts
        for script_spec in script_info:
            # Depreciated imp module
            #scripts.append(imp.load_source(script_spec[0], script_spec[1]))
            module_name = script_spec[0]
            path = script_spec[1]
            # Depreciated load_module. Should use exec_module
            # but exec_module prevents the import to be pickled.
            loader = importlib.machinery.SourceFileLoader(module_name, path)
            self.scripts.append(loader.load_module(module_name))

    def create_sim_data(self):
        # Create dictionary entries from self.inputSimData variable
        # to initialise and populate real simulation data file self.simData
        crit("ERROR: Not implemented yet")
        pass

    def run(self):
        modules = len(self.script_info)
        barrierWait = modules + 1
        flags = {}
        flags["simulation_active"] = mp.Event()
        flags["simulation_next"] = mp.Barrier(barrierWait)
        flags["simulation_stop"] = mp.Event()
        flags["Module_done"] = mp.Barrier(barrierWait)
        flags["simulation_result"] = mp.Barrier(barrierWait)

        flags["simulation_active"].set()
        flags["simulation_stop"].clear()

        self.simData = {}
        self.simData['scriptNames'] = self.script_info
        self.create_sim_data()   
        
        connectivityMatrix = self.connectivity_matrix
        process = []

        # Create module processes
        for idx, script in enumerate(self.scripts):
            p = script.Module(name=self.script_info[idx][0], args=(flags, self.simData, connectivityMatrix,))
            process.append(p)
        info("All processes created")

        # Start module Processes
        for p in process:
            p.start()
        info("All processes started")
        

        flags["simulation_next"].wait()
        t1 = time.time()
        while True:
        
            flags["Module_done"].wait()
            t2 = time.time()
            info(t2 - t1)

            flags["simulation_result"].wait()
            
            self.simData["/simulation/iteration"].value += 1

            # Switch simulation buffer
            if (self.simData['/simulation/buffer_current'].value == 0):
                self.simData['/simulation/buffer_current'].value = 1
            else:
                self.simData['/simulation/buffer_current'].value = 0

            flags["simulation_next"].wait()
            t1 = time.time()
            if (flags["simulation_stop"].is_set()):
                break

        for p in process:
            p.terminate()