import pylator as pyl
import multiprocessing as mp
import numpy as np


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
    "/inputs/noise"           : 1,
    "/inputs/sampling_period" : 0.01
    }
    return simData

class Module(pyl.Model):
    def initialise(self, simData):
        # Inputs using default values, set as constants (Generated)

        # User data
        simData["/self/previous_output"] = 0

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        iteration =  simData["/simulation/iteration"]
        Tt = simData["/simulation/time_step"]
        Ts = simData["/inputs/sampling_period"]

        if int(iteration*Tt / Ts)*Ts >= (iteration-1)*Tt:
            sigma = simData["/inputs/noise"]
            output = np.random.normal(0, sigma)
        else:
            output = simData["/self/previous_output"]

        simData["/outputs/signal"] = output
        simData["/self/previous_output"] = output
