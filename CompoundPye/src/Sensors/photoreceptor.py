## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 14.11.14

"""
@package CompoundPye.src.Sensors.photoreceptor

Provides classes (Sensors) that emulate a photoreceptor cell as in van Hateren and Snippe's paper 
'Information theoretical evaluation of parametric models of gain control in blowfly photoreceptor cells',2001.
"""

import sensor
import numpy as np

#import MotionDetectorModel.EH as EH

class SensorWiener(sensor.Sensor):
    """
    
    """    
    def __init__(self,filter_func,func_params=[],time_const=0.0,normalize=False,debug=[]):
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
    
    def __init__(self,time_const_lp3=3.0,time_const=0.0,normalize=False,debug=[]):     
        SensorWiener.__init__(self, M_DWM_Wiener,[], time_const,normalize, debug)
        
        self.current_DWM_values=[[0,0,1],1,1,1]
        
        self.time_const_lp3=time_const_lp3


    def update(self,intensities):
        sensor.Sensor.update(self,intensities)
        if self.debug.count('Photoreceptor.update'):
            print '--- debugging Photoreceptor.update() ---'
            print self.value
        output=M_DWM(self.value, self.current_DWM_values, self.dt,time_const_lp3=self.time_const_lp3)
        self.value=output[0]
        self.current_DWM_values=output[1:]
        
        if self.debug.count('Photoreceptor.update'):
            print output
            print '---------------------------------'
        
        self.history[1:]=self.history[:-1]
        self.history[0]=self.value
        
        self.value=(self.history*self.wiener).sum()*self.dt#*self.history.shape[0]
        
        
        
        
        
def M_DWM_Wiener(dt,A=3.13*10**-6,tau=0.000535,n=11):
    t_end=0.025
    steps=np.arange(0,t_end/dt)
    filter=A*(steps*dt/tau)**n*np.exp(-steps*dt/tau)
    return filter
        
        
def M_DWM(input,current_values,dt,time_const_lp1=0.00169,time_const_lp2=0.0718,time_const_lp3=0.1,k1=0.689,k2=9.07):
    '''
    @param needs to contain the current values of the low-pass filters and the first nonlinearity. ([lp1,lp2,nonlin])
    '''
    lp1_0=low_pass(input,current_values[0][0],time_const_lp1,dt)
    lp1_1=low_pass(lp1_0,current_values[0][1],time_const_lp1,dt)
    lp1=low_pass(lp1_1,current_values[0][2],time_const_lp1,dt)
    
    div1=lp1/current_values[1]
    
    lp2=low_pass(lp1,div1,time_const_lp2,dt)
    
    div2=div1/current_values[3]
    #print 'div1='+str(div1)
    #print 'div2='+str(div2)

    lp3=low_pass(div2,current_values[2],time_const_lp3,dt)
    nonlin=k1*np.exp(k2*lp3)
    #print nonlin
    #print exp_lp3
    nonlin1=div2/(1+div2)
    
    return nonlin1,[lp1_0,lp1_1,lp1],lp2,lp3,nonlin

def low_pass(input,current_value,time_const,dt):
    #print dt
    #print time_const
    alpha=dt/(time_const+dt)
    return current_value*(1-alpha)+alpha*input
