-------------------------------------------------------------------------------
31-07-2017 - gene
-------------------------------------------------------------------------------
Before the simulator itself can be developed test tools are required. On 
such tool is an interface tool (To configure the simulator). Before files are
specified and developed an easy way to do the configuration is required.

It has been decided that excel will "for now" be the configurator for the
simulator coupled with python scripts to generate the correct interface files.
pandas will be used to interface with excel followed by creating the interface
to the simulator. Using VB scripts for the excel configuration would make it
more difficult to later change input or format. This is the reason for using
pandas as the base datastructure.

The final configuration file for the simulator will end up being a dictionary
with entries defined equivalent to a file structure.

-------------------------------------------------------------------------------
24-07-2017 - gene
-------------------------------------------------------------------------------
A fair amount of time has been spent on deciding on a data storage mechanism 
and how a user will insert module connectivity and configuration into the
simulator.
Ideally a GUI interface would be great. This is not priority now.

-------------------------------------------------------------------------------
17-07-2017 - gene
-------------------------------------------------------------------------------
The purpose is to build a simulator equivalent to what is available in 
Simulink. In explanation, linking different blocks with various inputs and
outputs and simulating their effect. 
The current projects available in python seems to not be suited for my 
purpose. I might be missing a few projects or not grasping all aspect of the 
available python projects out there and would appreciate any suggestions or 
pointers.
Some main features:
    Multiprocessing capability per block (I will call them modules).
    Modules must support any set of code. Such as a mathematical functions,
    GUI interfaces for users, interfaces to FEM simulators etc.

The purpose of the pylator:
    To simulate physical systems including user interactions.

The philosophy for the simulator is such as to assume that every module 
execute every iteration without its inputs changing in-between. Every module
should be defined only by inputs, outputs and constants. All outputs 
should have initial/default values. To enable successful multiprocessing 
data must be shared in the case of single machine simulation, in other 
cases interfaces such as MPI should be used.
