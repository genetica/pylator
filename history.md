-------------------------------------------------------------------------------
30-08-2017 - gene
-------------------------------------------------------------------------------
The Model class are in a usable condition. This class is built on 
multiprocessing class Process and can be inherited by the the user modules.
The generic functions to build the simulation dictionary is not yet completed
and currently this must be completed manually:
    createModuleDictionary(self)
    updateSimulationVariables(self)
    updateInputVariables(self)
    setOutputVariables(self)
    updateOutputVariables(self)
The user then need to define the following function:
    initialise(self, simData)
    execute(self, simData)
    finalise(self, simData) 
simData in this case is the module specific dictionary which in the end
of the execution cycle update the real simulation dictionary. Although
all shared arrays are still the same memory space.

The Scheduler class are created that define how the simulation are 
executed. Currently the function for creating the general simulation 
dictionary must still be created and the user need to write this function
themselve.
    create_sim_data(self)

Also the Scheduler does not currently use any inset data such as the 
connectivity matrix, it only use the manually generated script_info which
define which modules to load and execute.

In summary the schedular currently only load modules and execute and change
the current requested buffer pointer.

-------------------------------------------------------------------------------
25-08-2017 - gene
-------------------------------------------------------------------------------
Was awaiting approval to continue work.

Has developed Model.py and sim.py. Building a module class on top of the
multiprocessing Process class. The class Module will be required for every
module to be used and will be imported as Module, the user will require to
override the function execute and have access to simData. self.simData also
exist but more readable code will be developed to just use simData, self is 
very cluttering.

This is not working code currently.
A folder streamTest was also added, this folder contains different tests that
was executed and played around with to figure the multiprocessing module and
different speed executions.

Note, accessing dictionary entries iterativley is very slow compared to 
storing the reference in a new variable directly. 

Guideline will need to be provided to users that write the Module code
just to keep speed up etc.

-------------------------------------------------------------------------------
11-08-2017 - gene
-------------------------------------------------------------------------------
Currently the input/output to sim is performed through excel files. The files
are read as pandas dataframes and then converted to a data dictionary which 
will be used in the simulation and converted to shared c-types.
The process in starting currently is as follow:
- Use moduleIOInterface.py to create a base Module excel file.

- Use moduleScenario.py to create a scenario file of the specific module
    this is basically a copy of the base Module excel file with added name
    to specify the scenario.

Use simInputModule.py 
- Execute function createEmptySim
    create empty sim file with scenario specifications containing
    empty ModelList
    empty matrix connectivity
    basic global variables required
    The ModelList spreadsheet can then be filled in with the required 
    modules name, python file of module and specific scenario file.
    Additional global variables can be added.
    
- Execute function getModulesForSim
    This retrieve all the scenario files for the modules and add them as 
    spreadsheets in the simulation file.
    The scenario files can be modified and updated and the original files
    can be updated with updateModulesFromSim.
    and Modules can be reupdated by updateSimFromModules

- Execute function createConnectivityMatrix
    This reads all scenario files and generate an empty connectivity matrix
    The matrix use all inputs/outpus that "exposed" is set to true. Constants
    are not added to the matrix. All globals are added to the matrix as 
    outputs.
    The matrix can be filled in by making crosses at required connections.

- Execute updateFilesFromSim
    This stores the ModelList, Matrix and Globals into seperate scenario 
    files which can be recalled and modifed and re-updated with
    updateSimFromFiles. Each spreadsheet can also be updated seperatly.

- Execute function getSimData
    This creates the simData dictionary for the simulator. Read, generate and
    convert all initial values into the dictionary as shared c types.
    (This function must still be completed.)
    
-------------------------------------------------------------------------------
17-07-2017 - gene
-------------------------------------------------------------------------------
Pylator Goal:
    To simulate physical systems including user interactions.
    Replace simulink and be more flexable.

Features:
    Multiprocessing
    Recall previous simulation states
    Configure different Scenarios where each modules can be configured uniquely.

Definitions:
    Module:
        The unit/block which performs a function, can be multiple functions 
        on a set of inputs and produce a set of outputs per iteration.