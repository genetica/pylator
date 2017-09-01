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

debug = mp.get_logger().debug
info = mp.get_logger().info
crit = mp.get_logger().critical


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

    def keypress(self):
        key = self.simData['/simulation/buffer_current'].value
        buffer_current = self.simData['/simulation/buffer_current'].value

        if self.simData["/control/output/keypress"][int(buffer_current)].value == ord('q'):
            self.flags["simulation_stop"].set()

    def run(self):
        modules = len(self.script_info)
        barrierWait = modules + 1
        self.flags = {}
        self.flags["simulation_active"] = mp.Event()
        self.flags["simulation_next"] = mp.Barrier(barrierWait)
        self.flags["simulation_stop"] = mp.Event()
        self.flags["Module_done"] = mp.Barrier(barrierWait)
        self.flags["simulation_result"] = mp.Barrier(barrierWait)

        self.flags["simulation_active"].set()
        self.flags["simulation_stop"].clear()

        self.simData = {}
        self.simData['scriptNames'] = self.script_info

        keyPressed = 0
        self.simData["/control/output/keypress"] = []
        for i in range(2):
            base_ptr = mp.Value(ctypes.c_uint8, keyPressed)
            self.simData["/control/output/keypress"].append(base_ptr)
        
        
        self.create_sim_data()   
        
        connectivityMatrix = self.connectivity_matrix
        process = []

        info("Creating processes...")
        # Create module processes
        for idx, script in enumerate(self.scripts):
            p = script.Module(name=self.script_info[idx][0], args=(self.flags, self.simData, connectivityMatrix,))
            process.append(p)
        info("Processes created!")

        # Start module Processes
        info("Starting processes...")
        for p in process:
            p.start()
        info("Processes started!")
        

        self.flags["simulation_next"].wait()
        t1 = time.time()
## Simulation Loop
        while True:
            #Wait for all modules to complete
            self.flags["Module_done"].wait()
## Process Simulation Results
            t2 = time.time()  
            info("FRAMERATE {:.3f}s delay,  {:.2f} FPS".format(t2 -t1, 1.0/(t2-t1)))

 
            self.keypress()

            if (self.flags["simulation_stop"].is_set()):
                break

            #Wait for all results to be processed
            self.flags["simulation_result"].wait()
## Prepare Next Simulation Step

            # Increase iteration step
            self.simData["/simulation/iteration"].value += 1

            # Switch simulation buffer
            # Note: The simulation buffer gives the buffer where outputs
            #       will be stored. This in the beginning of a simulation iteration
            #       the inputs uses the previous buffer value.
            if (self.simData['/simulation/buffer_current'].value == 0):
                self.simData['/simulation/buffer_current'].value = 1
            else:
                self.simData['/simulation/buffer_current'].value = 0

            # Clear the keypress placed as input to the simulation iteration that just finished.
            self.simData["/control/output/keypress"][int(self.simData['/simulation/buffer_current'].value)].value = 0

            # The longestDelay are introduced to help interactive modules to re-execute and prevent "lockup" of 
            # rendering processes such as cv2.waitKey. waitkey can now have a shorter wait time allowing 
            # maximum executino of the full simulation but continue rendering the windows.
            # The longest delay are used to estimate re-execution of modules and need to be reset
            # after every iteration to prevent iteration time to monotonically increase.
            self.simData["/simulation/longestDelay"].value = 0.0
  
            # Wait for all modules to syncronise and update simulation variables
            self.flags["simulation_next"].wait()
## Start Simulation Step  
            info("Iteration {}".format(self.simData["/simulation/iteration"].value))
            t1 = time.time()
            if (self.flags["simulation_stop"].is_set()):
                break
            ## While loop END

        # Terminate all processes
        for p in process:
            p.terminate()