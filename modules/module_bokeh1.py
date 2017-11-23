"""

    Demonstrates the usage of bokeh for display purposes.

    This can also serve as a base template for creating bokeh 
    interfaces.

    Note:
        Only a single module can be instantiated otherwise server IPs should
        be changed.

"""
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

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

# To quit browser tab
import win32com.client
import traceback

# Bokeh imports
from bokeh.layouts import row, widgetbox, layout, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Button, Panel, Tabs, Toggle, RadioButtonGroup
from bokeh.plotting import Figure

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.server.server import Server

def module_configuration():
    simData = {
        # Define Module Outputs
        "/outputs/signal_type/dtype"   : "str",
        "/outputs/signal_type/shape"   : [10],
        "/outputs/signal_type/default" : "sine",

        # Define module inputs with assigned defaults
        "/inputs/monitor" : [],
        "/inputs/signal1" : 0,
        "/inputs/signal2" : 0,
        "/inputs/signal3" : 0,
        "/inputs/signal4" : 0,
        "/inputs/array1"  : 0
    }
    return simData

class Module(pyl.Model):
    def initialise(self, simData):

        simData["/self/update_plot"] = True
        simData["/self/updateRate"] = 0.001

        # Create bokeh application with initalisation function modify doc.
        self.bokeh_app = Application(FunctionHandler(self.bokeh_document))
        crit('INFO: Opening Bokeh application on http://localhost:5006/')
        # Create server, replaces "bokeh serve" call in command line
        self.server = Server({'/': self.bokeh_app})
        # Start secondary thread that will maintain the io_loop for bokeh,
        # and maintain the connection to the server for callbacks.
        self.worker_init = threading.Event()
        self.worker = threading.Thread(target=self.bkworker)
        self.worker.start()
        # Wait for bokeh document to be created
        self.worker_init.wait()

    def bkworker(self):
        # Main secondary thread.
        # Run this as a thread to continuously update the io_loop
        # to be non-blocking.
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()

    def stop_bkworker(self):
        # Stop the io_loop for the bokeh server
        self.server.io_loop.stop()
        # wait for the thread managing the io_loop to the bokeh server to close
        self.worker.join()

    def bokeh_document(self, doc):
        # Document to be loaded by Bokeh Server
        try:
            self.modify_doc(doc)
        except Exception as e:
            # Display any exceptions and problems with created Document.
            for err in traceback.format_tb(e.__traceback__):
                for line in err.split("\n"):
                    crit(line)
            crit(e)
            # Stop io_loop
            self.server.io_loop.stop()
            # Allow simulator to exit gracefully.
            self.worker_init.set()

    def update_simdata(self):
        # Callback for updating iteration umber in Simulation Panel
        self.widget_sim["TextInput_iteration"].value = str( \
                                    self.moduleData["/simulation/iteration"])
        self.widget_sim["TextInput_ips"].value = str( \
                                    self.moduleData["/simulation/iterations_per_second"])

    def on_click_quit(self):
        # Callback for Quit Button simulation
        self.set_quit = True

    def slider_callback(self, attr, old, new):
        # This function is used for callback from bokeh server
        # such as buttons etc.
        self.samples = new

    def on_click_pause(self, status):
        # Callback to pause the graph updates
        self.hold = status

    def on_click_radio_button(self, active):
        if active == 0:
            self.signal_type = "sine"
        elif active == 1:
            self.signal_type = "block"
        elif active == 2:
            self.signal_type = "triangle"

    def modify_doc(self, doc):
        """
            This is the function used for plot layout and data initialisation
        """
        # Create doc
        self.doc = doc
        # Add periodic callback to update simulation data
        self.period_callback_sim = self.doc.add_periodic_callback(self.update_simdata, 100)
        # Add periodic callback for refreshing displays
        self.period_callback = self.doc.add_periodic_callback(self.update_data, 100)
        # Set threading locks to prevent bokeh server retention
        self.updated_plot = threading.Event()
        self.updated_data = threading.Event()
        self.updated_plot.set()

        # Create simulation Panel
        self.widget_sim = {}
        self.set_quit = False
        self.widget_sim["Button_quit"] = Button(label="Quit", button_type="danger")
        self.widget_sim["Button_quit"].on_click(self.on_click_quit)

        self.widget_sim["TextInput_iteration"] = TextInput(value="0", title="Iteration")
        self.widget_sim["TextInput_ips"] = TextInput(value="0", title="IPS")

        sim_tab = layout(widgetbox(list(self.widget_sim.values())))

# Create User Panels
        time_step = self.simData["/simulation/time_step"]

    # Create number of required figures
        fig_tools = "hover,crosshair,pan,reset,save,wheel_zoom,box_zoom"
        fig = []
        for i in range(4):
            fig.append(Figure(tools=fig_tools))

        self.samples_to_stream = 400

    # Create dummy data to initilise plotted lines as required
        self.data = []
        for i in range(5):
            self.data.append(ColumnDataSource({'x': np.arange(200)*-1*time_step, \
                                               'y': np.zeros(200)}))
    # Create plottedlines
        self.lines = []
        self.lines.append(fig[0].line('x', 'y', source=self.data[0], color='navy'))
        self.lines.append(fig[1].line('x', 'y', source=self.data[1], color='purple'))
        self.lines.append(fig[2].line('x', 'y', source=self.data[2], color='blue'))
        self.lines.append(fig[2].line('x', 'y', source=self.data[3], color='red'))

        self.array = []
        self.array_x = []
        self.array.append(fig[3].line('x', 'y', source=self.data[4], color='red'))
        self.array_x.append(np.arange(self.moduleData["/inputs/array1"].size))
    # Create variables for stored lines that will be plotted
        self.t = []
        self.tb = []
        self.y = []
        self.yb = []
        for l in self.lines:
            self.y.append([])
            self.yb.append([])

        plot_layouts = {}
        plot_titles = ["Generator", "Outputs"]
