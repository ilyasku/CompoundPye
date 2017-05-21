## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 22.01.15

"""
@package CompoundPye.src.Surroundings.Stimuli.two_dim_box
Provides the class TwoDimBox, a Stimulus with predefined box-shape.  
"""

import numpy as np

from . import stimulus

class TwoDimBox(stimulus.Stimulus):
    def __init__(self,px_x,px_y,relative_extend,relative_starting_point,relative_velocity,amplitude=0.5):

        size=np.array((px_x,px_y)).astype(int)

        extend=(np.array(relative_extend)*size).astype(int)
        starting_point=(np.array(relative_starting_point)*size)
        velocity=(np.array(relative_velocity)*size)
        
        stimulus.Stimulus.__init__(self,1,extend,starting_point,velocity)
    
        intensities=np.ones(extend)*amplitude

        self.intensities[:,:,0]=intensities

        
