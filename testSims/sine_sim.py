import pylator as pyl
import logging
import multiprocessing as mp
import ctypes
import numpy as np

# Constants


simulate_data = False

debug = mp.get_logger().debug
info = mp.get_logger().info
crit = mp.get_logger().critical

class MyScheduler(pyl.Scheduler):
    # This is temporary and should be generated automatically
    # by the simulator class.
    def create_sim_data(self):
        iteration = 0
        self.simData["/simulation/iteration"] = mp.RawValue(ctypes.c_int, iteration)       
        longestDelay = 0.0
        self.simData["/simulation/longestDelay"] = mp.Value(ctypes.c_float, longestDelay)
        buffer_current = 0
        self.simData["/simulation/buffer_current"] = mp.RawValue(ctypes.c_int, buffer_current)
        time_step = 0.0001
        self.simData["/simulation/time_step"] = mp.RawValue(ctypes.c_double, time_step)




        sampling_period = 0.0002
        self.simData["/user/signal/sampling_period"] = mp.RawValue(ctypes.c_double, sampling_period)
        frequency = 112
        self.simData["/user/signal/frequency"] = mp.RawValue(ctypes.c_double, frequency)
        amplitude = 1.0
        self.simData["/user/signal/amplitude"] = mp.RawValue(ctypes.c_double, amplitude)
        
        noise = 0.1
        self.simData["/user/signal/noise"] = mp.RawValue(ctypes.c_double, noise)

        signal_type = 'block'
        self.simData["/inputs/signal_type"] = mp.RawValue(ctypes.c_wchar_p, signal_type)




        # self.simData["/rxData/outputs/pipeline"] = []  
        # for i in range(2):
        #     base_ptr = mp.RawArray(ctypes.c_uint16, n_bytes//2)
        #     #arr = np.frombuffer(base_ptr)
        #     #arr[:] = np.array(np.ones((height, width))*0, np.int64).flatten()
        #     self.simData["/rxData/outputs/pipeline"].append(base_ptr)


        # self.simData["/convertData/inputs/pipeline"] = None
        # self.simData["/convertData/outputs/pipeline"] = []
        # for i in range(2):
        #     base_ptr = mp.RawArray(ctypes.c_int64, elements)
        #     arr = np.frombuffer(base_ptr)
        #     arr[:] = np.array(np.ones(elements)*0, np.int64)
        #     self.simData["/convertData/outputs/pipeline"].append(base_ptr)

        # self.simData["/showData/inputs/pipeline"] = None 
        # self.simData["/probe/inputs/pipeline"] = None 
        

        # self.simData["/nucData/inputs/nucTableAvaiable"] = None
        # self.simData["/nucData/inputs/nucTable"] = None
        # self.simData["/nucData/inputs/pipeline"] = None
        # self.simData["/nucData/outputs/pipeline"] = []
        # for i in range(2):
        #     base_ptr = mp.RawArray(ctypes.c_int64, elements)
        #     arr = np.frombuffer(base_ptr)
        #     arr[:] = np.array(np.ones(elements)*0, np.int64)
        #     self.simData["/nucData/outputs/pipeline"].append(base_ptr)


        # self.simData["/calibrateData/inputs/pipeline"] = None
        # self.simData["/calibrateData/outputs/nucTableAvailable"] = []
        # for i in range(2):
        #     base_ptr = mp.RawValue(ctypes.c_bool)
        #     self.simData["/calibrateData/outputs/nucTableAvailable"].append(base_ptr)


        # self.simData["/calibrateData/outputs/nucTable"] = []
        # for i in range(2):
        #     base_ptr = mp.RawArray(ctypes.c_double, elements*3)
        #     arr = np.frombuffer(base_ptr)
        #     arr[:] = np.array(np.ones(height*width*3))
        #     self.simData["/calibrateData/outputs/nucTable"].append(base_ptr)



        self.simData["/sine_generator/outputs/signal"] = []
        for i in range(2):
            base_ptr = mp.RawValue(ctypes.c_double)
            self.simData["/sine_generator/outputs/signal"].append(base_ptr)

        self.simData["/noise_generator/outputs/signal"] = []
        for i in range(2):
            base_ptr = mp.RawValue(ctypes.c_double)
            self.simData["/noise_generator/outputs/signal"].append(base_ptr)

        self.simData["/adder/outputs/signal"] = []
        for i in range(2):
            base_ptr = mp.RawValue(ctypes.c_double)
            self.simData["/adder/outputs/signal"].append(base_ptr)

        self.simData["/low_pass/outputs/signal"] = []
        for i in range(2):
            base_ptr = mp.RawValue(ctypes.c_double)
            self.simData["/low_pass/outputs/signal"].append(base_ptr)


        # create shared array
        #base_ptr = mp.RawArray(ctypes.c_int64, N)
        #arr = np.frombuffer(base_ptr)
        #arr[:] = np.array(np.random.uniform(size=N)*1000, np.int64)
        #simData["array_ptr"] = base_ptr
        #simData["array"] = arr

        self.simData["/user/inputs/scope1"] = ["sine_generator"]
        self.simData["/user/inputs/scope2"] = ["adder", "low_pass"]

        
# Simulator Input Variables
script_info = [
                 ["sine_generator",      "../modules/module_sine_generator.py"],
                 ["noise_generator",     "../modules/module_noise_generator.py"],
                 ["adder",               "../modules/module_adder.py"],
                 ["low_pass",            "../modules/module_lowpass_filter.py"],
                 ["scope1",              "../modules/module_scope.py"],
                 ["scope2",              "../modules/module_scope.py"]
                 ]

simData = {}
connectivityMatrix ={   "/adder/inputs/signal1" : "/noise_generator/outputs/signal",
                        "/adder/inputs/signal2" : "/sine_generator/outputs/signal",
                        
                        "/sine_generator/inputs/signal_type"     : "sine",
                        "/sine_generator/inputs/frequency"       : "/user/signal/frequency",
                        "/sine_generator/inputs/amplitude"       : "/user/signal/amplitude",
                        "/sine_generator/inputs/sampling_period" : "/user/signal/sampling_period",

                        "/noise_generator/inputs/sampling_period" : "/user/signal/sampling_period",
                        "/noise_generator/inputs/noise"           : "/user/signal/noise",   
                        
                        "/low_pass/inputs/signal" : "/adder/outputs/signal",

                        "/scope1/inputs/signal" : "/user/inputs/scope1",
                        "/scope2/inputs/signal" : "/user/inputs/scope2"

                    }
# Usage of these inputs are not complete in class yet thus in modules the following functions must be
# implemented manually
# def createModuleDictionary(self)
# def updateSimulationVariables(self):
# def updateInputVariables(self):
# def setOutputVariables(self):
# def updateOutputVariables(self):

# All modules should have the following function:
# def initialise(self, simData):
# def execute(self, simData):
# def finalise(self, simData):


# Create simulator
sim = MyScheduler(script_info, simData, connectivityMatrix)

if __name__ == "__main__":   
    #FATAL/DEBUG/INFO
    # Set logging of simulator
    sim.set_logging(logging.FATAL)
    # Start simulation
    sim.run()
  