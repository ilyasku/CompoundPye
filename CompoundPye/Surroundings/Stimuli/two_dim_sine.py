## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 21.10.14

"""
@package CompoundPye.src.Surroundings.Stimuli.two_dim_sine
Provides the class TwoDimSine, a Stimulus with predefined sines in each of the two Surroundings' dimensions.  
"""


import numpy as np

from . import stimulus



class TwoDimSine(stimulus.Stimulus):
    
    def __init__(self,px_x,px_y,relative_extend,relative_starting_point,relative_velocity,n_periods=[1,1],amplitudes=[.2,.2],offsets=[.25,.25],phase_shifts=[0,0]):

        size=np.array((px_x,px_y)).astype(int)

        extend=(np.array(relative_extend)*size).astype(int)
        starting_point=(np.array(relative_starting_point)*size)
        velocity=(np.array(relative_velocity)*size)
        periods=n_periods
        
        stimulus.Stimulus.__init__(self,1,extend,starting_point,velocity)
        
        intensities=np.zeros(extend)
        for k in range(0,2):
            i=1-k
            sin=np.sin(np.arange(0,extend[i])*2*np.pi*periods[i]/extend[i]+phase_shifts[i])*amplitudes[i]+offsets[i]
            for j in range(0,extend[k]):
                intensities[j]+=sin
                   
            intensities=intensities.transpose()
            
        self.intensities[:,:,0]=intensities


class TwoDimSineRender(stimulus.Stimulus):
    
    def __init__(self,px_x,px_y,relative_extend,relative_starting_point,relative_velocity,n_periods=[1,1],amplitudes=[.2,.2],offsets=[.25,.25],phase_shifts=[np.pi/2.,np.pi/2.]):

        size=np.array((px_x,px_y)).astype(int)

        extend=(np.array(relative_extend)*size).astype(int)
        starting_point=(np.array(relative_starting_point)*size)
        velocity=(np.array(relative_velocity)*size)
        self.args=[n_periods,amplitudes,offsets,phase_shifts]

        self.t=0

        self.xy_grid=np.meshgrid(np.arange(extend[0]).astype(np.float64),np.arange(extend[1]).astype(np.float64))

        
        stimulus.Stimulus.__init__(self,1,extend,starting_point,velocity)

    def two_dim_sine(self,xy_grid,n_periods,amplitudes,offset,phase_shifts):

        intensities=np.zeros_like(xy_grid[0])
    
        intensities=np.sin(2*np.pi*n_periods[0]*xy_grid[0]/intensities.shape[1]+phase_shifts[0])*np.sin(2*np.pi*n_periods[1]*xy_grid[1]/intensities.shape[0]+phase_shifts[1])*amplitudes[0]+offset[0]
        intensities=intensities.transpose()
        
        return intensities


    def update(self,dt):
        self.t=self.t+dt
        dx=int(self.velocity[0]*self.t)
        dy=int(self.velocity[1]*self.t)
        self.xy_grid[0]=self.xy_grid[0]+dx
        self.xy_grid[1]=self.xy_grid[1]+dy
        self.intensities[:,:,0]=self.two_dim_sine(self.xy_grid,*self.args)

