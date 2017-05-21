## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.15

# last update: 15.10.15

"""
@package CompoundPye.src.Graph.sensors
Provides functions to determine neighbourhood of ommatidia. Mainly uses 
tools from networkx to do so.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# should return neighbours,distances,angles
def determine_neighbours(coords, neighbours_per_direction=1, neighbour_range=0.1,
                         bi_directional=False,
                         directions_dict={'HP': ([-np.pi * 5. / 36, np.pi * 5. / 36],),
                                          'HN': ([31. / 36 * np.pi, np.pi], 
                                                 [-np.pi, -31. / 36 * np.pi]),
                                          'VP': ([np.pi * 13. / 36., 23. / 36 * np.pi],),
                                          'VN': ([-23. / 36 * np.pi, -np.pi * 13. / 36.],)}):
    """
    Determines edges depending on node coordinates. The direction dict needs 
    to provide names of directions 
    as keys and angle ranges as values (see the default parameter). 
    On default, there are four directions:
        HP = horizontal positive, i.e. to the right,
        HN = horizontal negative, i.e. to the left,
        VP = vertical positive, i.e. upwards,
        VN = vertical negative, i.e. downwards.
    @param coords Array of coordinates.
    @param neighbours_per_direction Maximum number of neighbours per direction 
    (for each ommatidium).
    @param neighbour_range Maximum range between neighbours.
    @param bi_directional NOT IMPLEMENTED YET.
    @param directions_dict Dictionary containing direction labels as 
    keys and angle ranges as values.
    @return tuple of three values: (1) List containing neighbours for each ommatidium, 
    (2) distance matrix, (3) angle matrix.
    """
    
    # distances (phi=angle on x-y-plane, theta=angle to z-axis, as in spherical coordinates)
    d = np.zeros((coords.shape[0], coords.shape[0]))
    d_phi = np.zeros((coords.shape[0], coords.shape[0]))
    d_theta = np.zeros((coords.shape[0], coords.shape[0]))
    
    for i in range(coords.shape[0]):
        d_phi[:, i] = coords[:, 0] - coords[i, 0]
        d_theta[:, i] = coords[:, 1] - coords[i, 1]
        d[:, i] = np.sqrt(d_phi[:, i] ** 2 + d_theta[:, i] ** 2)

    d[(np.arange(d.shape[0]), np.arange(d.shape[0]))] = np.inf

    # angles (of vectors from one node to the other on phi-theta-2D-plane)
    angles = np.arctan(d_theta / d_phi)
    negative = np.where(d_phi < 0)
    s = np.sign(d_theta[negative])
    s[np.where(s == 0)] = 1
    angles[negative] = s * np.pi + angles[negative]
    
    if bi_directional:
        neighbours = _determine_neighbours_bi(angles, d, neighbours_per_direction,
                                              neighbour_range, directions_dict)
    else:
        neighbours = _determine_neighbours_single(angles, d, neighbours_per_direction,
                                                  neighbour_range, directions_dict)
        
    return neighbours, d, angles


def plot_neighbourhood(ax, G, direction_colors={}, node_color='white',
                       alpha=0.8, labels=True, node_size=300, font_size=12):
    """
    Plots the Graph using networkx' draw method.
    Each edge should have an direction assigned to it; with the direction_colors 
    parameter you can assign different directions different colors for plotting.
    @param ax Axis-object.
    @param G Graph-object.
    @param direction_colors Dictionary with directions as keys and colors as values.
    """
    pos_dict = {}
    for i in G.node:
        pos_dict[i] = np.array([G.node[i]['phi'], G.node[i]['theta']])

    edge_colors = 'black'

    if len(list(direction_colors.keys())) > 0:
        edge_colors = []
        for edge_origin in list(G.edge.keys()):
            for edge_target in list(G.edge[edge_origin].keys()):
                if list(direction_colors.keys()).count(G.edge[edge_origin][edge_target]['direction']):
                    edge_colors.append(direction_colors[G.edge[
                        edge_origin][edge_target]['direction']])
                else:
                    edge_target.append('black')
                                
    nx.draw(G, pos_dict, ax, with_labels=labels, edge_color=edge_colors, 
            node_color=node_color, alpha=alpha, node_size=node_size, font_size=font_size)    
    return G


def coords_to_graph(coords, index_offset=0):
    """
    Creates a Graph containing one node for each ommatidiuml (x,y)-coordinate.
    @param coords Array of ommatidial (x,y)-coordinates.
    @return Graph-object.
    """
    G = nx.DiGraph()
    for i in range(coords.shape[0]):
        G.add_node(i + index_offset, phi=coords[i, 0], theta=coords[i, 1], eye=None)
    return G


def neighbours_to_graph_edges(G, neighbours, index_offset=0):
    """
    Takes the lists of neighbours and adds appropriate edges to the graph.
    @param G Graph containing one node per ommatidium and their coordinates as values.
    @param neighbours Lists of neighbours for each node/ommatidium.
    """
    for i in range(len(neighbours)):

        for key in neighbours[i]:
            for j in range(len(neighbours[i][key])):
                if not G.has_edge(i + index_offset, neighbours[i][key][j] + index_offset):
                    G.add_edge(i + index_offset, neighbours[i][key][j] 
                               + index_offset, direction=key)


# should return only neighbours
def _determine_neighbours_single(angles, distances, neighbours_per_direction,
                                 neighbour_range, directions_dict):

    """
    Determines neighbours in a single directional fashion, i.e. ommatidium i can 
    consider j as a neighbour, even if j does not consider i as a neighbour.
    Args:
        angles: Angle matrix holding the angles between all ommatidia.
        distances: Distance matrix.
        neighbours_per_direction: Maximum number of neighbours per direction; 
        even if there are several candidates in range, only the closest 
        neighbours_per_direction will be chosen.
        neighbour_range: Maximum distance between neighbours.
        directions_dict: Dictionary with direction labels as keys, and angle ranges as values.


    Returns: 
        List containing one dictionary per ommatidium; each dictionary 
        contains directions as keys and a list of neighbours as values.
    """
    neighbours = []

    # to track the average distance between neighbours: (0) right (1) left (2) top (3) down
    avg_distances = np.zeros(4)
    count_added_distances = np.zeros(4)

    for i in range(0, distances.shape[0]):
        neighbours_i = {}
        for key in directions_dict:

            neighbours_i[key] = []
            candidates = np.array([])
            d = []
            for _range in directions_dict[key]:
                candidates = np.concatenate([candidates, 
                                             np.where((angles[:, i] >= _range[0]) 
                                                      & (angles[:, i] <= _range[1]))[0]])
                
                d = d + [(distances[i, j], j, angles[i, j]) for j in candidates]
            d.sort()

            for k in range(neighbours_per_direction):
                if len(d) > k:
                    if d[k][0] < neighbour_range:
                        neighbours_i[key].append(d[k][1])
                        if key == 'HP':
                            avg_distances[0] = avg_distances[0] + d[k][0] * np.cos(d[k][2])
                            count_added_distances[0] += 1
                        elif key == 'HN':
                            avg_distances[1] = avg_distances[1] + d[k][0] * np.cos(d[k][2])
                            count_added_distances[1] += 1
                        elif key == 'VP':
                            avg_distances[2] = avg_distances[2] + d[k][0] * np.sin(d[k][2])
                            count_added_distances[2] += 1
                        elif key == 'VN':
                            avg_distances[3] = avg_distances[3] + d[k][0] * np.sin(d[k][2])
                            count_added_distances[3] += 1                        
                else:
                    break
        neighbours.append(neighbours_i)

    avg_distances = avg_distances / count_added_distances
    print('=' * 30)
    s = ['right', 'left', 'up', 'down']
    for i in range(4):
        print(s[i])
        print("\tnumber of connections: " + str(count_added_distances[i]))
        print("\taverage distance: " + str(avg_distances[i]))

    return neighbours


# should return only neighbours
def _determine_neighbours_bi(angles, distances, neighbours_per_direction,
                             neighbour_range, directions_dict):
    print("!--!" * 10)
    print("WARNING: bi directional neighbour detection not implemented yet!") 
    print("Using single directional detection instead")
    print("!--!" * 10)
    return _determine_neighbours_single(angles, distances, neighbours_per_direction,
                                        neighbour_range, directions_dict)


if __name__ == "__main__":
    """
    Run this file for tests and examples of the functions provided here.
    """
    plt.ion()

    # coords = np.array(([0.5, 0.75], [0.25, 0.5], [0.5, 0.5], [0.75, 0.5], [0.5, 0.25]))
    coords = np.random.rand(30, 2)

    neighbours, distances, angles = determine_neighbours(coords, 1, 0.25)
    
    G = coords_to_graph(coords, 10)
    neighbours_to_graph_edges(G, neighbours, 10)

    f, ax = plt.subplots(1, 1)
    
    # G = plot_neighbourhood(ax, coords, neighbours)

    plot_neighbourhood(ax, G, {'HP': 'r',
                               'HN': 'blue',
                               'VP': 'g',
                               'VN': 'purple'})
    f.show()
