import pylator as pyl
import numpy as np
import multiprocessing as mp
import time

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

def module_configuration():
    simData = {
    # Define Module Outputs
    "/outputs/signal/dtype"   : "double",
    "/outputs/signal/shape"   : [],
    "/outputs/signal/default" : 0,

    # Define module inputs with assigned defaults
    "/inputs/signal1" : 0,
    "/inputs/signal2" : 0
    }
    return simData

class Module(pyl.Model):
    def initialise(self, simData):
        # Inputs using default values, set as constants (Generated)
        # User data
        simData["/self/previous_output"] = 0

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))
        simData["/outputs/signal"] = simData["/inputs/signal1"] + simData["/inputs/signal2"]
