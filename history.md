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