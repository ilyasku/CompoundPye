## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 08.10.14

"""
@package CompoundPye.src.Circuits
Provides Circuit-objects, which handle the complete network of Component-objects (components or neurons).
"""
#from ...src import settings as _settings
from ..settings import cv

import circuit

if cv==True:
    import circuit_array
