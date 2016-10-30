import CompoundPye as CP
from CompoundPye.src.Parser import sc, creator, sp, cp


import sys, os

HERE=os.path.dirname(os.path.abspath(__file__))

circuit_file = HERE + "/../circ_files/Tm1_Tm2_as_HPF_larger_time_const_HS.txt"

arrangement,variables,components,connections,receiver=cp.parse_file(circuit_file)


borders = [0.0,0.0,0.0,0.0]

bee_sensor_file_string = CP.OmmatidialMap.read_ommatidia.write_sphere_coords_spheric_to_sensor_file_buffer(borders = borders, animal = 'bee')

sensor_file = '.tmp_sensors_bee.txt'

tmp_file = open(sensor_file, 'wt')
tmp_file.write(bee_sensor_file_string)
tmp_file.close()

sensor_settings, sensor_variables, sensor_defaults, sensors = sp.parse_file(sensor_file)

os.remove(sensor_file)

## todo: px needs to be pixels of surroundings ... still need to read that from video?
circ_lists = creator.create_circ_lists(px, sensor_settings, sensor_variables, sensor_defaults, sensors,
                                       arrangement, variables, components, connections, receiver,
                                       neighbour_kw_params = {'manually': False, 'range': 0.0255, 'max_n': 1},
                                       show_nhood_plot = True)

S = CP.system.System()
