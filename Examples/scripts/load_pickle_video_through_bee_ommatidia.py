import CompoundPye as CP

import sys
import os
import numpy as np

HERE=os.path.dirname(os.path.abspath(__file__))
DATA_PATH_PREFIX = "/home/ilyas/Data/CompoundPye/360video/apis/0s_to_0.1s/"

DT = 0.0005
RELAX_TIME = 0.0
RELAX_INTENSITY = 0.5

T_END = 0.001

#######################################################
# > Create surroundings with video                    #
#######################################################
sys.stdout.write("Creating surroundings ...\n")


surr = CP.Surroundings.video.VideoSurroundings("/home/ilyas/UNI/CompoundPye/Videos/market_360_degree_gray.avi")

#######################################################
# > Load list of components and sensors             #
#######################################################
sys.stdout.write("loading circ_lists ...\n")

import pickle

with open('/home/ilyas/UNI/CompoundPye/tmp/bee_circ_lists_border_left_eye.pkl', 'rb') as f:
    circ_lists = pickle.load(f)

#######################################################
# > Create Circuit from components and sensors        #
#######################################################
sys.stdout.write("Creating circuit ...\n")


circ = CP.Circuits.circuit.Circuit(*circ_lists[:2])

#######################################################
# > Create System                                     #
#######################################################
sys.stdout.write("Creating system ...\n")

S = CP.system.System(circ, surr, DT, RELAX_TIME, RELAX_INTENSITY)

#######################################################
# > set of which components to save output            #
#######################################################

sys.stdout.write("Creating list of neuron indices ...\n")

neuron_save_labels = ["T4", "T5"]

neuron_save_indices = []

for i in range(len(S.circuit.components)):
    c = S.circuit.components[i]
    if neuron_save_labels.count(c.label):
        neuron_save_indices.append(i)

#######################################################
# > set of which sensors to save output               #
#######################################################
sys.stdout.write("Creating list of sensor indices ...\n")

n_sensors_save = 3
sensor_save_indices = np.random.choice(len(S.circuit.sensors), n_sensors_save)

#######################################################
# > run simulation                                    #
#######################################################

t = np.arange(0,T_END, DT) # array of time stamps

#######################################################
# >> prepare arrays to store the outputs              #
#######################################################
sys.stdout.write("Preparing data output arrays ...\n")

components_output_array = np.zeros((t.shape[0], len(neuron_save_indices)))
sensors_output_array = np.zeros((t.shape[0], n_sensors_save))

i = 0

from tqdm import tqdm

sys.stdout.write("Starting simulation ...\n")

for i in tqdm(list(range(t.shape[0]))):
    t_i = t[i]

    new_comp_values=np.zeros(len(neuron_save_indices))

    for j in range(len(neuron_save_indices)):
        new_comp_values[j]=S.circuit.components[neuron_save_indices[j]].get_output()

    new_sens_values=np.zeros(len(sensor_save_indices))
    for k in range(len(sensor_save_indices)):
        new_sens_values[k]=S.circuit.sensors[sensor_save_indices[k]].get_value()

    components_output_array[i,:]=new_comp_values
    sensors_output_array[i,:]=new_sens_values

    S.update()



#######################################################
# > save data arrays                                  #
#######################################################

sys.stdout.write("Saving arrays ...\n")

np.save(DATA_PATH_PREFIX + "components.npy", components_output_array)
np.save(DATA_PATH_PREFIX + "sensors.npy", sensors_output_array)
np.save(DATA_PATH_PREFIX + "t.npy", t)


del components_output_array
del sensors_output_array
del t

#######################################################
# > after simulation, save column positions of output #
#   neurons and sensors,                              #
#   and directions of correlators                     #
#######################################################

sys.stdout.write("Saving labels and positions ...\n")

# >> neurons

component_positions = np.zeros((len(neuron_save_indices), 2))
directions = []
labels = []

for i in range(len(neuron_save_indices)):
    c = S.circuit.components[neuron_save_indices[i]]
    component_positions[i,:] = c.graph_pos
    directions.append(c.direction)
    labels.append(c.label)

np.save(DATA_PATH_PREFIX + "component_positions.npy", component_positions)
np.save(DATA_PATH_PREFIX + "component_directions.npy", np.array(directions))
np.save(DATA_PATH_PREFIX + "component_labels.npy", np.array(labels))

# >> sensors

sensor_positions = np.zeros((n_sensors_save, 2))

for i in range(n_sensors_save):
    pos = S.circuit.sensors[sensor_save_indices[i]].receptive_field
    pos = pos / np.array(S.surroundings.n_pixel)
    sensor_positions[i,:] = pos

np.save(DATA_PATH_PREFIX + "sensor_positions.npy", sensor_positions)


sys.stdout.write("Done.\n")
