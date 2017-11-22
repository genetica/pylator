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
    "/outputs/signal/shape"   : [200],
    "/outputs/signal/default" : 0,

    # Define module inputs with assigned defaults
    "/inputs/signal" : 0
    }
    return simData

class Module(pyl.Model):
    def initialise(self, simData):
        # Inputs using default values, set as constants (Generated)
        # User data
        self.buffer = deque()
        for i in range(simData["/outputs/signal/shape"][0]*2):
            self.buffer.append(0)

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        self.buffer.append(simData["/inputs/signal"])
        fft = np.fft.rfft(np.array(self.buffer))
        fft = np.abs(fft)
        simData["/outputs/signal"][:] = fft[:simData["/outputs/signal"].size]
        self.buffer.popleft()