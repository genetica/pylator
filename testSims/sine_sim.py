"""
    1D signal simulation example

    A sine wave generator and noise generator, added together and then 
    fed through a lowpass filter. Scopes are placed on the sine wave
    generated, the signal with added noise and then the low passed signal.abs

    Original Created: Gene Stoltz
    Original Date: 30-08-2017

    Version: 1.0

"""

import pylator as pyl
import multiprocessing as mp
import numpy as np
import logging

# Simulator Input Variables
script_info = [
                 ["sine_generator",      "../modules/module_sine_generator.py"  , "../scenarios/module_sine_generator_1.json"],
                 ["noise_generator",     "../modules/module_noise_generator.py" ],
                 ["adder",               "../modules/module_adder.py"           ],
                 ["low_pass",            "../modules/module_lowpass_filter.py"  ],
                 ["scope1",              "../modules/module_scope.py"           ],
                 ["scope2",              "../modules/module_scope.py"           ]
                 ]

simData = {
    "/user/outputs/sampling_period" : 0.0002,
    "/user/outputs/amplitude"       : 1.0,
    "/user/outputs/frequency"       : 112,
    "/user/outputs/signal_type"     : "block",
    "/user/outputs/noise"           : 0.1,

    "/simulation/time_step"         : 0.0001,

    "/user/inputs/scope1"           : ["sine_generator"],
    "/user/inputs/scope2"           : ["adder", "low_pass"]
}

connectivityMatrix ={   "/adder/inputs/signal1" : "/noise_generator/outputs/signal",
                        "/adder/inputs/signal2" : "/sine_generator/outputs/signal",
                        
                        "/low_pass/inputs/signal" : "/adder/outputs/signal",

                        # Variables defined in connectivity matrix takes priority over scenario files.
                        #"/sine_generator/inputs/signal_type"     : "/user/outputs/signal_type",
                        #"/sine_generator/inputs/frequency"       : "/user/outputs/frequency",
                        #"/sine_generator/inputs/amplitude"       : "/user/outputs/amplitude",
                        #"/sine_generator/inputs/sampling_period" : "/user/outputs/sampling_period",                   

                        "/noise_generator/inputs/sampling_period" : "/user/outputs/sampling_period",
                        "/noise_generator/inputs/noise"           : "/user/outputs/noise",

                        "/scope1/inputs/monitor"  : "/user/inputs/scope1",
                        "/scope1/inputs/signal1"  : "/sine_generator/outputs/signal",
                        "/scope2/inputs/monitor"  : "/user/inputs/scope2",
                        "/scope2/inputs/signal1"  : "/adder/outputs/signal",
                        "/scope2/inputs/signal2"  : "/low_pass/outputs/signal"
                    }

# Create simulator
sim = pyl.Scheduler(script_info, simData, connectivityMatrix)
if __name__ == "__main__":   
    #FATAL/DEBUG/INFO
    # Set logging of simulator
    sim.set_logging(logging.FATAL)
    # Start simulation
    sim.run()
  