# Panel - Sine Generator
        self.hold = False
        self.widget_1 = {}
        self.widget_1["Button_pause"] = Toggle(label="Pause", button_type="primary")
        self.widget_1["Button_pause"].on_click(self.on_click_pause)

        self.signal_type = "sine"
        self.widget_1["radio_button"] = RadioButtonGroup(labels=["Sine", "Block", "Triangle"], \
                                                         active=0)
        self.widget_1["radio_button"].on_click(self.on_click_radio_button)
        self.widget_1["widgetbox"] = widgetbox(self.widget_1["radio_button"], \
                                               self.widget_1["Button_pause"])

        plot_layouts["Generator"] = layout([row([fig[0], fig[1]]), self.widget_1["widgetbox"]])

# Panel - Output
        self.widget_2 = {}
        self.widget_2["Button_pause"] = Toggle(label="Pause", button_type="primary")
        self.widget_2["Button_pause"].on_click(self.on_click_pause)
        #self.widget_2["widgetbox"] = Slider(self.widget_1["Button_pause"])
        self.widget_2["widgetbox"] = widgetbox(self.widget_2["Button_pause"])
        plot_layouts["Outputs"] = layout(row([fig[2], fig[3]]), self.widget_2["widgetbox"])


    # Add Panels to the final layout
        tab = []
        # Add simulation Panel
        tab.append(Panel(child=sim_tab, title="Simulation"))
        # Add user Panels
        tab.append(Panel(child=plot_layouts["Generator"], title="Generator"))
        tab.append(Panel(child=plot_layouts["Outputs"], title="Outputs"))

        # Assign final layout
        tabs = Tabs(tabs=tab)
        # Create base document for application
        self.doc.add_root(tabs)
        # Release initialisation , indicate document creation are complete
        self.worker_init.set()

    def update_data(self):
        # Function to update data to the plotted lines.
        # If there is no new data skip this update
        if self.updated_data.is_set():
            # Check that data is not set twice
            if not self.updated_plot.is_set():
                for idx, l in enumerate(self.lines):
                    l.data_source.stream({'x': self.tb, 'y' : self.yb[idx]}, self.samples_to_stream)
                for l in self.yb:
                    l = []
                self.tb = []
                self.array[0].data_source.data = {'x': self.array_x[0], 'y': self.arr}
            # Indicate that plots have been updated with new data
            self.updated_plot.set()

    def additional_keypresses(self, simData):
        # Handles keypresses received throughout the system
        key = simData["/inputs/keypress"]
        if key == ord('p'):
            self.hold ^= True

    def execute(self, simData):
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        iteration = simData["/simulation/iteration"]
        time_step = simData["/simulation/time_step"]

        # Create time line
        self.t.append(iteration * time_step)

        # Read inputs for streaming data
        self.y[0].append(simData["/inputs/signal1"])
        self.y[1].append(simData["/inputs/signal2"])
        self.y[2].append(simData["/inputs/signal3"])
        self.y[3].append(simData["/inputs/signal4"])

        self.arr = simData["/inputs/array1"]

        #if (iteration*time_step)%simData["/self/updateRate"] < time_step:
        if self.hold == False:
            # See if bokeh finished updating data
            if self.updated_plot.is_set():
                # Clear flag for plot
                self.updated_plot.clear()
                # Copy time data
                self.tb = self.t[:]
                # Copy all required line data to be updated into temp
                # variable.
                for idx, y in enumerate(self.y):
                    # Check that data sizes is equal
                    if len(y) > len(self.tb):
                        diff = len(y) - len(self.tb)
                        self.yb[idx] = y[diff:]
                    else:
                        self.yb[idx] = y[:]
                    if len(y) < len(self.tb):
                        diff = len(self.tb) - len(y)
                        self.tb = self.t[diff:]

                # Reset input data, to prevent double updated data
                self.t = []
                for y in self.y:
                    y = []
                # Allow update function to update new data
                self.updated_data.set()

        # Update Outputs
        simData["/outputs/signal_type"] = self.signal_type

        # Manage any required keypresses that propagates throught the system
        self.additional_keypresses(simData)
        # Check if bokeh server is running otherwise quit.
        if not self.worker.is_alive():
            crit("Bokeh Server is not running!")
            self.set_quit = True
        # This is required for simulation interface
        if self.set_quit:
            # Close simulation
            simData["/outputs/keypress"] = ord('q')
            # Send keypress to browser to close
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys("^w")

    def finalise(self, simData):
        self.stop_bkworker()

if __name__ == "__main__":
    pass
