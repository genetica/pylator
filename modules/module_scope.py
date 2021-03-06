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
    "/inputs/monitor" : [],
    "/inputs/signal1" : 0,
    "/inputs/signal2" : 0,
    }
    return simData



class Module(pyl.Model):
    def initialise(self, simData):
        data_points = 200
    
        time_step = simData["/simulation/time_step"]

        self.plot_time = deque()
        for i in range(data_points):
            self.plot_time.append((-data_points+i)*time_step)
        simData["/self/data_to_time"] = self.plot_time

        for monitor in simData["/inputs/monitor"]:
            simData["/self/data_to_plot/" + monitor] = deque()
            for i in range(data_points):
                simData["/self/data_to_plot/" + monitor].append(0)

        self.fig, self.ax = plt.subplots()
        for monitor in simData["/inputs/monitor"]:
            simData["/self/line/" + monitor], = self.ax.plot(simData["/self/data_to_time"], simData["/self/data_to_plot/" + monitor])
        
        self.cid = self.fig.canvas.mpl_connect('key_press_event', self)

        simData["/self/update_plot"] = True
        simData["/self/updateRate"] = 0.001

        self.ax.grid(True)
        plt.ion()
        #self.fig.canvas.draw()
        plt.show(block=False)

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        iteration = simData["/simulation/iteration"]
        time_step = simData["/simulation/time_step"]

        for idx, monitor in enumerate(simData["/inputs/monitor"]):
            simData["/self/data_to_plot/"+monitor].append(simData["/inputs/signal" + str(idx+1)])
            simData["/self/data_to_plot/"+monitor].popleft()

        simData["/self/data_to_time"].append(iteration * time_step)
        simData["/self/data_to_time"].popleft()        

        #simData["/self/line"].set_ylim
        #simData["/self/line"].set_ydata(simData["/self/data_to_plot"])       
        if (iteration*time_step)%simData["/self/updateRate"] < time_step*0.1:
            if simData["/self/update_plot"]:
                time_axes = (np.array(simData["/self/data_to_time"]) +iteration )* time_step *1e6
                for monitor in simData["/inputs/monitor"]:
                    simData["/self/line/" + monitor].set_data(time_axes, simData["/self/data_to_plot/" + monitor])
                self.ax.relim(True)
                self.ax.autoscale(True)
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