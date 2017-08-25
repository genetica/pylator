-------------------------------------------------------------------------------
25-08-2017 - gene
-------------------------------------------------------------------------------
With my lack of knowledge in multiprocessing I have found a few, I'll almost 
call them, guidelines. Checking if an Event() is set takes a lot of time, 
thus
While Event().is_set():
    #some code
Is very slow in checking the flag. For highly iterative quick tasks, find
another way.

I have come to the conclusion that I will have to pickle a dictionary 
to every process containing the ctype handle created by multiprocessing
module. This is different from just sending data pointers to every process
as the multiprocessing assist in creating a generic pointer that every
process can use as pointers are usually referenced to the start of the 
current process memory block and not absolute.

-------------------------------------------------------------------------------
21-08-2017 - gene
-------------------------------------------------------------------------------

Events help me control the processes individual. I have a flag and set it 
to indicate certain status or clear it or wait for another process to set
it. For multiple process wanting to all say they completed a certain stage
the usage of Barriers are more efficient. A Barrier wait for a set amount
of process to reach it where after it releases all the processes currently 
at it, it can also be re-used multiple times.

-------------------------------------------------------------------------------
15-08-2017 - gene
-------------------------------------------------------------------------------

The usage of a Manager() sounds great. Add arbitrary data to the manager
and share it over multiple processes, it even allow distributed computing
to share variables. Unfortunatley for big data it is terrible.
Managerd pickle the data to a process and then pickle the changed data back 
to itself ensuring concurrency. Managers does not work with binary objects 
in the sense that the manager can not detect whether data change within the 
object or not. Managers as I see it can be used for control and moving
data for distributed computing.

-------------------------------------------------------------------------------
11-08-2017 - gene
-------------------------------------------------------------------------------
It is important to have a fast simulation. A current question that I am 
pondering. To collect thoughts. A program can run as threaded, still actively
sharing the same CPU cache. As multi-processing thus using physical different
CPU cores and not sharing cache. It is possible for two CPUs to share
RAM and using semaphores to keep concurrency. Then there is distributed 
computing which I will just ignore currently. Semaphores are not required if
programming is done correctly but some control will still be required. The
simulation modules should either run as a thread or as a process. What would
the trade-off be, spawning multiple threads and executing them in the right
order RAM access will be reduced as the right data is already in the cache
but speed is limited to the clock of the core. Processes will increase RAM
access but speed is limited to a factor of the amount of cores. We assume
a single access bus to the RAM. Only a single CPU core can access the RAM
at a time (physical constraint) thus in essence the maximum speed of the 
processes is then limited by the speed of the RAM bus. I should look at how
these limits can be calculated per machine and what trade-offs can be made.
I currently feel like processes will be the most flexible as controlling 
what data are stored in the CPU cache is not that easy with current 
frameworks. Modules will currently be spawned as processes. 

It will be an interesting endeavour to design an algorithm (learning or 
traditional) that analyses all the loaded modules and decide which modules
should be packed together in a process and multiple threads and which modules
should live as their own process.

-------------------------------------------------------------------------------
10-08-2017 - gene
-------------------------------------------------------------------------------
An interesting GUI platform, maybe for future interface:
www.fltk.org
I found a platform openeaagles or more a Mixed  Reality Simulation Platform
specifically for building and simulating real "systems" in an environment.
Might be useful for complete 3D world interface. It also connects well with
Outerra, a 3D engine for planetary rendering using real data, but its paid.
Another interface is JSBSim ,an open source flight dynamics & control 
software library in C++. Maybe interfacing with 3d generators such as Blender
and the unreal engine for world simulation.

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
