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
        
        outputs=np.empty(self.n_comp)
        for i in range(0,self.n_comp):
            outputs[i]=self.components[i].get_output()
                
        #if n_processes==1:
        sensor_values=np.empty(len(self.sensors))
        
        
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


    def get_sensor_values(self):
        out=[]
        for i in range(len(self.sensors)):
            out.append(self.sensors[i].get_value())
        return np.array(out)

    def get_component_outputs(self):
        out=[]
        for i in range(len(self.components)):
            out.append(self.components[i].get_output())
        return np.array(out)


class CircuitArray(Circuit):
    """
Circuit class that replaces some calculations with array operations,
in order to boost speed of simulations.
The normal Circuit object uses for loops to update sensors' and 
components' inputs. This class aims to replace those update steps 
by numpy array operations.
Current limitations:
* Works only with sensors of class `Photoreceptor`.
* Works only for 2-dimensional surroundings.
* Sensors/Photoreceptors need to have receptive fields 
  specified on initialization of a CircuitArray object.
    """
    
    def __init__(self,list_of_components,list_of_sensors,debug=False,mode='photoreceptor'):
        
        Circuit.__init__(self,list_of_components,list_of_sensors,debug)

        self.mode=mode


        # --------------- create arrays containing sensor properties ------------------
        self.sensor_time_consts=np.empty(len(list_of_sensors))
        self.photoreceptor_time_consts_lp3=np.empty(len(list_of_sensors))

        #self.sensor_receptive_field_coords=np.empty((len(list_of_sensors),2))
        

        self.sensor_inputs_array=np.empty(len(list_of_sensors))
        self.sensor_values_array=np.empty(len(list_of_sensors))
        self.current_DWM_values=np.empty((len(list_of_sensors),6))
        for i in range(len(self.sensors)):
            self.sensor_values_array[i]=self.sensors[i].get_value()
            self.current_DWM_values[i,:3]=self.sensors[i].current_DWM_values[0]
            self.current_DWM_values[i,3:]=self.sensors[i].current_DWM_values[1:]
            
            self.sensor_time_consts[i]=self.sensors[i].time_const
            self.photoreceptor_time_consts_lp3[i]=self.sensors[i].time_const_lp3

            #self.sensor_receptive_field_coords[i,:]=self.sensors[i].receptive_field
        # -----------------------------------------------------------------------------

        # -------------- create arrays containing component properties ----------------
        self.component_outputs_array=np.empty(len(list_of_components))
        self.component_inputs_array=np.empty(len(list_of_components))
        self.component_values_array=np.empty(len(list_of_components))
        for i in range(len(self.components)):
            self.component_outputs_array[i]=self.components[i].get_output()
            self.component_values_array[i]=self.components[i].value
        # -----------------------------------------------------------------------------

    def update(self,dt,intensities):
        """
        """

        # update sensors ... the old way
        for i in range(len(self.sensors)):
            self.sensor_inputs_array[i]=self.sensors[i]._compute_input_two_dim(intensities)
        
        self.M_DWM_for_arrays(dt,self.photoreceptor_time_consts_lp3)
        
        self.component_inputs_array=self.sensors_weight_matrix.dot(self.sensor_values_array)+self.components_weight_matrix.dot(self.component_outputs_array)

        self.component_outputs_array=self.update_components(dt)


    def M_DWM_for_arrays(self,dt,time_const_lp3,time_const_lp1=0.00169,time_const_lp2=0.0718,k1=0.689,k2=9.07):
        
        lp1_0=low_pass(self.sensor_inputs_array,self.current_DWM_values[:,0],time_const_lp1,dt)
        lp1_1=low_pass(lp1_0,self.current_DWM_values[:,1],time_const_lp1,dt)
        lp1=low_pass(lp1_1,self.current_DWM_values[:,2],time_const_lp1,dt)

        div1=lp1/self.current_DWM_values[:,3]

        lp2=low_pass(lp1,div1,time_const_lp2,dt)

        div2=div1/self.current_DWM_values[:,5]

        lp3=low_pass(div2,self.current_DWM_values[:,4],time_const_lp3,dt)
        nonlin=k1*np.exp(k2*lp3)

        nonlin1=div2/(1+div2)

        self.sensor_values_array[:]=nonlin1
        self.current_DWM_values[:,0]=lp1_0
        self.current_DWM_values[:,1]=lp1_1
        self.current_DWM_values[:,2]=lp1
        self.current_DWM_values[:,3]=lp2
        self.current_DWM_values[:,4]=lp3
        self.current_DWM_values[:,5]=nonlin

    def get_sensor_values(self):
        return self.sensor_values_array

    def get_component_outputs(self):
        return self.component_outputs_array

def low_pass(x,current_value,time_const,dt):
    alpha=dt/(time_const+dt)
    return current_value*(1-alpha)+alpha*x
        
