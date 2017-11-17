import pylator as pyl
import multiprocessing as mp
import numpy as np
import time
from collections import deque


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
    "/inputs/signal" : 0,
    }
    return simData

class Module(pyl.Model):
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