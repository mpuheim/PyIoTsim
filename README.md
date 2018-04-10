# PyIoTsim  
Python IoT Simulator  

Simple demonstration of PyOpenFCM library (fcmlib) in simulated IoT environment.  

Scenario: Navigation of a mobile robot in camera monitored space. 

Depedencies:  
- Python 3.6  
- pygame, requests  
- fcmlib (PyOpenFCM - https://github.com/mpuheim/PyOpenFCM)  

Implementation derived from pyRoSim (https://github.com/mpuheim/pyRoSim)

Short scripts description:  
- setupmap.py - create environment with cameras  
- simulation.py - run offline simulation with simple rule based controller  
- traincams.py - train camera models implemented using fcmlib neuro-fuzzy relations  
- traincontroller.py - train robot controller implemented using fcmlib three-term relations  
- ???.py - run simulation online using fcmlib webapi