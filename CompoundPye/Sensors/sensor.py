## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.14

"""
@package CompoundPye.src.Sensors.sensor
Holds the basic Sensor class.

@todo find a solution for adding the right path to sys.path
"""

#import sys
#sys.path.append('..')
#sys.path.append('MotionDetectorModel/')
if __name__.count('.') == 0 and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from Components.Connections import connection
else:
    from ..Components.Connections import connection

from . import filter_funcs as ff

import numpy as np

cut_off=0.01

class Sensor:
    """
    Basic Sensor class.
    
    Sensors can be used in a Circuit to look at the Surroundings and provide sensory information to the Circuit.
    They can have (and should have, to be of any use) connections to Components in the circuit. Preferably, one should use input filters (== special Components) to down regulate or up regulate the 
    arbitrary outputs of a sensor. This regulation is not implemented in Sensors itself yet.
    """
    
    def __init__(self,normalize=False,time_const=0.0,debug=[]):
        """
        Initializes a Sensor-object with given input dimension.
        @param time_const The Sensor's time constant, which specifies how much of its previous Component.value remains after each update step.
        """
        self.connections=[]
        self.time_const=time_const
        self.value=0
        self.normalize=normalize
        

        self.receptive_field_set=False
        self.receptive_field=None
        self.filter=None
        self.normalization_factor=1.
        
        self.label=''
        self.group=''

        self.neighbours_horizontal=[]
        self.neighbours_vertical=[]

        self.debug=debug
        
    def add_connection(self,weight,target):
        """
        Adds a Connection from the Sensor to a Component.
        @param weight Strength of the Connection.
        @param target Component-object that is to be the target of the Connection. 
        """
        new_connection=connection.Connection(weight,target)
        self.connections.append(new_connection)
        
    def update(self,intensities):
        """
        Updates the sensory information that the Sensor provides.
        
        As input one has to provide the intensities of a Surrounding-object. The actual input to this sensor is then calculated using the angles stored in Sensor.receptive_field .
        Before that is possible, though, one has to set what the Sensor can see, preferably using the function MotionDetectorModel.Surroundings.one_dim.OneDim.set_sensor or similar functions of more dimensional Surrounding-objects.
        @param intensities Intensities stored in a Surrounding-object (see MotionDetectorModel.Surroundings.one_dim.OneDim.intensities).
        @note The actual calculation happens in separate one or two dimensional update-functions.
        """
        
        if self.receptive_field_set==False:
            print('WARNING: Sensor not set! (It does not know where to look for inputs.)')
        else:     
            if self.receptive_field.shape[0]==1:
                self._update_one_dim(intensities)
            elif self.receptive_field.shape[0]==2:
                self._update_two_dim(intensities)
            else:
                pass
        if self.debug.count('Sensor.update'):
            print('---- debugging Sensor.update ----')
            print(self.value)
            print('-----------------')
        
    def get_value(self):
        """
        Read the current output value of the Sensor.
        @return Current output value.
        """
        return self.value
    
    def set_receptive_field(self,px,rel_center,filter='gaussian',filter_params=[],filter_kw_params={}):
        """
        Sets the receptive field of a sensor.
        
        Sensors do not 'see' anything before their receptive field is set.
        @param center Center of the neuron's receptive field (in relative size).
        @param filter Keyword (string) for a certain filter; at the moment only 'gaussian' works.
        @param filter_params List of parameters to be passed on to the filter function.
        @param filter_kw_params Dictionary of keyword-parameters to be passed on to the filter function.
        """



        global cut_off
        
        

        if type(rel_center)==int or type(rel_center)==float:
            rel_center=[rel_center]
        if type(px)==int or type(px)==float:
            px=[px]
        
        
        rel_center=np.array(rel_center)
        px=np.array(px)

        center=rel_center*px
        
        
        
        if filter=='gaussian':
            if center.shape[0]==1:
                filter_func=ff.one_dim_gauss
            elif center.shape[0]==2:
                filter_func=ff.two_dim_gauss
        elif filter=='pixel':
            if center.shape[0]==1:
                filter_func=ff.pixel_one_dim
            elif center.shape[0]==2:
                filter_func=ff.pixel_two_dim
        
        

        self.filter=filter_func(cut_off,px,*filter_params,**filter_kw_params)
        self.receptive_field=center-(np.array(self.filter.shape[:2])-1)/2.0
        self.normalization_factor=self.filter.sum()

        for i in range(0,self.receptive_field.shape[0]):
            self.receptive_field[i]=max(self.receptive_field[i],0)
        

        self.receptive_field_set=True
        #print '------------set receptive field-----------------'
        
        #print 'center:'
        #print center
        #print 'filter shape:'
        #print self.filter.shape
        #print 'receptive field'
        #print self.receptive_field

        #print '------------------------------------------------'

        
        
        
    def _update_one_dim(self,intensities):
        """
        Updates the sensory information that the Sensor provides (one-dimensional surroundings).
        
        As input one has to provide the intensities of a Surrounding-object. The actual input to this sensor is then calculated using the angles stored in Sensor.receptive_field .
        Before that is possible, though, one has to set what the Sensor can see, preferably using the function MotionDetectorModel.Surroundings.one_dim.OneDim.set_sensor or similar functions of more dimensional Surrounding-objects.
        @param intensities Intensities stored in a Surrounding-object (see MotionDetectorModel.Surroundings.one_dim.OneDim.intensities).
        """

        if self.debug.count('Sensor.update'):
            print('---- debugging Sensor._update_one_dim ----')
            #print field.sum()
            #print int(self.receptive_field[0])
            #print int(self.receptive_field[0])+self.filter.shape[0]
            print(intensities.shape)
            #print intensities
            print(intensities[int(self.receptive_field[0]):int(self.receptive_field[0])+self.filter.shape[0],0])
            print('----------------------')


        field=intensities[int(self.receptive_field[0]):int(self.receptive_field[0])+self.filter.shape[0],0]*self.filter        

        self.value=field.sum()
        if self.normalize:
            self.value=self.value/self.normalization_factor
        
    
    def _compute_input_two_dim(self,intensities):
        
        if len(intensities.shape)==3:

            field=intensities[int(self.receptive_field[0]):int(self.receptive_field[0])+self.filter.shape[0],
                              int(self.receptive_field[1]):int(self.receptive_field[1])+self.filter.shape[1],0]*self.filter
        elif len(intensities.shape)==2:
            field=intensities[int(self.receptive_field[0]):int(self.receptive_field[0])+self.filter.shape[0],
                              int(self.receptive_field[1]):int(self.receptive_field[1])+self.filter.shape[1]]*self.filter
            
        
        return field.sum()


    def _update_two_dim(self,intensities):
        """
        Updates the sensory information that the Sensor provides (two-dimensional surroundings).
        
        As input one has to provide the intensities of a Surrounding-object. The actual input to this sensor is then calculated using the angles stored in Sensor.receptive_field .
        Before that is possible, though, one has to set what the Sensor can see, preferably using the function MotionDetectorModel.Surroundings.one_dim.OneDim.set_sensor or similar functions of more dimensional Surrounding-objects.
        @param intensities Intensities stored in a Surrounding-object (see MotionDetectorModel.Surroundings.one_dim.OneDim.intensities).
        """
        
        if self.debug.count('Sensor.update'):
            print('----------------------------------------------------------------')
            print('enter function Sensor._update_two_dim')

        self.value=self._compute_input_two_dim(intensities)

        if self.normalize:
            self.value=self.value/self.normalization_factor
        if self.debug.count('Sensor.update'):
            print('\tvalue:')
            print('\t\t'+str(self.value))
            print('----------------------------------------------------------------')
        
        
        
        
    def set_dt(self,dummy):
        pass
        
