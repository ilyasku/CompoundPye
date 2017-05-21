## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 12.10.14

"""
@package CompoundPye.src.Surroundings.one_dim
Provides the class OneDim, to create one-dimensional Surroundings.
"""

import numpy as np

from . import Stimuli

class OneDim:
    """
    The basic Surroundings-class to create one dimensional Surroundings-objects, which handles the 'Surroundings of the motion detector'.
    
    A Surroundings-object is the tool to handle the Surroundings of the motion detector. It holds 'the world' that Sensors of a Circuit/network can see.
    It stores Stimuli and from them calculates the intensities at each pixel of the Surroundings.
    The Surroundings are thought of as indeed surrounding the agent, so sometimes angles are used to specify a location in the Surroundings (from 0 to 360 degree in the one dimensional case).
     
    """
    def __init__(self,n_pixel=2**10,intensity_dimension=1): #stimulus dimension?==colors?==RGB?
        """
        Creates a OneDim-object.
        @param n_pixel Number of pixels of the Surroundings.
        @param intensity_dimension Dimension of the intensities, e.g. 1 for bright-dark or 3 for RGB colored Stimuli.
        """
        self.n_pixel=n_pixel
        
        self.intensities=np.zeros((n_pixel,intensity_dimension))
        self.stimuli=[]
        
    def set_sensor(self,sensor,phi_min,phi_max):
        """
        Sets a Sensor's receptive field to given angles.
        @param sensor Sensor-object of which the receptive field should be set.
        @param phi_min Minimum angle of the Surroundings that can be observed by the Sensor.
        @param phi_min Maximum angle of the Surroundings that can be observed by the Sensor.
        """
        sensor.receptive_field=[[phi_min,phi_max]]
        
        
    def update(self,dt):
        """
        Updates the agent's Surroundings, that is, it updates all stimuli stored in OneDim.stimuli.
        @param dt Time step for the update.
        """
        self.intensities=np.zeros(self.intensities.shape)
        for stim in self.stimuli:
            stim.update(dt)
            #self.intensities[self.stimuli[i].index_in_space%self.n_pixel:(self.stimuli[i].index_in_space+self.stimuli[i].spatial_extend)%self.n_pixel]=self
            stim.index_in_space[0]=stim.index_in_space[0]%self.n_pixel
            
            overshoot=stim.index_in_space[0]+stim.spatial_extend[0]-1-self.n_pixel
            #print overshoot
            if overshoot<0:
                self.intensities[stim.index_in_space[0]:stim.index_in_space[0]+stim.spatial_extend[0]]+=stim.intensities
                
            else:
                self.intensities[stim.index_in_space[0]:]+=stim.intensities[:-overshoot-1]
                self.intensities[:overshoot+1]+=stim.intensities[stim.intensities.shape[0]-overshoot-1:]
        
    def add_stimulus(self,object,object_params,object_params_dict):
        """
        Adds a new Stimulus to the list of stimuli.
        @param object A class to create the new Stimulus-object.
        @param object_params List of parameters to pass on to the constructor of the class.
        @param object_params_dict Dictionary of keyword-parameters to pass on to the constructor of the class.
        """
        new_stimulus=object(*object_params,**object_params_dict)
        self.stimuli.append(new_stimulus)
