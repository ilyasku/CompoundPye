## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 08.10.14
#
# @todo current_DWM_values exists only for photoreceptors, not for blank sensors.

# modified: 31.01.16

"""
@package CompoundPye.src.system
This file holds the class System, which handles the communication between Surroundings- and Circuit-objects.
"""

trace_length=500
import numpy as np
import sys

## Handles communication between Surrounding- and Circuit-objects
class System:
    
    def __init__(self,circuit,surroundings,dt,relaxation_time=1,relaxation_intensity=0.5,relax_calculation='simple_photoreceptor'):
        self.circuit=circuit
        self.surroundings=surroundings
        self.dt=dt
        self.sensors_to_track=[]
        self.components_to_track=[]
        self.track_data={'components':{},'sensors':{}}

        for s in self.circuit.sensors:
            s.set_dt(dt)
        
        self.initial_relaxation(relaxation_time, relaxation_intensity,relax_calculation)
        
            
        
    def initial_relaxation(self,t_relax,I,mode):
        t=0
        if type(I)==float or type(I)==int or type(I)==np.float64:
            self.surroundings.intensities=np.ones(self.surroundings.intensities.shape)*I
        elif type(I)==np.ndarray:
            self.surroundings.intensities=I
        if mode=='simple_photoreceptor':
            progress=0
            #sys.stdout.write('[%-20s] %d%% of t_end' % ('='*(progress/5), progress))
            while t<t_relax:
                self.circuit.sensors[0].update(self.surroundings.intensities)
                t+=self.dt
                count=0
                '''
                if count%50==0:
                    progress=int(t/t_relax*100)
                    sys.stdout.write('\r')
                    sys.stdout.write('[%-20s] %d%% of t_end' % ('='*(progress/5), progress))
                    sys.stdout.flush()
            sys.stdout.write('\n')
            '''
                #print 'relaxation: '+str(t/t_relax*100)+'% urks'
            sys.stdout.write('relaxation done\n')
            for i in range(1,len(self.circuit.sensors)):
                self.circuit.sensors[i].current_DWM_values=self.circuit.sensors[0].current_DWM_values
                self.circuit.sensors[i].value=self.circuit.sensors[0].value
        elif mode=='none':
            pass
        else:
            while t<t_relax:
                self.circuit.update(self.dt,self.surroundings.intensities)
                t+=self.dt
            sys.stdout.write('relaxation done\n')
        
    def update(self):
        """
        @todo comment this function
        @todo add tracking of components
        """
        global trace_length
        
        self.surroundings.update(self.dt)
        self.circuit.update(self.dt,self.surroundings.intensities)
        
        for i in self.sensors_to_track:
            if self.track_data['sensors'].keys().count(i):
                #array=np.zeros(trace_length)
                #array[:-1]=self.track_data['sensors'][i][1:]
                #array[-1]=self.circuit.sensors[i].get_value()
                self.track_data['sensors'][i][:-1]=self.track_data['sensors'][i][1:]
                self.track_data['sensors'][i][-1]=self.circuit.sensors[i].get_value()
            else:
                new_array=np.zeros(trace_length)
                new_array[-1]=self.circuit.sensors[i].get_value()
                self.track_data['sensors'][i]=new_array
                
        for i in self.components_to_track:
            if self.track_data['components'].keys().count(i):
                self.track_data['components'][i][:-1]=self.track_data['components'][i][1:]
                self.track_data['components'][i][-1]=self.circuit.components[i].get_output()
            else:
                new_array=np.zeros(trace_length)
                new_array[-1]=self.circuit.components[i].get_output()
                self.track_data['components'][i]=new_array
        
#class SystemVideoOutput(System):
    
    #def __init__(self,circuit,surroundings,dt,outputfile):
