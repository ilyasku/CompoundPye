## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 12.10.14

"""
@package CompoundPye.src.Surroundings.Stimuli.one_dim_box
Provides the class OneDimSine, a Stimulus with a predefined sine-shape of given length.
"""

from . import stimulus
import numpy as np

class OneDimSine(stimulus.Stimulus):
    """
    OneDimSine is a Stimulus with a predefined sine-shape of given length.
    
    The user can specify the length, starting point, velocity and some sine specific parameters when creating an object of this class.
    Spatial values need to be specified in pixels of the Surrouding's intensities-array (see MotionDetectorModel.Surroundings.one_dim.OneDim.intensities). 
    """
    
    def __init__(self,length,starting_point,velocity,n_periods=1.,amplitude=.5,phase_shift=0.0,offset=.5):
        """
        Initializes a OneDimSine-object.
        @param length Length of the sine-wave in pixels.
        @param starting_point Index of the left-most pixel of the stimulus.
        @param velocity Stimulus velocity in pixel/time unit.
        @param n_periods Number of periods in the length of the stimulus.
        @param amplitude Amplitude of the sine-wave.
        @param phase_shift Initial phase shift (if you do not want the sine-wave to start at sin(0)).
        @param offset Offset that is added to the sine function. 
        """
        stimulus.Stimulus.__init__(self,1,[length],starting_point,velocity)
        
        
        self.intensities.transpose()[0]=np.sin((np.arange(0,length)*n_periods*2.*np.pi/length)+phase_shift)*amplitude+offset
        
        
