import sys
import pylator as pyl
import logging
import numpy as np
import multiprocessing as mp
import ctypes
import time
import socket
import os
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







class Module(pyl.Model):
    #Temporary function should be internal
    def createModuleDictionary(self):
        self.moduleData = {}
        # simulation specific
        self.moduleData["/simulation/continuous"] = False
        self.moduleData["/simulation/iteration"] = self.simData["/simulation/iteration"].value
        self.moduleData["/simulation/time_step"] = self.simData["/simulation/time_step"].value
        self.moduleData["/simulation/buffer_current"] = self.simData["/simulation/buffer_current"].value

        self.moduleData["/control/input/keypress"] = 0
        
        self.moduleData["/self/monitor"] = self.simData["/user/inputs/" + self.__name__]        

        #inputs/outputs
        for monitor in self.moduleData["/self/monitor"]:
            self.moduleData["/inputs/" + monitor] = self.simData["/" + monitor + "/outputs/signal"][1].value

    def updateInputVariables(self):
        # check what buffer frame input to use
        buff_frame = self.moduleData["/simulation/buffer_current"]
        if buff_frame == 0:
            buff_frame = 1
        else:
            buff_frame = 0
        self.moduleData["/inputs/keypress"] = self.simData["/control/outputs/keypress"][buff_frame].value
        for monitor in self.moduleData["/self/monitor"]:
            self.moduleData["/inputs/" + monitor] = self.simData["/" + monitor + "/outputs/signal"][buff_frame].value
    def assignOutputVariables(self):
        # Assign pointer to output shared memory.
        buff_frame = self.moduleData["/simulation/buffer_current"]
        pass
    def updateOutputVariables(self):
        #Set value for shared variables that is not matrices, maybe not necessary
        buff_frame = self.moduleData["/simulation/buffer_current"]       
        pass
        




    def initialise(self, simData):
        data_points = 200
    
        time_step = simData["/simulation/time_step"]

        self.plot_time = deque()
        for i in range(data_points):
            self.plot_time.append((-data_points+i)*time_step)
        simData["/self/data_to_time"] = self.plot_time

        for monitor in simData["/self/monitor"]:
            simData["/self/data_to_plot/" + monitor] = deque()
            for i in range(data_points):
                simData["/self/data_to_plot/" + monitor].append(0)



        self.fig, self.ax = plt.subplots()
        for monitor in simData["/self/monitor"]:
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

        #plt.ion()


        iteration = simData["/simulation/iteration"]
        time_step = simData["/simulation/time_step"]


        for monitor in simData["/self/monitor"]:
            simData["/self/data_to_plot/"+monitor].append(simData["/inputs/" + monitor])
            simData["/self/data_to_plot/"+monitor].popleft()

        simData["/self/data_to_time"].append(iteration * time_step)
        simData["/self/data_to_time"].popleft()        

        #simData["/self/line"].set_ylim


        #simData["/self/line"].set_ydata(simData["/self/data_to_plot"])
        

        if (iteration*time_step)%simData["/self/updateRate"] < time_step*0.1:
            if simData["/self/update_plot"]:
                time_axes = (np.array(simData["/self/data_to_time"]) +iteration )* time_step *1e6
                for monitor in simData["/self/monitor"]:

                    simData["/self/line/" + monitor].set_data(time_axes, simData["/self/data_to_plot/" + monitor])
                self.ax.relim(True)
                self.ax.autoscale(True)


                    #print(self.ax.get_xlim())
                #simData["/self/line"].set
                #simData["/self/line"], = self.ax.plot(simData["/self/data_to_plot"])
                #self.ax.draw_artist(self.ax.patch)
                #self.ax.draw_artist(simData["/self/line"])
                #self.ax.draw_artist(ax.yaxis)
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
            #simData["/self/fig"].set_ydata(simData["/self/data_to_plot"])  # update the data
            #plt.draw()                         # redraw the canvas

            #d = np.random.rand(1000)
            #self.line.set_ydata = simData["/self/data_to_plot"]
            #self.ax.draw()
            #self.ax.plot(simData["/self/data_to_plot"], 'r')

            #self.fig.canvas.draw()

            #fig = plt.figure(1)
        



        # plt.plot(d)
        #plt.show(block=False)
        # print(d)
        # print(fig)

        #time.sleep(0.5)

    def __call__(self, event):
        #print('click', event)
        if event.key == 'v':
            if self.moduleData["/self/update_plot"] == False:
                self.moduleData["/self/update_plot"] = True
            else:
                self.moduleData["/self/update_plot"] = False
        
        if event.key == 'q':
            self.flags["simulation_stop"].set()

        self.moduleData["/control/outputs/keypress"] = ord(event.key)

            #self.ax.relim(True)
            #self.ax.autoscale(True)
            #visible = xl.get_visible()
            #xl.set_visible(not visible)
            #fig.canvas.draw()
        # if event.inaxes!=self.line.axes: return
        # self.xs.append(event.xdata)
        # self.ys.append(event.ydata)
        # self.line.set_data(self.xs, self.ys)
        # self.line.figure.canvas.draw()




if __name__ == "__main__":
    pass