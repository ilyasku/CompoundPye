"""
Contains a functions that starts a small simulation using two photoreceptors
and the normal set of neuron types.
"""


#import MotionDetectorModel.Parser as Parser
from CompoundPye.src import Parser
from CompoundPye.src.Circuits import circuit
import numpy as np

import os
here=os.path.dirname(os.path.abspath(__file__))

default_s_file=here+'/../sensor_files/two_photoreceptors_HRC_pixel.txt'
#c_file=here+'../circ_files/L4_network_for_thesis.txt'
default_c_file=here+'/../circ_files/L4_network_with_GC1_larger_time_const_HS.txt'

def get_response(dt,intensities_array,t_relax,store_output,s_file=default_s_file,c_file=default_c_file):
    """
    For given input intensities, this function computes my model's response for all components.
    Output is only stored for those neurons appearing in store_output (list of neuron labels as strings).
    This function is designed for circuits with a single sensor. (So best keep single_photor.txt as s_file.)
    @param dt time step
    @param intensities_array Array of input intensities, used as direct input value to the photoreceptor.
    @param t_relax Relaxation time.
    @param store_output List of neuron labels for which the output at each time step will be returned (in the returned data_array).
    """


    s_parsed=Parser.sp.parse_file(s_file)
    c_parsed=Parser.cp.parse_file(c_file)

    kwargs={'show_nhood_plot':False}

    circ=circuit.Circuit(*Parser.creator.create_circ_lists(2,*(s_parsed+c_parsed),**kwargs)[:2])

    photo0=circ.sensors[0]
    photo1=circ.sensors[1]
    photo0.set_dt(dt)
    photo1.set_dt(dt)

    #photo0.debug=['Sensor.update']

    photo0.set_receptive_field(2,0.49,'pixel')
    photo1.set_receptive_field(2,0.51,'pixel')

    store_output_indices=[]
    _dtype=[]
    for i in range(0,len(circ.sensors)):
        _dtype.append(('s'+str(i),np.float32))

    print "="*30
    print "#\tlabel\toutput index"
    print '='*30
    for i in range(0,len(circ.components)):
        c=circ.components[i]
        if store_output.count(c.label):
            array_column=len(store_output_indices)+len(circ.sensors)
            store_output_indices.append(i)
            _dtype.append((c.group_label+c.label,np.float32))
        else:
            array_column=None
        print str(i)+"\t"+c.label+'\t'+str(array_column)
        print '-'*30
    

    t=np.arange(0,intensities_array.shape[0])*dt

    #relax_array=np.zeros(int(t_relax/dt))
    
    #data_array=np.zeros((t.shape[0],len(circ.sensors)+len(store_output_indices)))
    data_array=np.zeros(t.shape[0],dtype=_dtype)

    current=np.array([intensities_array[0,:]]).transpose()
    for j in range(0,int(7./10*t_relax/dt)):
        photo0.update(current)
        photo1.update(current)
        #relax_array[j]=photo0.get_value()
    for k in range(j,int(t_relax/dt)):
        circ.update(dt,current)
        #relax_array[k]=photo0.get_value()

    for i in range(0,t.shape[0]):
        current=np.array([intensities_array[i,:]]).transpose()
        circ.update(dt,current)

        data_vector=[]
        for s in circ.sensors:
            data_vector.append(s.get_value())
        for j in store_output_indices:
            data_vector.append(circ.components[j].get_output())
            
        data_vector=np.array(data_vector)
        data_array[i]=tuple(data_vector)

    return t,data_array,circ#,relax_array
            
