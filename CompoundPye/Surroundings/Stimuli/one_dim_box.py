## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 12.10.14

"""
@package CompoundPye.src.Surroundings.Stimuli.one_dim_box
Provides the class OneDimBox, a Stimulus with a predefined box-shape of given length.
"""

from . import stimulus
import numpy as np


class OneDimBox(stimulus.Stimulus):
    """
    OneDimBox is a Stimulus with a predefined box-shape of given length.
    
    The user can specify the length, starting point, velocity and intensity when creating an object of this class.
    Spatial values need to be specified in pixels of the Surrouding's intensities-array (see MotionDetectorModel.Surroundings.one_dim.OneDim.intensities). 
    """
    
    def __init__(self,length,starting_point,velocity,intensity=1):
        """
        Initializes a OneDimBox-object.
        @param length Length of the box in pixels.
        @param starting_point Index of the left-most pixel of the box.
        @param velocity Stimulus velocity in pixel/time unit.
        @param intensity Height/intensity of the stimulus. 
        """
        
        stimulus.Stimulus.__init__(self,1,[length],starting_point,velocity)
        
        self.intensities=np.ones(self.intensities.shape)*intensity
        
