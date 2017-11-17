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
import cv2

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

def module_configuration():

    simData = {
    "/outputs/signal/dtype"   : "uint8",
    "/outputs/signal/shape"   : [50, 50],
    "/outputs/signal/default" : 0,

    "/inputs/windows_size" : 50,
    "/inputs/signal"   : 0
    }
    return simData

class Module(pyl.Model):
    """
    This is an example template for creating modules. The name of the module must stay Module.
    """
    def initialise(self, simData):
        self.previous = np.ones(simData["/outputs/signal/shape"], np.uint8)
        simData["/self/updateRate"] = 0.001

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))


        w = simData["/inputs/window_size"]
                    
        self.previous = cv2.GaussianBlur(np.array((self.previous.astype(np.int) + simData["/inputs/signal"].astype(np.int))/2, np.uint8), (w,w), 0)
        
        simData["/outputs/signal"][:, :] = self.previous
        

if __name__ == "__main__":
    """
    Here the test vectors for the function can be placed and unit testing
    can be performed as the module are being developed.
    Either by creating a test bench(1) with pylator or by simply
    calling the execute(2) function.
    (1) -
    """