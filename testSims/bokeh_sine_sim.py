import pylator as pyl
import logging
import multiprocessing as mp
import ctypes
import numpy as np
      
# Simulator Input Variables
script_info = [
                 ["sine_generator",      "../modules/module_sine_generator.py"],
                 ["noise_generator",     "../modules/module_noise_generator.py"],
                 ["adder",               "../modules/module_adder.py"],
                 ["low_pass",            "../modules/module_lowpass_filter.py"],
                 ["fft1",                "../modules/module_fft.py"],
                 #["scope1",              "../modules/module_bokeh.py"],
                 ["scope2",              "../modules/module_bokeh1.py"]
                 ]

simData = {
    "/user/outputs/sampling_period" : 0.0002,
    "/user/outputs/amplitude"       : 1.0,
    "/user/outputs/frequency"       : 112,
    "/user/outputs/signal_type"     : "block",
    "/user/outputs/noise"           : 0.1,

    "/simulation/time_step"         : 0.0001,

    "/user/inputs/scope1"           : ["sine_generator"],
    "/user/inputs/scope2"           : ["adder"],

    "/user/outputs/fft_size"        : [300]

}
connectivityMatrix ={   "/adder/inputs/signal1" : "/noise_generator/outputs/signal",
                        "/adder/inputs/signal2" : "/sine_generator/outputs/signal",
                        
                        "/sine_generator/inputs/signal_type"     : "/scope2/outputs/signal_type",
                        "/sine_generator/inputs/frequency"       : "/user/outputs/frequency",
                        "/sine_generator/inputs/amplitude"       : "/user/outputs/amplitude",
                        "/sine_generator/inputs/sampling_period" : "/user/outputs/sampling_period",

                        "/noise_generator/inputs/sampling_period" : "/user/outputs/sampling_period",
                        "/noise_generator/inputs/noise"           : "/user/outputs/noise",   
                        
                        "/low_pass/inputs/signal" : "/adder/outputs/signal",

                        "/fft1/inputs/signal"       : "/low_pass/outputs/signal",
                        "/fft1/outputs/signal/shape" : "/user/outputs/fft_size",

                        "/scope1/inputs/signal" : "/user/inputs/scope1",
                        "/scope2/inputs/signal" : "/user/inputs/scope2",



                        "/scope1/inputs/monitor"  : "/user/inputs/scope1",
                        "/scope1/inputs/signal1"  : "/sine_generator/outputs/signal",

                        "/scope2/inputs/monitor"  : "/user/inputs/scope2",
                        "/scope2/inputs/signal1"  : "/sine_generator/outputs/signal",
                        "/scope2/inputs/signal2"  : "/noise_generator/outputs/signal",
                        "/scope2/inputs/signal3"  : "/adder/outputs/signal",
                        "/scope2/inputs/signal4"  : "/low_pass/outputs/signal",
                        "/scope2/inputs/array1"   : "/fft1/outputs/signal",

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
sim = pyl.Scheduler(script_info, simData, connectivityMatrix)

if __name__ == "__main__":
    #FATAL/DEBUG/INFO
    # Set logging of simulator
    sim.set_logging(logging.FATAL)
    # Start simulation
    sim.run()
  