##@author Ilyas Kuhlemann
#@contact ilyasp.ku@gmail.com
#@date 30.01.16
#
#@mainpage CompoundPye
#
#@section overview Overview
#
#This package provides tools to model the motion detector of Drosophila's visual system. It is designed for easy set-up of columnar structured neural networks, as in arthropods' compound eyes.
#
#
#@section req Requirements
#
# CompoundPye was tested on Ubuntu 14.04 with Python 2.7 only. \n
# It requires following modules:
# <UL>
# <LI> NumPy</LI>
# <LI> SciPy</LI>
# <LI> OpenCV for python (cv2) </LI>
# <LI> NetworkX </LI>
# <LI> PyQt4 </LI>
# </UL>
#
#@section structure Structure
#
# To get an idea of how to use the module, a good starting point is to run cp_GUI.py. This should start CompoundPye's main GUI, where you can set up neural circuits, decide which stimuli to show to the modelled visual system, and start a simulation.
#\n
# BEWARE: No usage example yet, and GUI tool-tips still missing, so setting up simulations without instructions will be hard.\n
#
#\image html program_simple_overview_with_GUI.png

"""
This file initializes the CompoundPye package. It is a framework for modelling and simulation of columnar structured neural networks, as in Artrhopod's compound eyes.
"""

from src import *
