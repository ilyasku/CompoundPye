## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 12.10.14

"""
@package CompoundPye.src.Surroundings.Stimuli.stimulus
Provides the basic Stimulus class, which can be used to add Stimuli to a Surrounding-object.

@todo check for case of 2 dimensional stimulus
@todo Stimulus.intensities needs to become iterable!
"""

import numpy as np

class Stimulus:
    """
    The basic Stimulus class, which can be used to add a Stimulus to a Surrounding-object.
    
    The user can specify the spatial extend or length of the Stimulus, which creates an array empty array of specified length/extend.
    This array can be filled with arbitrary values representing the visual intensities of the Stimulus. The array will be added to the intensities stored in a Surroundings-object.
    The Stimulus moves in the Surroundings according to the specified velocity.
    """
    def __init__(self,intensity_dim,spatial_extend,starting_point,velocity):
        """
        Initializes a Stimulus object.
        @param intensity_dim Dimension of the intensity, e.g. 1 for a bright-dark Stimulus or 3 for a RGB colored Stimulus.
        @param starting_point Index of the left-most pixel of the stimulus.
        @param velocity Stimulus velocity in pixel/time unit.
        """
    
        if type(starting_point)==int or type(starting_point)==float:
            self.position_in_space=np.array([starting_point])
        else:
            self.position_in_space=np.array(starting_point).astype(np.float32)

        self.index_in_space=[]
        for i in range(0,self.position_in_space.shape[0]):
            self.index_in_space.append(int(self.position_in_space[i])) 
        self.intensities=np.zeros(list(spatial_extend)+[intensity_dim])
        self.spatial_extend=spatial_extend
        self.velocity=np.array(velocity).astype(np.float32)

    def update(self,dt):
        """
        Updates the Stimulus, that is, the Stimulus moves according to its velocity.
        @param dt Time step for the update.
        """
        self.position_in_space+=self.velocity*dt
        self.index_in_space=[]
        for i in range(0,self.position_in_space.shape[0]):
            self.index_in_space.append(int(self.position_in_space[i])) 
        

        
