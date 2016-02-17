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
        periods=n_periods
        
        stimulus.Stimulus.__init__(self,1,extend,starting_point,velocity)
        
        print '----------+++++++++++---------'
        print 'in TwoDimSine:'
        #print relative_periods
        print periods
        print extend

        intensities=np.zeros(extend)
        for k in range(0,2):
            i=1-k
            sin=np.sin(np.arange(0,extend[i])*2*np.pi*periods[i]/extend[i]+phase_shifts[i])*amplitudes[i]+offsets[i]
            for j in range(0,extend[k]):
                intensities[j]+=sin
                   
            intensities=intensities.transpose()
            
        self.intensities[:,:,0]=intensities


        print self.intensities
        print '----------+++++++++++---------'
