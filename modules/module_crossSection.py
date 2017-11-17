import pylator as pyl
import multiprocessing as mp
import numpy as np
import time
from  collections import deque

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

import matplotlib as mpl
mpl.use('TkAgg')
#mpl.use('WXAgg')

import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
# import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
# from matplotlib import style

# LARGE_FONT= ("Verdana", 12)
#style.use("ggplot")
#style.use("dark_background")



def module_configuration():
    simData = {
    # Define Module Outputs
    #"/outputs/signal/dtype"   : "double",
    #"/outputs/signal/shape"   : [],
    #"/outputs/signal/default" : 0,

    # Define module inputs with assigned defaults
    "/inputs/signal1" : 0,
    }
    return simData



class Module(pyl.Model):
    def initialise(self, simData):
        data_points = 200
    
        time_step = simData["/simulation/time_step"]

        self.x = np.arange(1001)
        self.y = np.ones(1001)*255
        self.y[0] = 0

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.x, self.y)
        
        self.cid = self.fig.canvas.mpl_connect('key_press_event', self)

        simData["/self/update_plot"] = True
        simData["/self/updateRate"] = 0.001

        self.ax.grid(True)
        plt.ion()
        #self.fig.canvas.draw()
        plt.show(block=False)

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        pipeline = simData["/inputs/signal1"]

        iteration = simData["/simulation/iteration"]
        time_step = simData["/simulation/time_step"]

    

        #simData["/self/line"].set_ylim
        #simData["/self/line"].set_ydata(simData["/self/data_to_plot"])       
        if (iteration*time_step)%simData["/self/updateRate"] < time_step*0.1:
            if simData["/self/update_plot"]:
                
                self.line.set_ydata(pipeline[500,:])
                #self.ax.relim(True)
                #self.ax.autoscale(True)
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()

    def __call__(self, event):
        if event.key == 'v':
            if self.moduleData["/self/update_plot"] == False:
                self.moduleData["/self/update_plot"] = True
            else:
                self.moduleData["/self/update_plot"] = False
        if event.key == 'q':
            self.moduleData["/outputs/keypress"] = ord('q')

if __name__ == "__main__":
    pass