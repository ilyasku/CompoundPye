"""
Contains a functions that starts a small simulation using two photoreceptors
and the normal set of neuron types.
"""

import numpy as np
import os

from CompoundPye import Parser
from CompoundPye.Circuits import circuit

here = os.path.dirname(os.path.abspath(__file__))

default_sensor_file = here + '/../sensor_files/two_photoreceptors_HRC_pixel.txt'
default_circuit_file = here + '/../circ_files/Tm1_Tm2_as_HPF_larger_time_const_HS.txt'


def get_response(dt, intensities_array, relaxation_time, neuron_types_to_be_recorded,
                 sensor_file=default_sensor_file, circuit_file=default_circuit_file):
    """
    For given input intensities, this function computes my model's response for all components.
    Output is only stored for those neurons appearing in neuron_types_to_be_recorded (list of neuron 
    labels as strings). This function is designed for circuits with a single sensor. 
    (So best keep single_photor.txt as sensor_file.)
    @param dt time step
    @param intensities_array Array of input intensities, used as direct input 
    value to the photoreceptor.
    @param relaxation_time Relaxation time.
    @param neuron_types_to_be_recorded List of neuron labels for which the output at each time 
    step will be returned (in the returned data_array).
    """

    sensor_file_parsed = Parser.sp.parse_file(sensor_file)
    circuit_file_parsed = Parser.cp.parse_file(circuit_file)

    kwargs = {'show_nhood_plot': False}

    circuit_object = circuit.Circuit(
        *Parser.creator.create_circ_lists(2, *(sensor_file_parsed + circuit_file_parsed),
                                          **kwargs)[: 2])

    photoreceptor_0 = circuit_object.sensors[0]
    photoreceptor_1 = circuit_object.sensors[1]
    photoreceptor_0.set_dt(dt)
    photoreceptor_1.set_dt(dt)

    photoreceptor_0.set_receptive_field(2, 0.49, 'pixel')
    photoreceptor_1.set_receptive_field(2, 0.51, 'pixel')

    store_output_indices = []
    _dtype = []
    for i in range(0, len(circuit_object.sensors)):
        _dtype.append(('s' + str(i), np.float64))

    for i in range(0, len(circuit_object.components)):
        neuron = circuit_object.components[i]
        if neuron_types_to_be_recorded.count(neuron.label):
            store_output_indices.append(i)
            _dtype.append((neuron.group_label + neuron.label, np.float64))        
    
    t = np.arange(0, intensities_array.shape[0]) * dt
    
    data_array = np.zeros(t.shape[0], dtype=_dtype)

    current_intensities = np.array([intensities_array[0, :]]).transpose()
    for j in range(0, int(7. / 10 * relaxation_time / dt)):
        photoreceptor_0.update(current_intensities)
        photoreceptor_1.update(current_intensities)
        
    for k in range(j, int(relaxation_time / dt)):
        circuit_object.update(dt, current_intensities)

    for i in range(0, t.shape[0]):
        current_intensities = np.array([intensities_array[i, :]]).transpose()
        circuit_object.update(dt, current_intensities)

        data_vector = []
        for s in circuit_object.sensors:
            data_vector.append(s.get_value())
        for j in store_output_indices:
            data_vector.append(circuit_object.components[j].get_output())
            
        data_vector = np.array(data_vector)
        data_array[i] = tuple(data_vector)

    return t, data_array, circuit_object
