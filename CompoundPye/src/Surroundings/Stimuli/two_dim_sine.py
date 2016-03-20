## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 21.10.14

"""
@package CompoundPye.src.Surroundings.Stimuli.two_dim_sine
Provides the class TwoDimSine, a Stimulus with predefined sines in each of the two Surroundings' dimensions.  
"""


import numpy as np

import stimulus



class TwoDimSine(stimulus.Stimulus):
    
    def __init__(self,px_x,px_y,relative_extend,relative_starting_point,relative_velocity,n_periods=[1,1],amplitudes=[.2,.2],offsets=[.25,.25],phase_shifts=[0,0]):

        size=np.array((px_x,px_y)).astype(int)

        extend=(np.array(relative_extend)*size).astype(int)
        starting_point=(np.array(relative_starting_point)*size)
        velocity=(np.array(relative_velocity)*size)
        self.args=[n_periods,amplitudes,offsets]

        self.t=0

        self.xy_grid=np.meshgrid(np.arange(extend[0]),np.arange(extend[1]))

        
        stimulus.Stimulus.__init__(self,1,extend,starting_point,0)

    def two_dim_sine(self,t,xy_grid,n_periods,amplitudes,offset):

        intensities=np.zeros_like(xy_grid[0])
    
        intensities=np.sin(t*n_periods[0]*xy_grid[0]/intensities.shape[0])*np.sin(t*n_periods[1]*xy_grid[1]/intensities.shape[1])*amplitudes[0]+offset[0]
        intensities=intensities.transpose()
        
        return intensities


    def update(self,dt):
        self.t=self.t+dt
        self.intensities[:,:,0]=self.two_dim_sine(self.t,self.xy_grid,*self.args)
