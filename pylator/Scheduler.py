"""

    Scheduler class:
    The class are used to instantiate a simulation with
    created modules and execute the scheduler in controlling
    data flow and simultanuous execution of modules.

    Original Created: Gene Stoltz
    Original Date: 30-08-2017

    Version: 1.0

"""

import pylator as pyl
import multiprocessing as mp
import numpy as np
import logging
import importlib.util
import ctypes
import time
import json
import os
if os.name == 'nt':
    import msvcrt

debug = mp.get_logger().debug
info = mp.get_logger().info
crit = mp.get_logger().critical

class Scheduler(object):
    def set_logging(self, level):
        #level = logging.INFO / logging.DEBUG logging.FATAL

        self.logger = mp.log_to_stderr()
        self.logger.setLevel(level)

    def __init__(self, script_info, simData, connectivity_matrix):
        self.script_info = script_info
        self.simData = simData
        self.connectivity_matrix = connectivity_matrix
        self.scripts = []
        # Load all scripts
        for script_spec in script_info:
            # Depreciated imp module
            #scripts.append(imp.load_source(script_spec[0], script_spec[1]))
            module_name = script_spec[0]
            path = script_spec[1]
            # Depreciated load_module. Should use exec_module
            # but exec_module prevents the import to be pickled.
            loader = importlib.machinery.SourceFileLoader(module_name, path)
            self.scripts.append(loader.load_module(module_name))

    def create_sim_data(self):
        # Keypress data
        keyPressed = 0
        self.simData["/control/outputs/keypress/shape"] = []
        self.simData["/control/outputs/keypress/dtype"] = np.int
        self.simData["/control/outputs/keypress"] = []
        for i in range(2):
            base_ptr = mp.Value(ctypes.c_uint8, keyPressed)
            self.simData["/control/outputs/keypress"].append(base_ptr)

        for name in self.script_info:
            self.simData["/" + name[0] + "/inputs/keypress"] = 0
            self.connectivity_matrix["/" + name[0] + "/inputs/keypress"] = \
                                     "/control/outputs/keypress"
            self.simData["/" + name[0] + "/outputs/keypress"] = []
            for i in range(2):
                base_ptr = mp.RawValue(ctypes.c_uint8, 0)
                self.simData["/" + name[0] + "/outputs/keypress"].append(base_ptr)

        # Create simulation data
        iteration = 0
        self.simData["/simulation/iteration"] = mp.RawValue(ctypes.c_int, iteration)
        longestDelay = 0.0
        self.simData["/simulation/longestDelay"] = mp.Value(ctypes.c_float, longestDelay)
        buffer_current = 0
        self.simData["/simulation/buffer_current"] = mp.RawValue(ctypes.c_int, buffer_current)
        iterations_per_second = 0.0
        self.simData["/simulation/iterations_per_second"] = mp.Value(ctypes.c_float, iterations_per_second)


        if "/simulation/time_step" in self.simData:
            self.simData["/simulation/time_step"] = \
                    mp.RawValue(ctypes.c_double, self.simData["/simulation/time_step"])
        else:
            time_step = 1.0
            self.simData["/simulation/time_step"] = mp.RawValue(ctypes.c_double, time_step)

        self.simData["/adder/outputs/signal"] = []
        for i in range(2):
            base_ptr = mp.RawValue(ctypes.c_double)
            self.simData["/adder/outputs/signal"].append(base_ptr)

        self.simData["/low_pass/outputs/signal"] = []
        for i in range(2):
            base_ptr = mp.RawValue(ctypes.c_double)
            self.simData["/low_pass/outputs/signal"].append(base_ptr)

        # Create simulation data for every module
        for idx, script in enumerate(self.scripts):
            name = self.script_info[idx][0]
            if "module_configuration" in script.__dict__:
                config = script.module_configuration()
                if len(self.script_info[idx]) == 3:
                    #Load scenario file if specified.
                    scenario_file_name = self.script_info[idx][2]
                    try:
                        with open(scenario_file_name, "r") as fp:
                            scenario = json.load(fp)
                        for key in scenario:
                            config[key] = scenario[key]
                    except IOError:
                        crit("{} defaults loaded. Unable to load scenario "
                             "file, {}".format(name, scenario_file_name))
                    except KeyError as e:
                        crit("Invalid entry {} in scenario "
                             "file {}".format(e, scenario_file_name))
                        exit()
                    info("{} loaded with {}.".format(name, scenario_file_name))
                else:
                    info("{} defaults loaded.".format(name))

                # update all variables from user defined inputs
                for key in config:
                    while (isinstance(config[key], str)) and \
                          (len(config[key][0]) > 0)      and \
                          (config[key][0] == "/"):
                        try:
                            config[key] = self.simData[config[key]]
                        except KeyError as e:
                            crit("{}, variable {} does not "
                                 "exist.".format(name, e))
                            exit()

                # Add all entries into simulation dictionary
                for key in config:
                    self.simData["/" + name + key] = config[key]

                # Remove all user defined constants from connectivity matrix and update
                # modules simData with new value from user defined constants
                to_be_remove = []
                for key in self.connectivity_matrix:
                    if (("/" + name +"/") in key) and ("/user/" in self.connectivity_matrix[key]):
                        to_be_remove.append(key)

                for user in to_be_remove:
                    key = self.connectivity_matrix[user]
                    try:
                        self.simData[user] = self.simData[key]
                        config["/" + "/".join(user.split("/")[2:])] = self.simData[key]
                        key = user
                    except KeyError as e:
                        crit("{}, variable {} does not "
                             "exist.".format("Connectivity Matrix", e))
                        exit()
                    while (isinstance(self.simData[key], str)) and \
                            (len(self.simData[key][0]) > 0)    and \
                            (self.simData[key][0] == "/"):
                        try:
                            self.simData[key] = self.simData[self.simData[key]]
                            config["/" + "/".join(key.split("/")[2:])] = self.simData[key]
                        except KeyError as e:
                            crit("{}, variable {} does not "
                                 "exist.".format(name, e))
                            exit()
                    del self.connectivity_matrix[key]

                # Assign memory to all outputs
                # Currently not support matrix assigments as defaults for inputs. - TODO
                outputs_added = []
                for key in config:
                    if "outputs" in key:
                        output = key.split('/')[2] # ["", "outputs", "output"]
                        if output not in outputs_added:
                            outputs_added.append(output)
                            test = "/outputs/" + output
                            try:
                                data_type = config[test + "/dtype"]
                                shape = config[test + "/shape"]
                                default = config[test + "/default"]
                            except KeyError as e:
                                crit("{:15}, Incomplete output, '{}' "
                                     "does not exist.".format(name, e))
                                exit()
                            # Convert data types
                            try:
                                dtype, ctype = self.select_data_type(data_type)
                            except ValueError:
                                crit("{} invalid data type '{}'".format(name + test, data_type))
                                exit()

                            # Check shape data
                            if not isinstance(shape, list):
                                crit("{} invalid shape '{}'".format(name + test, data_type))
                                exit()
                            else:
                                for d in shape:
                                    if not isinstance(d, int):
                                        crit("{} invalid dimension '{}'".format(name + test, d))
                                        exit()

                            # Check default value is acceptable, TODO

                            # Create memory allocation and buffers
                            self.simData["/" + name + test + "/shape"] = tuple(shape)
                            self.simData["/" + name + test + "/dtype"] = dtype
                            self.simData["/" + name + test] = []
                            elements = int(np.prod(shape))
                            if elements > 1:
                                if data_type == "str":
                                    if not isinstance(defaults, str):
                                        defaults = ""
                                    empty = np.zeros(elements, dtype)
                                    empty[:len(defaults)] = defaults[:]
                                    defaults = empty

                                elif isinstance(default, str):
                                    try:
                                        defaults = np.loadtxt(defaults, dtype=dtype)
                                    except:
                                        crit("{} default loading, problem "
                                             "with {}.".format(name, default))
                                else:
                                    defaults = np.ones(elements, dtype=dtype)*default
                                for i in range(2):
                                    base_ptr = mp.RawArray(ctype, elements)
                                    arr = np.frombuffer(base_ptr, dtype)
                                    arr[:] = defaults
                                    self.simData["/" + name + test].append(base_ptr)
                                
                                if data_type == "str":
                                    self.simData["/" + name + test + "/dtype"] = "str"
                            else:
                                defaults = default
                                for i in range(2):
                                    base_ptr = mp.RawValue(ctype, defaults)
                                    self.simData["/" + name + test].append(base_ptr)
            else:
                crit("{:20} has no configuration data.".format(name))

    def select_data_type(self, data_type):
        data_type_dict = {
            "int"       : (np.int, ctypes.c_int),
            "float"     : (np.float32, ctypes.c_float),
            "double"    : (np.float64, ctypes.c_longdouble),
            "uint8"     : (np.uint8, ctypes.c_uint8),
            "uint16"    : (np.uint16, ctypes.c_uint16),
            "str"       : (np.uint16, ctypes.c_wchar),
            "bool"      : ("bool", ctypes.c_bool)
        }

        if data_type in data_type_dict:
            dtype, ctype = data_type_dict[data_type]
        else:
            raise ValueError

        return dtype, ctype

    def check_terminal_input(self):
        if os.name == 'nt':
            if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    key = ord(key)
                    if (key != 0) and (key != 255):
                        buffer_current = self.simData['/simulation/buffer_current'].value
                        self.simData["/control/outputs/keypress"][buffer_current].value = key
                except:
                    crit("WARNING: {} received not readable".format(key))
        else:
            crit("WANRING: Current terminal input is only supported in Windows.")

    def keypress(self):
        buffer_current = self.simData['/simulation/buffer_current'].value

        for idx, script in enumerate(self.scripts):
            key = self.simData["/" + self.script_info[idx][0] + \
                               "/outputs/keypress"][buffer_current].value
            if (key != 0) and (key != 255):
                self.simData["/control/outputs/keypress"][buffer_current].value = key

        self.check_terminal_input()
        key = self.simData["/control/outputs/keypress"][buffer_current].value
        if key == ord('q'):
            self.flags["simulation_stop"].set()

    def run(self):
        modules = len(self.script_info)
        barrierWait = modules + 1
        self.flags = {}
        self.flags["simulation_active"] = mp.Event()
        self.flags["simulation_next"] = mp.Barrier(barrierWait)
        self.flags["simulation_stop"] = mp.Event()
        self.flags["Module_done"] = mp.Barrier(barrierWait)
        self.flags["simulation_result"] = mp.Barrier(barrierWait)

        self.flags["simulation_active"].set()
        self.flags["simulation_stop"].clear()

        self.simData["scriptNames"] = self.script_info

        self.create_sim_data()

        connectivityMatrix = self.connectivity_matrix
        process = []

        info("Creating processes...")
        # Create module processes
        for idx, script in enumerate(self.scripts):
            p = script.Module(name=self.script_info[idx][0], \
                              args=(self.flags, self.simData, connectivityMatrix,))
            process.append(p)
        info("Processes created!")

        # Start module Processes
        info("Starting processes...")
        for p in process:
            p.start()
        info("Processes started!")

        self.flags["simulation_next"].wait()
        t1 = time.time()
