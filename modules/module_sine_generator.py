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
    "/inputs/signal_type"     : "sine",
    "/inputs/frequency"       : 112,
    "/inputs/amplitude"       : 1,
    "/inputs/sampling_period" : 0.01
    }
    return simData

class Module(pyl.Model):
    def initialise(self, simData):
        # Inputs using default values, set as constants (Generated)
        #simData["/inputs/signal_type"] = "sine"
        print(simData["/inputs/signal_type"])
        # User data
        simData["/self/previous_output"] = 0

    def execute(self, simData):
        
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        iteration =  simData["/simulation/iteration"]
        Tt = simData["/simulation/time_step"]
        Ts = simData["/inputs/sampling_period"]
        f = simData["/inputs/frequency"]
        A = simData["/inputs/amplitude"]

        signal_type = simData["/inputs/signal_type"]
        
        if (signal_type == "sine"):
            function = np.sin
        elif (signal_type == "block"):
            function = self.block
        elif (signal_type == "triangle"):
            function = self.triangle
        else:
            function = self.no_function
            
        if int(iteration*Tt / Ts)*Ts >= (iteration-1)*Tt:
            time = iteration*Tt
            period = 1/f
            fraction = (time - int(time/period)*period) / period * 2*np.pi           
            output = A*function( fraction )
        else:
            output = simData["/self/previous_output"]      

        simData["/outputs/signal"] = output
        simData["/self/previous_output"] = output

    # User define functions
    def block(self, value):
        return 1 if value < np.pi else 0

    def triangle(self, value):
        return value/(np.pi) if value < np.pi else (2*np.pi - value)/(np.pi)
    
    def no_function(self, value):
        return value