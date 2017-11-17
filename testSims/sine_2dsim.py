"""
    2D signal simulation example.

    Currently only a sine wave generator followed by a probe to visualise the generated
    wave.

    Original Created: Gene Stoltz
    Original Date: 30-08-2017

    Version: 0.1

"""

import pylator as pyl
import multiprocessing as mp
import numpy as np
import logging
import time
      
# Simulator Input Variables
script_info = [
                 ["2dsine_generator",     "../modules/module_2dsine_generator.py"],
                 ["2dgaussian",           "../modules/module_2dgaussian.py"],
                 ["2dscope",              "../modules/module_2dscope.py"],
                 ["crossSection",              "../modules/module_crossSection.py"],
                 ["2dscopeGaus",              "../modules/module_2dscope.py"]
                 ]

simData = {
    "/user/outputs/sampling_period" : 0.01,
    "/user/outputs/amplitude"       : 1.0,
    "/user/outputs/frequency"       : 113,
    "/user/outputs/signal_type"     : "sine",

    "/user/outputs/width"           : 1001,
    "/user/outputs/height"          : 1001,
    "/user/outputs/image_shape"     : [1001, 1001],
    "/user/outputs/image_dtype"     : "uint8",

    "/user/outputs/window_size"     : 501,

    "/simulation/time_step"         : 0.01,

    "/user/outputs/2dscope"          : ["2dsine_generator"],
    "/user/outputs/2dscopeGaus"      : ["2dgaussian"]
}

connectivityMatrix ={                          
                        "/2dsine_generator/inputs/signal_type"     : "/user/outputs/signal_type",
                        "/2dsine_generator/inputs/frequency"       : "/user/outputs/frequency",
                        "/2dsine_generator/inputs/amplitude"       : "/user/outputs/amplitude",
                        "/2dsine_generator/inputs/sampling_period" : "/user/outputs/sampling_period",
                        
                        "/2dsine_generator/outputs/signal/shape"   : "/user/outputs/image_shape",
                        "/2dsine_generator/outputs/signal/dtype"   : "/user/outputs/image_dtype",
                        "/2dsine_generator/inputs/height"          : "/user/outputs/height",
                        "/2dsine_generator/inputs/width"           : "/user/outputs/width",

                        "/2dscope/inputs/monitor" :  "/user/outputs/2dscope",
                        "/2dscope/inputs/signal1"  : "/2dsine_generator/outputs/signal",

                        "/2dscopeGaus/inputs/monitor" :  "/user/outputs/2dscopeGaus",
                        "/2dscopeGaus/inputs/signal1"  : "/2dgaussian/outputs/signal",


                        "/2dgaussian/inputs/window_size" : "/user/outputs/window_size",
                        "/2dgaussian/outputs/signal/shape"   : "/user/outputs/image_shape",
                        "/2dgaussian/inputs/signal" : "/2dsine_generator/outputs/signal",

                        "/crossSection/inputs/signal1" : "/2dgaussian/outputs/signal"

                    }

# Create simulator
sim = pyl.Scheduler(script_info, simData, connectivityMatrix)

if __name__ == "__main__":   
    #FATAL/DEBUG/INFO
    # Set logging of simulator
    sim.set_logging(logging.FATAL)
    # Start simulation
    sim.run()
  