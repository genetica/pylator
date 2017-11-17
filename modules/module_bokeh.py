import sys
import pylator as pyl
import logging
import numpy as np
import multiprocessing as mp
import ctypes
import time
import socket
import os
import threading
import subprocess
from  collections import deque

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, layout
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from bokeh.client import push_session
from bokeh.models.widgets import Button
from bokeh.events import ButtonClick



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
       
    def startServer(self):
        print("Starting Server")
        self.session.loop_until_closed() # run forever

    def callback(self, event):
        print("ASDF")
        self.moduleData["/outputs/keypress"] = ord('q')

    def initialise(self, simData):

        #self.server = threading.Thread(target=self.startServer)
        #self.server.start()
        #time.sleep(5)
        self.curdoc = curdoc()
        self.session = push_session(self.curdoc)

        data_points = 200
    
        time_step = simData["/simulation/time_step"]

        self.plot_time = deque()
        for i in range(data_points):
            self.plot_time.append((-data_points+i)*time_step)
        simData["/self/data_to_time"] = self.plot_time

        simData["/self/data_to_time"] = np.arange(data_points)


        for monitor in simData["/inputs/monitor"]:
            #simData["/self/data_to_plot/" + monitor] = deque()
            simData["/self/data_to_plot/" + monitor] = np.ones(data_points)
            #for i in range(data_points):
            #    simData["/self/data_to_plot/" + monitor].append(i)
        
        #for monitor in simData["/inputs/monitor"]:
        #    simData["/self/source"] = ColumnDataSource(data=dict(x=simData["/self/data_to_time"], y=simData["/self/data_to_plot/" + monitor]))
        
        simData["/self/update_plot"] = True
        simData["/self/updateRate"] = 0.001

        # Set up plot
        # self.plot = figure(plot_height=400, plot_width=400, title="my sine wave",
        #             tools="crosshair,pan,reset,save,wheel_zoom",
        #             #x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

        self.plot = []

        for monitor in simData["/inputs/monitor"]:
         self.plot.append(figure(plot_height=400, plot_width=400, title=monitor,
                    tools="crosshair,pan,reset,save,wheel_zoom"))
                    #x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])


        for idx, monitor in enumerate(simData["/inputs/monitor"]):
            simData["/self/line/" + monitor] = self.plot[idx].line(x=simData["/self/data_to_time"], y=simData["/self/data_to_plot/" + monitor], line_width=3, line_alpha=0.6)
            #simData["/self/line/" + monitor] = self.plot.line(x=[0], y=[0], line_width=3, line_alpha=0.6)
            #self.line = self.plot.line(x=simData["/self/data_to_time"], y=simData["/self/data_to_plot/" + monitor], line_width=3, line_alpha=0.6)
            

        self.button = Button()
        self.button.on_event(ButtonClick, self.callback)
        
        self.box = widgetbox(self.button)
        self.PlotLayout = layout(self.plot, self.box)
        self.session.show(self.PlotLayout)
        
        self.t = []

        self.y = {}
        for monitor in simData["/inputs/monitor"]:
            self.y[monitor] = []

  
    def execute(self, simData):
        
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        iteration = simData["/simulation/iteration"]
        time_step = simData["/simulation/time_step"]

        self.t.append(iteration * time_step)
        for idx, monitor in enumerate(simData["/inputs/monitor"]):
            self.y[monitor].append(simData["/inputs/signal" + str(idx+1)])
        
        if (iteration*time_step)%simData["/self/updateRate"] < time_step*0.1:
            if (self.button.clicks != 0):
                print(self.button.clicks)
            if simData["/self/update_plot"]:
                for monitor in simData["/inputs/monitor"]:
                    #self.t = np.arange(len(self.y[monitor]))
                    simData["/self/line/" + monitor].data_source.stream({'x':self.t, 'y': self.y[monitor]}, 200)
                    self.y[monitor] = []
                self.session.force_roundtrip()
                self.t = []


if __name__ == "__main__":
    pass