## Simulation Loop
        while True:
            #Wait for all modules to complete
            self.flags["Module_done"].wait()

## Process Simulation Results
            t2 = time.time()
            if t2 - t1 > 0:
                ips = 1.0/(t2-t1)
                self.simData["/simulation/iterations_per_second"].value = 1.0/(t2-t1)
                debug("ITERATION RATE {:.3f}s delay,  {:.2f} IPS".format(t2 -t1, ips))
                
            self.keypress()

            if self.flags["simulation_stop"].is_set():
                self.flags["simulation_active"].clear()

            #Wait for all results to be processed
            self.flags["simulation_result"].wait()
            if not self.flags["simulation_active"].is_set():
                break
## Prepare Next Simulation Step

            # Increase iteration step
            self.simData["/simulation/iteration"].value += 1

            # Switch simulation buffer
            # Note: The simulation buffer gives the buffer where outputs
            #       will be stored. This in the beginning of a simulation iteration
            #       the inputs uses the previous buffer value.
            if self.simData['/simulation/buffer_current'].value == 0:
                self.simData['/simulation/buffer_current'].value = 1
            else:
                self.simData['/simulation/buffer_current'].value = 0

            # Clear the keypress placed as input to the simulation iteration that just finished.
            self.simData["/control/outputs/keypress"] \
                        [int(self.simData['/simulation/buffer_current'].value)].value = 0

            # The longestDelay are introduced to help interactive modules to re-execute and
            # prevent "lockup" of rendering processes such as cv2.waitKey. waitkey can now have
            # a shorter wait time allowing maximum executino of the full simulation but
            # continue rendering the windows.
            # The longest delay are used to estimate re-execution of modules and need to be reset
            # after every iteration to prevent iteration time to monotonically increase.
            self.simData["/simulation/longestDelay"].value = 0.0

            # Wait for all modules to syncronise and update simulation variables
            self.flags["simulation_next"].wait()
## Start Simulation Step
            info("Iteration {}".format(self.simData["/simulation/iteration"].value))
            t1 = time.time()
            if self.flags["simulation_stop"].is_set():
                break
            ## While loop END

        self.flags["simulation_active"].clear()
        self.flags["simulation_next"].abort()
        self.flags["Module_done"].abort()
        self.flags["simulation_result"].abort()

        info("Waiting for Modules to exit!")

        # Terminate all processes
        for p in process:
            p.join()
        info("Simulation Complete.")
