## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 14.11.14

"""
@package CompoundPye.src.Sensors.photoreceptor

Provides classes (Sensors) that emulate a photoreceptor cell as in van Hateren and Snippe's paper 
'Information theoretical evaluation of parametric models of gain control in blowfly photoreceptor cells',2001.
"""

from . import sensor
import numpy as np

#import MotionDetectorModel.EH as EH

class SensorWiener(sensor.Sensor):
    """
Van Hateren and Snippe's photoreceptor model relies on a Wiener filter; so this is a implementation of 
the Wiener filter they used as Sensor object compatible with CompoundPye.
    """    
    def __init__(self,filter_func,func_params=[],time_const=0.0,normalize=False,debug=[]):
        """ Constructor of SensorWiener .
@param filter_func (Pointer to) filter function.
@param func_param List of parameters to be passed on to the filter function.
@param time_const Time constant used when updating.
@param normalize Boolean, determining whether to normalize output or not.
@param debug List of debug strings in case you want to see debugging output.
        """
        sensor.Sensor.__init__(self,normalize=normalize,time_const=time_const,debug=debug)
        
        self.dt=None
        self.wiener=None
        self.history=None
        
        self.filter_func=filter_func
        self.func_params=func_params

    def set_dt(self,dt):
        self.dt=dt
        self.wiener=self.filter_func(dt,*self.func_params)
        self.history=np.zeros(self.wiener.shape)
        
    def update(self,intensities):
        
        sensor.Sensor.update(self,intensities)
        
        self.history[1:]=self.history[:-1]
        self.history[0]=self.value
        
        self.value=(self.history*self.wiener).sum()*self.dt#*self.history.shape[0]
        
        
class Photoreceptor(SensorWiener):
    """ Implementation of van Hateren and Snippe's photoreceptor model as a CompoundPye sensor.
    """
    def __init__(self,time_const_lp3=3.0,time_const=0.0,normalize=False,debug=[]):     
        """ Constructor of class Photoreceptor .
@param time_const_lp3 Time constant of low-pass filter LP3 (see https://github.com/ilyasku/CompoundPye/wiki)
@param time_const Useless parameter here, included to use identical syntax in GUI ...
@param normalize Boolean, determining whether to normalize output or not.
@param debug List of debug strings in case you want to see debugging output.
        """
        SensorWiener.__init__(self, M_DWM_Wiener,[], time_const,normalize, debug)
        
        self.current_DWM_values=[[0.0,0.0,1.0],1.0,1.0,1.0]
        
        self.time_const_lp3=time_const_lp3


    def update(self,intensities):
        sensor.Sensor.update(self,intensities)
        if self.debug.count('Photoreceptor.update'):
            print('--- debugging Photoreceptor.update() ---')
            print(("value = "+str(self.value)))
        output=M_DWM(self.value, self.current_DWM_values, self.dt,time_const_lp3=self.time_const_lp3)
        self.value=output[0]
        self.current_DWM_values=output[1:]
        
        
        self.history[1:]=self.history[:-1]
        self.history[0]=self.value
        
        self.value=(self.history*self.wiener).sum()*self.dt#*self.history.shape[0]
        
        if self.debug.count('Photoreceptor.update'):
            print("DWM output:")
            print(output)
            print('---------------------------------')
        
        
        
        
def M_DWM_Wiener(dt,A=3.13*10**-6,tau=0.000535,n=11):
    t_end=0.025
    steps=np.arange(0,t_end/dt)
    filter=A*(steps*dt/tau)**n*np.exp(-steps*dt/tau)
    return filter
        
        
def M_DWM(input,current_values,dt,time_const_lp1=0.00169,time_const_lp2=0.0718,time_const_lp3=3.0,k1=0.689,k2=9.07):
    """
    @param input Intensity (float of domain [0,1]) that the sensor receives.
    @param current_values List/tuple of M_DWM values of previous function call.
    @param dt Time step.
    @param time_const_lp1 [float] Time constant of first low-pass filter.
    @param time_const_lp2 [float] Time constant of second low-pass filter.
    @param time_const_lp3 [float] Time constant of third low-pass filter.
    @param k1 [float] Constant of first nonlinearity.
    @param k2 [float] Constant of output nonlinearity. 
    @return Tuple of outputs of the different components. 
    Contains 5 items:
    1. Output of the filter.
    2. List of 3 outputs of the first low-pass filter (third order?).
    3. Output of second lp filter.
    4. Output of third lp filter.
    5. Output of first nonlinearity.
    Items 2-5 serve as parameter current_values for next function call.
    """
    lp1_0=low_pass(input,current_values[0][0],time_const_lp1,dt)
    lp1_1=low_pass(lp1_0,current_values[0][1],time_const_lp1,dt)
    lp1=low_pass(lp1_1,current_values[0][2],time_const_lp1,dt)
    
    div1=lp1/current_values[1]
    
    lp2=low_pass(lp1,div1,time_const_lp2,dt)
    
    div2=div1/current_values[3]

    lp3=low_pass(div2,current_values[2],time_const_lp3,dt)
    nonlin=k1*np.exp(k2*lp3)

    nonlin1=div2/(1+div2)
    
    return nonlin1,[lp1_0,lp1_1,lp1],lp2,lp3,nonlin

def low_pass(input,current_value,time_const,dt):
    alpha=dt/(time_const+dt)
    return current_value*(1-alpha)+alpha*input
