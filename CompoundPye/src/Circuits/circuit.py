## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 08.10.14

"""
@package CompoundPye.src.Circuits.circuit
Holds the basic Circuit class.
"""

import numpy as np
from scipy.sparse import csr_matrix,lil_matrix


class Circuit:
    """
    Basic Circuit class that handles a network of components and sensors and their updating at each time step.
    """   
     
    def __init__(self,list_of_components,list_of_sensors,debug=False):
        """
        Initializes a Circuit-object.
        Creates the weight matrices that represent the connections between components (and sensors).
        @param list_of_components Requires a list of components with predefined connections.
        @param list_of_sensors Requires a list of sensors with predefined connections to one or more component.
        """
        
        self.components=list_of_components
        self.components_weight_matrix=None
        self.sensors=list_of_sensors
        self.sensors_weight_matrix=None
        
        
        self.debug=debug
        
        self.create_weight_matrices()
        
        
    def create_weight_matrices(self):
        """
        Creates the weight matrices.
        Creates the components_weight_matrix from connections between components.
        Creates the sensors_weight_matrix from conncections from sensors to components.
        """
        
        self.n_comp=len(self.components)

        #create components_weight_matrix ...
        
        for i in range(0,self.n_comp):
            self.components[i].index_in_circuit_list=i

        components_weight_matrix=np.zeros((self.n_comp,self.n_comp))
        
        for i in range(0,self.n_comp):
            for j in range(0,len(self.components[i].connections)):
                components_weight_matrix[self.components[i].connections[j].target.index_in_circuit_list][i]=self.components[i].connections[j].weight
                
        #create sensors_weight_matrix ...
        n_sens=len(self.sensors)
        
        for i in range(0,n_sens):
            self.sensors[i].index_in_circuit_list=i
            
        sensors_weight_matrix=np.zeros((self.n_comp,n_sens))
            
        for i in range(0,n_sens):
            for j in range(0,len(self.sensors[i].connections)):
                sensors_weight_matrix[self.sensors[i].connections[j].target.index_in_circuit_list][i]=self.sensors[i].connections[j].weight
                
        if self.debug:
            print '-------debugging output-----------------'
            print '-------function: Circuit.create_weight_matrices()-------'
            print 'components_weight_matrix:'
            print components_weight_matrix
            print 'sensors_weight_matrix:'
            print sensors_weight_matrix
            print '----------------------------------------'
            
        self.components_weight_matrix=csr_matrix(components_weight_matrix)
        self.sensors_weight_matrix=csr_matrix(sensors_weight_matrix)


    
    def update(self,dt,intensities):
        """
        Updates the circuit's components (in self.components) and its sensors (in self.sensors).
        @param dt Time step for the update.
        @param intensities Intensities of stimuli (provides input for the detectors).
        """
        
        outputs=np.zeros(self.n_comp)
        for i in range(0,self.n_comp):
            outputs[i]=self.components[i].get_output()
                
        #if n_processes==1:
        sensor_values=np.zeros(len(self.sensors))
        
        
        for i in range(0,len(self.sensors)):
            self.sensors[i].update(intensities)
            sensor_values[i]=self.sensors[i].get_value()
        '''
        else:
            pool=mp.Pool(n_processes)
            l=[pool.apply(_mp_update_single,args=(self,i, intensities)) for i in range(0,len(self.sensors))]
            sensor_values=np.array(l)
        ''' 
        inputs=self.sensors_weight_matrix.dot(sensor_values)+self.components_weight_matrix.dot(outputs)
        
        
        
        for i in range(0,self.n_comp):
            self.components[i].update(inputs[i],dt)
        
        if self.debug:
            print '-------debugging output-----------------'
            print '-------function: Circuit.update()-------'
            print 'sensor_values:'
            print sensor_values
            print 'outputs:'
            print outputs
            print 'inputs:'
            print inputs
            print '--------------------------------------'
'''            
def _mp_update_single(obj,i,intensities):
    obj.sensors[i].update(intensities)
    return obj.sensors[i].get_value()
'''
