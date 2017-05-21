

import cv2
import numpy as np

DATA_LOCATION_PREFIX = "/media/windows/ilyas/data/360video/apis/0s_to_5s/"
DATA_LOCATION_PREFIX = "/home/ilyas/Data/CompoundPye/360video/apis/0s_to_1s/"

component_positions = np.load(DATA_LOCATION_PREFIX+"component_positions.npy")
component_directions = np.load(DATA_LOCATION_PREFIX+ "component_directions.npy")
component_labels = np.load(DATA_LOCATION_PREFIX + "component_labels.npy")


#######################################################
# > determine positions of columns                    #
#######################################################

unique_positions = []

# >> get unique phi coordinates
phi_pos = np.unique(component_positions[:,0])

theta_pos = []

for i in range(phi_pos.shape[0]):
    # >> for each phi coordinate, get all possible theta coordinates
    theta_pos_i = np.unique(component_positions[component_positions[:,0] == phi_pos[i],1])

    # >> fill list theta_pos such that it has as many elements as the phi_pos array
    theta_pos.append(theta_pos_i)

#######################################################
# > for each column, create one node                  #
#######################################################

# >> list of nodes
nodes = []

nodes_thrown_away = 0

for i in range(phi_pos.shape[0]):
    phi = phi_pos[i]

    for theta in theta_pos[i]:
        node = [(phi, theta),
                [], # one list to store indices and direction of T4 contributions to this node
                []] # one to store the same for T5 contributions

        neurons_at_this_node = np.where((component_positions[:,0] == phi) & (component_positions[:,1] == theta))[0]

        receives_neutral_input = np.zeros((2,2)) ## keep track whether this node receives input from
                                                 # T4s/T5s of all 4 cardinal directions
        
        for j in neurons_at_this_node:
            if component_directions[j] == "HP":
                direction = np.array([1.0,0.0])
            elif component_directions[j] == "HN":
                direction = np.array([-1.0,0.0])
            elif component_directions[j] == "VP":
                direction = np.array([0.0,1.0])
            elif component_directions[j] == "VN":
                direction = np.array([0.0,-1.0])
            else:
                sys.stderr.write("ERROR: neuron %i has no or wrong direction: %s \n" % (j, component_directions[j]))

            if component_labels[j] == "T4":
                node[1].append((j, direction))
                receives_neutral_input[0,:] += direction
            elif component_labels[j] == "T5":
                node[2].append((j,direction))
                receives_neutral_input[1,:] += direction
            else:
                sys.stderr.write("ERROR: neuron %i is neither 'T4' nor 'T5'. It is: %s\n"  % (j, component_labels[j]))


        if receives_neutral_input.any():
            nodes_thrown_away += 1
        else:
            nodes.append(node)

print(("Nodes thrown away: ", nodes_thrown_away))
            
node_positions = np.array([item[0] for item in nodes])



# >> function to compute arrows for nodes

def compute_arrows(current_neuron_outputs, ## current readings from T4 and T5 cells
                                           ## ... might be a good idea to window filter raw output,
                                           ## don't need such a high temporal resolution.
                   nodes): ## information to which node the readings need to be added
    node_arrows = np.zeros((len(nodes), 2))

    for i in range(len(nodes)):
        n = nodes[i]        
        for T4 in n[1]: ## T4 should be a tuple of two items:
                        # (1) index of this cell in the output_array
                        # (2) a unit vector representing its direction
            node_arrows[i,:] += current_neuron_outputs[T4[0]] * T4[1] 
            
        for T5 in n[2]:
            pass # for now ... test only T4 first

    return node_arrows

def direction_to_color(node_arrows):
    
    C = np.zeros((node_arrows.shape[0],3))

    angles = np.arctan2(node_arrows[:,0], node_arrows[:,1])

    C[:,0] = np.cos(angles)
    C[:,1] = np.sin(angles)

    C = C * 255.0

    return C


#######################################################
# >> window-filter output to roughly match the frames #
#   per second of the video                           #
#######################################################


## throw away at least the first
# 100 crappy values ...
START_INDEX = 100

components_output = np.load(DATA_LOCATION_PREFIX + "components.npy")[START_INDEX:,:]

t = np.load(DATA_LOCATION_PREFIX + "t.npy")[START_INDEX:]


cap = cv2.VideoCapture("/home/ilyas/UNI/CompoundPye/Videos/market_360_degree_gray.avi")

FPS = cap.get(cv2.CAP_PROP_FPS)
DT = t[1]-t[0]
T_END = t[-1]

#DT_PER_FRAMES = 1./FPS/DT

t_frames = np.arange(t[0], T_END, 1./FPS)
DT_frames = 1./FPS

filtered_output = np.zeros((t_frames.shape[0]-1, components_output.shape[1]))

for i in range(t_frames.shape[0] - 1):
    t_begin = t_frames[i]
    t_end = t_frames[i+1]

    data_indices = np.where((t >= t_begin) & (t < t_end))[0]

    filtered_output[i] = components_output[data_indices,:].mean(axis = 0)

    

#######################################################
# > create animation                                  #
#######################################################


import matplotlib
matplotlib.use('Agg')


import matplotlib.pyplot as plt


f,ax = plt.subplots(1,2, sharey = True)
ax[0].set_xlim(0.0,1.0)


## for now only static for testing, no animations ...

node_arrows = compute_arrows(components_output[0,:], nodes)

Q = ax[0].quiver(node_positions[:,0], node_positions[:,1], node_arrows[:,0]/node_arrows[:,0].max()*0.1, node_arrows[:,1]/node_arrows[:,1].max()*0.1, units = "xy", pivot = "mid", scale = 0.95)


I = ax[1].imshow(np.random.rand(960,1920), cmap = "gray", extent = (0.0,1.0,0.0,1.0))

ret, frame = cap.read()

#I.set_data(frame)

def update_plot(num, Q, I, components_output):

    global frame
    
    t_num = t_frames[num]
    
    print(num)
    
    node_arrows = compute_arrows(components_output[num,:], nodes)
    C = direction_to_color(node_arrows)
    Q.set_UVC(node_arrows[:,0]/node_arrows[:,0].max()*0.1,
              node_arrows[:,1]/node_arrows[:,1].max()*0.1)
              #C) ## color, not figured out yet

    while cap.get(cv2.CAP_PROP_POS_MSEC) < t_num*1000:
        ret, frame = cap.read()

    I.set_data(frame)

    return Q, I




from matplotlib import animation

anim = animation.FuncAnimation(f, update_plot, frames = 41, fargs = (Q, I, filtered_output), interval = 10)#, blit = False)

#x = np.linspace(0, 2*np.pi, 200)
#init_animation()

#anim = animation.FuncAnimation(f, animate, init_func = init_animation,frames = 50, fargs = (), interval = 10)#, blit = False)    


#f.show()

#anim.save("~/UNI/CompoundPye/tmp/animation.mp4", writer = mywriter)
anim.save("/home/ilyas/UNI/CompoundPye/tmp/animation.gif", writer = "imagemagick", fps = 10)

#f.show()
