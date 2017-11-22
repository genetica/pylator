"""

    Model class:
    This class are used to create a Module to be used by the
    pylator scheduler.


    Original Created: Gene Stoltz
    Original Date: 25-07-2017

    Version: 1.0

"""

import multiprocessing as mp
import logging
import time
from threading import BrokenBarrierError

import numpy as np
import ctypes


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

        self.connectivityMatrix = {}
        self.connectivity_matrix_own = {}
        for key in connectivityMatrix:
            if "/" + self.__name__ + "/"  in key:
                self.connectivityMatrix[key] = connectivityMatrix[key]
                self.connectivity_matrix_own["/" + "/".join(key.split("/")[2:])] = \
                                            connectivityMatrix[key]

        self.flags = flags

        self.p_longestDelay = 0.0
        Model.__count += 1

        self.createModuleDictionary()
        info("Initialised {}".format(self.name))

    def initialise(self, simData):
        pass

    def finalise(self, simData):
        info("Quitting")

    def createModuleDictionary(self):
        # Module dictionary
        self.moduleData = {}
        # Update dictionaries
        self.simulation_keys = []
        self.input_keys_val = []
        self.input_keys_arr = []
        self.input_strings = []
        self.output_keys_val = []
        self.output_keys_arr = []
        self.output_strings = []

        # simulation specific
        for key in self.simData:
            # Load simulation data
            if "/simulation/" in key:
                self.simulation_keys.append(key)
                self.moduleData[key] = self.simData[key].value
            # Load all data with respect to the module
            elif "/" + self.__name__ + "/" in key:
                new_key = "/" + "/".join((key.split("/")[2:]))
                self.moduleData[new_key] = self.simData[key]
                if  ("/outputs/" in new_key) and ("/dtype" not in new_key) \
                and ("/shape" not in new_key) and ("/default" not in new_key):
                    if isinstance(self.moduleData[new_key][0], ctypes.Array):
                        if (self.simData[key + "/dtype"] == "str"):
                            self.output_strings.append(new_key)
                        else:    
                            self.output_keys_arr.append(new_key)
                    else:
                        self.output_keys_val.append(new_key)

        for key in self.connectivity_matrix_own:
            val = self.connectivity_matrix_own[key]
            if isinstance(self.simData[val][0], ctypes.Array):
                if (self.simData[val + "/dtype"] == "str"):
                    self.input_strings.append(key)
                else:
                    self.input_keys_arr.append(key)
            else:
                self.input_keys_val.append(key)

        # Inputs
        self.function_char = np.vectorize(chr)
        for key in self.input_strings:
            # Read string typed data
            output_link = self.connectivity_matrix_own[key]
            dtype = np.uint16
            buf = np.frombuffer(self.simData[output_link][0], dtype)
            self.moduleData[key] = "".join(self.function_char(buf))

        for key in self.input_keys_val:           
            # Read scalar values
            output_link = self.connectivity_matrix_own[key]
            self.moduleData[key] = self.simData[output_link][0].value

        for key in self.input_keys_arr:
            # Read Array values
            output_link = self.connectivity_matrix_own[key]
            self.moduleData[key] = np.frombuffer(self.simData[output_link][0], \
                                        dtype=self.simData[output_link + "/dtype"] \
                                        ).reshape(self.simData[output_link + "/shape"])

        # Outputs
        for key in self.output_strings:
            self.moduleData[key] = ""
        
        for key in self.output_keys_val:
            self.moduleData[key] = 0
        
        for key in self.output_keys_arr:           
            self.moduleData[key] = np.frombuffer(self.moduleData[key][0], \
                                        dtype=self.moduleData[key + "/dtype"] \
                                        ).reshape(self.moduleData[key + "/shape"])

    def updateInputVariables(self):
        # check what buffer frame input to use
        buff_frame = self.moduleData["/simulation/buffer_current"]
        if buff_frame == 0:
            buff_frame = 1
        else:
            buff_frame = 0
        for key in self.input_strings:
            # Read string typed data
            output_link = self.connectivity_matrix_own[key]
            dtype = np.uint16
            buf = np.frombuffer(self.simData[output_link][buff_frame], dtype)
            out = self.function_char(buf)
            self.moduleData[key] = ("".join(out)).rstrip(" ")

        for key in self.input_keys_val:
            output_link = self.connectivity_matrix_own[key]
            self.moduleData[key] = self.simData[output_link][buff_frame].value

        for key in self.input_keys_arr:
            output_link = self.connectivity_matrix_own[key]
            self.moduleData[key] = np.frombuffer(self.simData[output_link][buff_frame], \
                                        dtype=self.simData[output_link + "/dtype"] \
                                        ).reshape(self.simData[output_link + "/shape"])

    def setOutputVariables(self):
        # Assign pointer to output shared memory.
        buff_frame = self.moduleData["/simulation/buffer_current"]
        for key in self.output_keys_val:
            self.moduleData[key] = self.simData["/" + self.__name__ + key][buff_frame].value

        for key in self.output_keys_arr:
            self.moduleData[key] = np.frombuffer( \
                                        self.simData["/" + self.__name__ + key][buff_frame], \
                                        dtype=self.moduleData[key + "/dtype"] \
                                        ).reshape(self.moduleData[key + "/shape"])

    def updateOutputVariables(self):
        #Set value for shared variables that is not matrices, maybe not necessary
        buff_frame = self.moduleData["/simulation/buffer_current"]
        for key in self.output_strings:
            # Write string typed data
            dtype = np.uint16
            elements = int(np.prod(self.moduleData[key + "/shape"]))
            update_string = "{:" + str(elements) + "}"
            self.simData["/" + self.__name__ + key][buff_frame][:] = update_string.format(self.moduleData[key])

        for key in self.output_keys_val:
            self.simData["/" + self.__name__ + key][buff_frame].value = self.moduleData[key]

    def updateSimulationVariables(self):
        self.moduleData['/simulation/iteration'] = \
                                        int(self.simData["/simulation/iteration"].value)
        self.moduleData['/simulation/buffer_current'] = \
                                        int(self.simData["/simulation/buffer_current"].value)
        self.moduleData['/simulation/longestDelay'] = self.simData["/simulation/longestDelay"].value

        buff_frame = self.moduleData['/simulation/buffer_current']
        if buff_frame == 0:
            buff_frame = 1
        else:
            buff_frame = 0

        self.moduleData["/inputs/keypress"] = \
                                        self.simData["/control/outputs/keypress"][buff_frame].value
        self.moduleData["/outputs/keypress"] = 0

    def setSimulationVariables(self):
        buff_frame = self.moduleData['/simulation/buffer_current']
        self.simData["/" + self.__name__ + "/outputs/keypress"][buff_frame].value = \
                                        self.moduleData["/outputs/keypress"]

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

            try:
                self.flags["simulation_next"].wait()
            except BrokenBarrierError:
                break

            t1 = time.time()
            self.preExecutionUpdateVariables()

            self.execute(self.moduleData)
            self.postExecutionUpdateVariables()
            t2 = time.time()
            td = t2 - t1
            info("{:.3f}".format(td))

            if td > self.simData["/simulation/longestDelay"].value:
                self.simData["/simulation/longestDelay"].value = td

            try:
                self.flags["Module_done"].wait()
            except BrokenBarrierError:
                break

            self.p_longestDelay = self.simData["/simulation/longestDelay"].value

            try:
                self.flags["simulation_result"].wait()
            except BrokenBarrierError:
                break

        self.finalise(self.moduleData)

    def execute(self, simData):
        raise ValueError(self.name, "No Model has been instantiated.")

if __name__ == '__main__':
    #  NOT valid test currently
    logger = mp.log_to_stderr()
    #logger.setLevel(logging.CRITICAL)
    logger.setLevel(logging.INFO)
