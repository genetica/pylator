import pylator as pyl
import multiprocessing as mp
import numpy as np
import time
import cv2

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

def module_configuration():
    simData = {
    # Define Module Outputs
    "/outputs/signal/dtype"   : "uint8",
    "/outputs/signal/shape"   : [50, 50],
    "/outputs/signal/default" : 0,

    # Define module inputs with assigned defaults
    "/inputs/width" : 50,
    "/inputs/height" : 50,

    "/inputs/signal_type"     : "sine",
    "/inputs/frequency"       : 112,
    "/inputs/amplitude"       : 1,
    "/inputs/sampling_period" : 0.01
    }
    return simData

class Module(pyl.Model):
    def initialise(self, simData):
        # Inputs using default values, set as constants (Generated)
        # User data
        simData["/self/previous_output"] = 0
        simData["/inputs/radius"] = 30
        self.image = np.ones((simData["/inputs/height"], simData["/inputs/width"]), np.uint8)*128

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        iteration =  simData["/simulation/iteration"]
        Tt = simData["/simulation/time_step"]
        Ts = simData["/inputs/sampling_period"]
        f = simData["/inputs/frequency"]
        A = 255
        radius = simData["/inputs/radius"]

        height, width = simData["/inputs/height"], simData["/inputs/width"]

        signal_type = simData["/inputs/signal_type"]
        
        if (signal_type == "sine"):
            function = self.sine
        elif (signal_type == "block"):
            function = self.block
        elif (signal_type == "triangle"):
            function = self.triangle
            
        if int(iteration*Tt / Ts)*Ts >= (iteration-1)*Tt:
            time_current = iteration*Tt
            period = 1/f
            fraction = (time_current - int(time_current/period)*period) / period * 2*np.pi           
            output_val = A*function( fraction )

            output = cv2.circle(self.image,(width//2, height//2),radius, int(output_val), -1)

        else:
            output = simData["/self/previous_output"]
        
        simData["/outputs/signal"][:, :] = output
        
        simData["/self/previous_output"] = output

        


    # User define functions
    def sine(self, value):
        return np.sin(value) / 2 + 0.5
    def block(self, value):
        return 1 if value < np.pi else 0

    def triangle(self, value):
        return value/(np.pi) if value < np.pi else (2*np.pi - value)/(np.pi)

if __name__ == "__main__":

    simData = {}
    simData["/simulation/iteration"] = 0
    simData["/simulation/time_step"] = 0.05
    simData["/inputs/sampling_period"] = 0.1
    simData["/inputs/frequency"] = 1
    simData["/inputs/radius"] = 30

    simData["/inputs/height"], simData["/inputs/width"] = 200, 400

    simData["/inputs/signal_type"] = "sine"
    
    flags = []
    connectivityMatrix = []

    class TestModule(Module):
        #Temporary function should be internal
        def createModuleDictionary(self):
            self.moduleData = {}

    t = TestModule(name="Tester", args=(flags, simData, connectivityMatrix,))
    for  i in range(20):
        simData["/simulation/iteration"] += 1
        t.initialise(simData)
        t.execute(simData)