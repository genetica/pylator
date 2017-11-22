pylator

Programming environment for modeling, simulating and analysing multidomain 
dynamical systems. Can be used for automaic control,
digital signal processing of multidomain simulation, Model-Based Design 
and Model-Based verification and operation with real-time systems.

Currently it provides automatic multi-core processing
of the different modules but aim to automatically divide multi-threading, 
multiprocessing(GPU and CPU) and distributed computing on start-up.

-------------------------------------------------------------------------------
Getting Started
-------------------------------------------------------------------------------

Add folder "./pylator" to python import path by using pylator.pth in 
site-packages.

Look within the folder "./testSims" for base projects. These projects use 
example modules in "./modules".
To run an example go to the folder "./testSims" and execute
    python sine_sim.py