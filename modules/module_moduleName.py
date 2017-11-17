"""

    Empty Module Template:
    This python file are used to demostrate an empty module template
    to be used with pylator.


    Original Created: Gene Stoltz
    Original Date: 16-10-2017

    Version: 1.0

"""

import pylator as pyl
import logging
import time
import numpy as np
import multiprocessing as mp

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

def module_configuration():
    """
    Defines the inputs and outputs. 
    This is required for all modules
    as it defines the interfaces for the module.

    These variables can be overwritten with either a configuration file
    or by adding the addition to the Connectivity Matrix linking a
    global variable to the input of the module.

    """
    simData = {
    # Define Module Outputs with their default values, must use "/outputs/"
    #  and the data type, shape and default values must be defined
    #  Use [] for scalar otherwise as required.
    "/outputs/signal1/dtype"   : "uint8",
    "/outputs/signal1/shape"   : [50, 50],
    "/outputs/signal1/default" : 0,

    "/outputs/signal2/dtype"   : "float",
    "/outputs/signal2/shape"   : [],
    "/outputs/signal2/default" : 10,

    # Define module inputs with assigned defaults, must use "/inputs/"
    # Currently matrix defaults is not supported. - TODO
    "/inputs/setting1" : 50,
    "/inputs/setting2" : 50,
    "/inputs/signal"   : 0
    }
    return simData

class Module(pyl.Model):
    """
    This is an example template for creating modules. The name of the module must stay Module.
    """
    def initialise(self, simData):
        """
        This initialises variables in the module, such as specific counters
        GUI elements etc. Variables can be created by using the 
        self.some_variable or 
        simData["/self/some_variable"]
        Any method can be used.
        """
        self.my_counter = 0

    def execute(self, simData):
        """
        This funtion is executed every iteration and should be non-blocking preferable,
        execpt if it influence the data flow.
        Outputs should be assigned to simData such as when it is a scalar value
            simData["/outputs/signal2"] = some_value
        or when the output is a matrix
            simData["/outputs/signal1"][:,:] = some_matrix_of_the_same_shape

        Inputs can easily be accessed through
            simData["inputs]
        """
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        self.my_counter += 1

        longData = simData["/inputs/signal"]
        shape = simData["/outputs/signal1/shape"]
        dtype = simData["/outputs/signal1/dtype"]

        if self.my_counter % 2:
            longData *= longData

        simData["/outputs/signal1"][:, :] = np.array(self.someFunction(longData), dtype=dtype).reshape(shape)

    def finalise(self, simData):
        """
        This function get executed when the simulation finishes.
        This is where data can be dumped, ports released, files closed etc.
        """
        info("Quitting!")

    # User defined functions, require "self" as first input.
    def someFunction(self, array):
        return array*10

if __name__ == "__main__":
    """
    Here the test vectors for the function can be placed and unit testing
    can be performed as the module are being developed.
    Either by creating a test bench(1) with pylator or by simply
    calling the execute(2) function.
    (1) -
    """