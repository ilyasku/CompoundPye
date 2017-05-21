## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 08.10.14


"""
@package CompoundPye.src.Parser.creator

Provides functions that use input parsed with MotionDetector.Parser.sensor_parser and 
MotionDetector.Parser.circuit_parser or input specified in the GUI to create lists of 
connected sensors and components. The central function to use here is create_circ_lists.
"""

import sys

from .. import Graph

import numpy as np

from . import paths_to as pt


def get_comp_dict():
    """
    Creates a dictionary of possible CompoundPye.Components.component.Component 
    classes to use and where to find them (path to file).
    @return Dictionary with class names as keys and their source files as values.
    """    
    d = {}
    for _file in pt.paths_to_component_objects:
        f = open(pt.here + _file, 'r')
        py_lines = f.readlines()
        for i in range(len(py_lines)):
            row = py_lines[i]
            if row:
                if len(row) > 5:
                    if row[:5] == 'class':
                        name = row[5:].split('(')[0].split(':')[0].lstrip()
                        fpath = pt.here + _file
                        d[name] = fpath
                            
    return d


def get_transf_func_dict():
    """
    Creates a dictionary of possible transfer-functions to use and where to 
    find them (path to file).
    @return Dictionary with function names as keys and their source files as values.
    """    
    d = {}
    for _file in pt.paths_to_transfer_functions:
        f = open(pt.here + _file, 'r')
        py_lines = f.readlines()
        for row in py_lines:
            if row:
                if len(row) > 3:
                    if row[:3] == 'def':
                        name = row[3:].split('(')[0].lstrip()
                        fpath = pt.here + _file
                        d[name] = fpath
    return d


def get_sensor_dict():
    """
    Creates a dictionary of possible MotionDetectorModel.Sensors.sensor.Sensor
    classes to use and where to find them (path to file).
    @return Dictionary with class names as keys and their source files as values.
    """
    d = {}
    for _file in pt.paths_to_sensor_objects:
        f = open(pt.here + _file, 'r')
        py_lines = f.readlines()
        for row in py_lines:
            if row:
                if len(row) > 5:
                    if row[:5] == 'class':
                        name = row[5:].split('(')[0].split(':')[0].lstrip()
                        fpath = pt.here + _file
                        d[name] = fpath
    return d


comp_dict = get_comp_dict()
transf_func_dict = get_transf_func_dict()
sensor_dict = get_sensor_dict()

# -------------------------------------------------------
# import .py-files of classes and functions in the dictionaries comp_dict,
# transf_func_dict and sensor_dict.
for _file in pt.paths_to_component_objects + pt.paths_to_transfer_functions + pt.paths_to_sensor_objects:
    dir, slash, fname = (pt. here + _file).rpartition('/')
    dir = dir + slash
    sys.path.append(dir)
    exec('from ' + fname[:-3] + ' import *')
# ---------------------------------------------------------


def create_circ_lists_GUI_interface(pixel, sensor_settings, sensor_variables, sensor_defaults,
                                    sensors, arrangement, variables,
                                    components, connections, receiver,
                                    neighbour_keyword_parameters, show_nhood_plot):
    """
    Create circuit lists (a list of components and a list of sensors) with information from the GUI.

    Changes some of the input arguments such that the function create_circ_lists can be called from
    within this function with information from the input arguments.
    corrected==in correct syntax for create_circ_lists()
    """
    corrected_sensors = {}
    for s in sensors:
        new_dict = s.copy()
        corrected_sensors[s['name']] = new_dict

    corrected_components = {'column_components': {}, 'between_next_neighbour_components': {},
                            'between_next_next_neighbour_components': {},
                            'tangential_components': {}}

    translations = {'column': 'column_components',
                    'between': 'between_next_neighbour_components',
                    'tangential': 'tangential_components'}
    for key in components:
        for c in components[key]:

            new_dict = c.values.copy()
            corrected_components[translations[key]][new_dict['name']] = new_dict

    corrected_connections = {'column_connections': connections['column'],
                             'next_neighbour_connections': connections['next_neighbour'],
                             'tangential_to_connections': connections['tangential_to'],
                             'tangential_from_connections': connections['tangential_from']}

    return create_circ_lists(pixel, sensor_settings, sensor_variables, sensor_defaults, 
                             corrected_sensors, arrangement, variables, corrected_components,
                             corrected_connections, receiver, neighbour_keyword_parameters,
                             show_nhood_plot)


def create_circ_lists(pixel, 
                      sensor_settings, sensor_variables, sensor_defaults, sensors, 
                      arrangement, variables, 
                      components, connections, receiver,
                      neighbour_keyword_parameters={'manually': False, 'range': 0.0255, 'max_n': 6},
                      show_nhood_plot=True):
    """
    Create circuit lists (a list of components and a list of sensors) with information
    from a circuit-file and a sensor-file.
    @param pixel
    @param sensor_settings
    @param sensor_variables
    @param sensor_defaults
    @param sensors
    @param arrangement
    @param variables
    @param components
    @param connections
    @param receiver
    @param neighbour_keyword_parameters
    @param show_nhood_plot
    @return Tuple of 2-4 items:
            (1) A <list> of all created component objects.
            (2) <list> of all created sensor objects.
            (3) <np.ndarray> conntaining normalized (phi, theta) coordinates for all sensors.
            (4) <np.ndarray> containing angles in radian between all sensors.
    """    
    neighbourhood_manually = neighbour_keyword_parameters['manually']
    
    if arrangement != 'column':
        msg = "In CompoundPye.Parser.creator.create_circ_lists: \n"
        msg += "`arrangement` was: \"" + arrangement + "\". Handling of this arrangement\n"
        msg += "is not implemented yet. (Only accepted keyword is \"column\" so far!)"
        raise NotImplementedError(msg)

    if neighbourhood_manually:        
        return _create_circ_lists_manually(pixel,
                                           sensor_settings, sensor_variables, 
                                           sensor_defaults, sensors,
                                           variables, 
                                           components, connections, receiver) 
    else:
        return _create_circ_lists_automatically(pixel,
                                                sensor_settings, sensor_variables,
                                                sensor_defaults, sensors,
                                                variables, components, connections, receiver,
                                                show_nhood_plot, neighbour_keyword_parameters)


def _create_circ_lists_manually(pixel, 
                                sensor_settings, sensor_variables, sensor_defaults, sensors,
                                variables, components, connections, receiver):

    components_list = []
    sensors_list = []

    sensor_array = create_sensors(pixel, sensor_settings, sensor_variables,
                                  sensor_defaults, sensors)
    col_components_pre = None
    for nhood in list(sensor_array.keys()):
        for i in range(0, len(sensor_array[nhood])):

            col_components = create_components(variables, components['column_components'],
                                               nhood + ',' + str(i), [0, 0])
            connect_receiver(sensor_array[nhood][i][1], col_components, receiver)
            connect_components(col_components, connections['column_connections'])
            if i > 0:
                nn_components = create_components(variables,
                                                  components['between_next_neighbour_components'],
                                                  'nn ' + nhood + ',' + str(i), [0, 0])
                nnn_components = create_components(variables,
                                                   components['between_next_next_neighbour_components'],
                                                   'nnn ' + nhood + ',' + str(i), [0, 0])
                cross_connect_next_neighbours(col_components_pre, nn_components,
                                              col_components,
                                              connections['next_neighbour_connections'],
                                              True, None)
                ## @todo implement connection of next next neighbours
                # cross_connect_next_next_neighbours()
                components_list = components_list + col_components + nn_components + nnn_components
            else:
                components_list = components_list + col_components
            col_components_pre = col_components
        sensors_list = sensors_list + [s[1] for s in sensor_array[nhood]]

    return components_list, sensors_list


def _create_circ_lists_automatically(pixel, 
                                     sensor_settings, sensor_variables, sensor_defaults, sensors,
                                     variables, components, connections, receiver, 
                                     show_nhood_plot, neighbour_keyword_parameters):
    components_list = []
    sensors_list = []

    ## get sensor objects and distances between sensors
    nhood_dict = create_sensors(pixel, sensor_settings, sensor_variables, sensor_defaults,
                                sensors, False)

    direction_dicts = {'left': {'HP': ([-np.pi * 5. / 36, np.pi * 5. / 36],),
                                'HN': ([31. / 36 * np.pi, np.pi],
                                       [-np.pi, -31. / 36 * np.pi]),
                                'VP': ([np.pi * 13. / 36., 23. / 36 * np.pi],),
                                'VN': ([-23. / 36 * np.pi, -np.pi * 13. / 36.],)},
                       'right': {'HN': ([-np.pi * 5. / 36, np.pi * 5. / 36],),
                                 'HP': ([31. / 36 * np.pi, np.pi],
                                        [-np.pi, -31. / 36 * np.pi]),
                                 'VP': ([np.pi * 13. / 36., 23. / 36 * np.pi],),
                                 'VN': ([-23. / 36 * np.pi, -np.pi * 13. / 36.],)}}

    node_color_dict = {'left': 'pink', 'right': 'lightblue'}

    if show_nhood_plot:
        import matplotlib.pyplot as plt
        f, ax = plt.subplots(1, 1)

    for nhood in list(nhood_dict.keys()):
        coords = nhood_dict[nhood][1]
        s_list = nhood_dict[nhood][0]

        c_list = []
        if nhood == 'left' or nhood == 'right':
            neighbours, distances, angles = Graph.sensors.determine_neighbours(coords,
                                                                               neighbour_keyword_parameters['max_n'],
                                                                               neighbour_keyword_parameters['range'],
                                                                               directions_dict=direction_dicts[nhood])
        else:
            neighbours, distances, angles = Graph.sensors.determine_neighbours(coords,
                                                                               neighbour_keyword_parameters['max_n'],
                                                                               neighbour_keyword_parameters['range'])

        G = Graph.sensors.coords_to_graph(coords, len(sensors_list))
        Graph.sensors.neighbours_to_graph_edges(G, neighbours, len(sensors_list))

        if show_nhood_plot:
            if nhood == 'right' or nhood == 'left':
                Graph.sensors.plot_neighbourhood(ax, G, {'HP': 'g',
                                                         'HN': 'r',
                                                         'VP': 'goldenrod',
                                                         'VN': 'blue'},
                                                 node_color_dict[nhood])
            else:
                Graph.sensors.plot_neighbourhood(ax, G, {'HP': 'g',
                                                         'HN': 'r',
                                                         'VP': 'goldenrod',
                                                         'VN': 'blue'})

        sensors_list = sensors_list + s_list

        ## list to hold lists of components for each column
        col_components_list = []
        ## create components for each column
        for i in range(0, len(s_list)):
            col_components = create_components(variables, components['column_components'],
                                               s_list[i].label, coords[i, :])
            connect_receiver(s_list[i], col_components, receiver)
            connect_components(col_components, connections['column_connections'])
            col_components_list.append(col_components)

        ## create components between next neighbours and connect them                
        for i in G:
            _i = i - list(G.node.keys())[0]                    
            c_list = c_list + col_components_list[_i]                    
            for j in G[i]:
                j = int(j)
                edge_i_j = G[i][j]

                _j = j - list(G.node.keys())[0]

                ## fixed labels for sensors!
                nn_j = create_components(variables,
                                         components['between_next_neighbour_components'],
                                         's' + str(i) + ' ' + 'nn' + str(j) + ' ' + nhood,
                                         np.array((G.node[i]['phi'], G.node[i]['theta'])))
                nnn_j = create_components(variables,
                                          components['between_next_next_neighbour_components'],
                                          's' + str(i) + ' ' + 'nnn' + str(j) + ' ' + nhood,
                                          np.array((G.node[i]['phi'], G.node[i]['theta'])))

                cross_connect_next_neighbours(col_components_list[_i],
                                              nn_j,
                                              col_components_list[_j],
                                              connections['next_neighbour_connections'],
                                              False,
                                              edge_i_j)
                ## @todo implement connection of next next neighbours
                # cross_connect_next_next_neighbours()                        
                c_list = c_list + nn_j + nnn_j               

        tangential_components = create_components(variables,
                                                  components['tangential_components'],
                                                  nhood + ' tangential',
                                                  nhood + ' tangential')
        connect_tangential_components(tangential_components,
                                      c_list,
                                      connections['tangential_to_connections'],
                                      connections['tangential_from_connections'])

        c_list = c_list + tangential_components

        components_list = components_list + c_list

    if show_nhood_plot:
        f.show()

    return components_list, sensors_list, coords, angles

def connect_tangential_components(tangential_components, non_tangential_components,
                                  connections_to, connections_from):
    """
    Connects tangential components, or rather connects components of all 
    columns to tangential cells.
    Now also includes connections FROM tangential cells to any other cells.
    @param tangential_components List of tangential components.
    @param non_tangential_components List of all other components.
    @param connections List of connections to tangential components.
    """
    for c in connections_to:
        if len(c) > 3:
            sources = get_components_via_label_and_attributes(non_tangential_components,
                                                              c[0], c[3])
        else:
            sources = get_components_via_label_and_attributes(non_tangential_components,
                                                              c[0], None)

        target = get_component_via_label(tangential_components, c[2])
            
        for comp in sources:
            comp.add_connection(float(c[1]) / len(sources), target)

    for c in connections_from:
        connect_tangential_via_labels(tangential_components + non_tangential_components, *c)

        
def get_components_via_label_and_attributes(components, name, parameters):
    """
    Get all components with given name and fulfilling given parmeter
    specifications from a list of components.
    @param components List of components among which to search.
    @param name Label of the wanted components.
    @param parameters Specifies parameters regarding axis and direction for the wanted neurons.
    """
    l = []
    if parameters == None:
        for comp in components:
            if comp.label == name:
                l.append(comp)
        return l
    else:
        p = 1.0
        axis = None
        direction = None
        for param in parameters.split(','):
            split = param.split('=')
            s = split[0] + '=' + '"' + split[1] + '"'
            exec(s)

        for comp in components:
            if comp.label == name:                
                axis_ok = False
                direction_ok = False
                if axis is not None:
                    if comp.attributes['axis'] == axis:
                        axis_ok = True
                else:
                    axis_ok = True
                if direction is not None:
                    if comp.attributes['direction'] == direction:
                        direction_ok = True
                else:
                    direction_ok = True
                        
                if axis_ok and direction_ok:
                    l.append(comp)
        return l

    
def create_sensors(pixel, sensor_settings, sensor_variables, sensor_defaults, sensors, mode_manual):
    """
    Create a list of sensors with information from a sensor-file.
    """    
    ## if the user specified neighbours manually,
    # they will be grouped together in one list, and 
    # all list returned in a dictionary
    if mode_manual:
        if not list(sensor_settings.keys()).count('dimension'):
            if sensor_settings['neighbours'] == 'x':
                rows = {}
                count = 0
                for s in list(sensors.keys()):
                    count += 1
                    s_class = get_sensor_class(sensors[s]['sensor'], sensor_defaults)
                    obj_args, obj_kwargs = get_sensor_args(sensors[s]['obj_args'],
                                                           sensor_variables, sensor_defaults)
                    filter = get_filter_keyword(sensors[s]['filter'], sensor_defaults)
                    filter_args, filter_kwargs = get_filter_args(sensors[s]['filter_args'],
                                                                 sensor_variables, sensor_defaults)
                    center = (float(sensors[s]['x']), float(sensors[s]['y']))
                    neighbourhood = sensors[s]['neighbourhood']
                    new_sensor = s_class(*obj_args, **obj_kwargs)
                    
                    new_sensor.set_receptive_field(pixel, center, filter, filter_args, filter_kwargs)
                    new_sensor.label = s
                    if new_sensor.label == '-' or new_sensor.label == '':
                        new_sensor.label = '(' + sensors[s]['x'] + ',' + sensors[s]['y'] + ')'
                    if list(rows.keys()).count(sensors[s]['neighbourhood']):
                        rows[neighbourhood].append((center[0], new_sensor))
                    else:
                        rows[neighbourhood] = [(center[0], new_sensor)]

                for row in list(rows.keys()):
                    rows[row].sort()

                return rows
                
    else:
        ## if rows/columns of neighbours are not input manually,
        # the distance between any pair of sensors will be returned
        # in addition to the list of sensor objects
        nhood_dict = {}
        for s in list(sensors.keys()):
            nhood = str(sensors[s]['neighbourhood'])
            if not list(nhood_dict.keys()).count(nhood):
                # 1. sensor objects; 2. x-coordinates; 3. y-coordinates
                nhood_dict[nhood] = ([], [], [])
            s_class = get_sensor_class(sensors[s]['sensor'], sensor_defaults)
            obj_args, obj_kwargs = get_sensor_args(sensors[s]['obj_args'], sensor_variables, sensor_defaults)
            filter = get_filter_keyword(sensors[s]['filter'], sensor_defaults)
            filter_args, filter_kwargs = get_filter_args(sensors[s]['filter_args'],
                                                         sensor_variables, sensor_defaults)
            center = (float(sensors[s]['x']), float(sensors[s]['y']))
            new_sensor = s_class(*obj_args, **obj_kwargs)
            new_sensor.set_receptive_field(pixel, center, filter, filter_args, filter_kwargs)
            new_sensor.label = s
            if new_sensor.label == '-':
                new_sensor.label = '(' + sensors[s]['x'] + ',' + sensors[s]['y'] + ')'
            nhood_dict[nhood][0].append(new_sensor)
            nhood_dict[nhood][1].append(float(sensors[s]['x']))
            nhood_dict[nhood][2].append(float(sensors[s]['y']))
            
        for nhood in list(nhood_dict.keys()):
            coords = np.zeros((len(nhood_dict[nhood][0]), 2))
            coords[:, 0] = nhood_dict[nhood][1]
            coords[:, 1] = nhood_dict[nhood][2]

            nhood_dict[nhood] = (nhood_dict[nhood][0], coords)

        return nhood_dict

    
def create_components(variables, components, group_str, coords):
    """
    Create a list of components with information from a circuit-file.
    """
    l = []
    for comp in list(components.keys()):
        comp_class = get_comp_class(components[comp]['component_object'])
        obj_args, obj_kwargs = get_obj_args(components[comp]['object_args'], variables)
        transf_func = get_transfer_func(components[comp]['transfer_func'])
        func_args = get_func_args(components[comp]['func_args'], variables)
        new_comp = comp_class(transf_func, func_args[0], *obj_args, **obj_kwargs)
        new_comp.group_label = group_str
        new_comp.label = comp
        new_comp.attributes = get_comp_attributes(components[comp]['attributes'])
        new_comp.next_neighbour_single_time = get_comp_single_time(components[comp]['single_time'])
        new_comp.graph_pos = coords
        l.append(new_comp)
    return l


def connect_receiver(sensor, components, receiver_list):
    """
    Connect components to columns' sensors according to the list of receiving components.
    """
    for comp in components:
        if receiver_list.count(comp.label):
            sensor.add_connection(1.0, comp)
    
    
def connect_components(list_of_components, connections):
    """
    Connect components in one column according to the list of connections.
    """
    for connection in connections:
        connect_via_labels(list_of_components, *connection)

        
def cross_connect_next_neighbours(left, between, right, connections, manually, edge_i_j):
    """
    Connect components/neurons in neighbouring columns according to the list of connections.
    
    @todo Clearly needs some refactoring!
    """
    if manually is False:
        
        direction_i_j = edge_i_j['direction']
        # at the moment: directions are HP = horizontal positive => to the right
        #                               HN = horizontal negative => to the left
        #                               VP = vertical positive => up
        #                               VN = vertical negative => down

    for connection in connections:
        if len(connection) > 3:
            connection_ipsi = False
            connection_contra = False
            attributes = connection[3].split(',')
            if attributes.count('ipsi') or attributes.count('ipsilateral'):
                connection_ipsi = True
            if attributes.count('contra') or attributes.count('contralateral'):
                connection_contra = True
        else:
            connection_ipsi = True
            connection_contra = True

        w = parse_nn_weight(connection[1])
        
        source = get_component_via_label(left, connection[0])
        if source is not None:
            ## case left <--> right
            target = get_component_via_label(right, connection[2])
            if target is not None:
                source.add_connection(w[0], target)
                source = get_component_via_label(right, connection[0])
                target = get_component_via_label(left, connection[2])
                source.add_connection(w[0], target)
            else:                
                ## case left and/or right --> between
                target = get_component_via_label(between, connection[2])
                if target is not None:
                    if manually is False:
                    
                        if direction_i_j[0] == "H":
                            target.attributes['axis'] = 'horizontal'
                        else:
                            target.attributes['axis'] = 'vertical'
                        if direction_i_j[1] == "P":
                            target.attributes['direction'] = 'positive'
                        else:
                            target.attributes['direction'] = 'negative'
                        
                        target.direction = direction_i_j

                    if connection_ipsi:
                        ## case left --> between
                        source.add_connection(w[0], target)
                    if connection_contra:
                        ## case right --> between
                        source = get_component_via_label(right, connection[0])
                        source.add_connection(w[1], target)
        else:
            source = get_component_via_label(between, connection[0])
            
            if source is not None:
                target = get_component_via_label(left, connection[2])
                if target is not None:
                    
                    if connection_ipsi:
                        source.add_connection(w[0], target)
                    if connection_contra:
                        target = get_component_via_label(right, connection[2])
                        source.add_connection(w[1], target)


def cross_connect_next_next_neighbours(left, between, right, connections):
    """
    Connect components/neurons in next-next-neighbouring columns 
    according to the list of connections.
    """    
    for connection in connections:
        s = 'connection: ' + connection[0] + ' ' + connection[1] + ' ' + connection[2] 
        w = parse_nn_weight(connection[1])
        
        source = get_component_via_label(left, connection[0])
        if source is not None:
            target = get_component_via_label(right, connection[2])
            if target is not None:
                source.add_connection(w[0], target)
                source = get_component_via_label(right, connection[0])
                target = get_component_via_label(left, connection[2])
                source.add_connection(w[0], target)
            else:
                target = get_component_via_label(between, connection[2])
                if target is not None:
                    source.add_connection(w[0], target)
                    source = get_component_via_label(right, connection[0])
                    source.add_connection(w[1], target)

        else:
            source = get_component_via_label(between, connection[0])
            if source is not None:
                target = get_component_via_label(left, connection[2])
                if target is not None:
                    source.add_connection(w[0], target)
                    target = get_component_via_label(right, connection[2])
                    source.add_connection(w[1], target)
    
    
def parse_nn_weight(s):
    """
    Parse the 'weight' parameter of a connection between next-neighbours.    
    
    Those weight parameters need special treatment, because they can be different
    coming from a right neighbour than coming from a left neighbour.
    @param s Weight as a string.
    @return Tuple of two floats, first the weight of connections from left,
    second of connections from right neighbours.
    """
    try:
        w = float(s)
        return w, w
    except:
        split = s.split(',')
        wl = split[0].lstrip().rstrip().lstrip('l')
        try:
            wl = float(wl)
        except:
            raise RuntimeError("In Parser.creator.parse_nn_weight: could"
                               + "not understand the (left) weight " + split[0])
        wr = split[1].lstrip().rstrip().lstrip('r')
        try:
            wr = float(wr)
        except:
            raise RuntimeError("In Parser.creator.parse_nn_weight: could"
                               + "not understand the (left) weight " + split[0])
        return wl, wr

     
def get_component_via_label(list_of_components, label):
    """
    Find a component in a list of components via its label.
    @param list_of_components List of MotionDetectorModel.Components.component.Component objects.
    @param label Label of the component to look for.
    @return (Pointer to) the component with specified label.
    """
    for comp in list_of_components:
        if comp.label == label:
            return comp

        
def connect_via_labels(comp_list, l1, weight, l2):
    """
    Connect two components with labels l1 and l2 in the given list of components.
    @param comp_list List of MotionDetectorModel.Components.component.Component objects.
    @param l1 Label of the source component.
    @param weight Weight of the connection.
    @param l2 Label of the target component.
    """    
    c1 = None
    c2 = None
    for i in range(0, len(comp_list)):
        if l1 == comp_list[i].label:
            c1 = i
        if l2 == comp_list[i].label:
            c2 = i
        if c1 is not None and c2 is not None:
            break
    
    comp_list[c1].add_connection(weight, comp_list[c2])

    
def connect_tangential_via_labels(comp_list, l1, weight, l2):
    """
    Connect tangential cell with label l1 and targets with label l2 in the given list of components.
    @param comp_list List of MotionDetectorModel.Components.component.Component objects.
    @param l1 Label of the source component.
    @param weight Weight of the connection.
    @param l2 Label of the target component.
    """
    c1 = None
    targets = []
    for i in range(0, len(comp_list)):
        if c1 is None:
            if l1 == comp_list[i].label:
                c1 = i
        if l2 == comp_list[i].label:
            targets.append(i)
    
    for c2 in targets:
        comp_list[c1].add_connection(weight, comp_list[c2])


def get_comp_class(s):
    """
    Creates a Component object of given string.
    @param s String representing a Component class
    @return Component object.
    """
    if s == '-':
        exec('r=Component')
        return r
    if list(comp_dict.keys()).count(s):
        exec('r=' + str(s))
        return r
    else:
        raise RuntimeError("in creator.get_comp_class: unknown component class " + s)

    
def get_obj_args(s, variables):
    """
    Creates a list of arguments and a dictionary of keyword arguments for a Component object.
    """
    if s == '-':
        return [], {}
    return get_args(s, variables)


def get_transfer_func(s):
    """
    Returns transfer function with identical name as the given string.
    @param s String representing a transfer function.
    @return transfer function.
    """
    if s == '-':
        exec('r=identity')
        return r
    else:
        if list(transf_func_dict.keys()).count(s):
            exec('r=' + s)
            return r
        else:
            raise RuntimeError("In Parser.creator.get_transfer_func:"
                               + " unknown transfer function " + s)

        
def get_func_args(s, v):
    """
    Creates a list of arguments and a dictionary of keyword arguments for a transfer function.
    @param s String of arguments.
    @param v Dictionary of variables.
    @return List of arguments and a Dictionary of keyword arguments.
    """
    if s == '-':
        return [], {}
    
    return get_args(s, v)


def get_args(s, v):
    """
    Parse a string of arguments to a list of arguments and a dictionary of keyword arguments.
    @param s String of arguments.
    @param v Dictionary of variables.
    """
    for key in list(v.keys()):
        exec(key + '=' + str(v[key]))
    s_dict = ''
    s_list = ''
    if s.count('='):
        part = s.partition('=')
        s_list = part[0].rpartition(',')[0]
        s_keywords = part[0].rpartition(',')[2] + part[1] + part[2]
        s_dict = '{'
        while s_keywords.count('='):
            part_i = s_keywords.partition('=')
            name = "'" + part_i[0] + "'"
            rest = part_i[2]
            if rest.count('='):
                part_j = rest.partition('=')
                value = part_j[0].rpartition(',')[0]
                s_keywords = part_j[0].rpartition(',')[2] + part_j[1] + part_j[2]
            else:
                value = rest
                s_keywords = ''
            s_dict = s_dict + name + ':' + value + ','
    else:
        s_list = '[' + s + ']'
        s_dict = '{ '
    
    try:
        exec('d = ' + str(s_dict[:-1]) + ' }')
        if s_list:        
            exec('l = ' + str(s_list))
            l = list(l)
        else:
            l = []
            
        return l, d
    except:
        raise RuntimeError("In Parser.creator.get_args: could not process the list string "
                           + s_list + " \n or the dictionary string {" + s_dict[:-1] + "}")

            
def get_comp_attributes(attr):
    d = {'axis': False, 'direction': False}
    if attr is None or attr == '-':
        return d
    else:
        s = attr.split(',')
        if s.count('direction'):
            d['direction'] = True
        if s.count('axis'):
            d['axis'] = True
        return d


def get_comp_single_time(value):
    if value is None or value == '-' or value == 'False' or value == '0':
        return False
    elif value == 'True' or value == '1':
        return True
    else:
        raise RuntimeError("In Parser.creator.get_comp_single_time: can't interprete keyword")

    
def get_sensor_class(s, default):
    """
    Creates a Sensor object of given string.
    @param s String representing a Sensor class.
    @return Sensor object.
    """
    if s == '-':
        if list(default.keys()).count('sensor'):
            s = default['sensor']
        else:
            exec('r = Photoreceptor')
            return r
    if list(sensor_dict.keys()).count(s):
        exec('r = ' + str(s))
        return r
    else:
        raise RuntimeError("In Parser.creator.get_sensor_class: unknow Component-class " + s)

    
def get_sensor_args(s, variables, default):
    """
    Creates a list of arguments and a dictionary of keyword arguments for a Sensor object.
    @param s String of arguments.
    @param variables Dictionary of variables.
    @param default Dictionary of defaul values (replaces '-' for given category).
    @return Tuple: [0] list of parameters, [1] dictionary of keyword parameters.
    """
    if s == '-':
        if list(default.keys()).count('obj_args'):
            s = default['obj_args']
        else:
            return [], {}
    
    return get_args(s, variables)


def get_filter_keyword(s, defaults):
    """
    Check if the given string is in the list of possible filter keys,
    return the appropriate filter key.
    """
    if s == '-':
        if list(defaults.keys()).count('filter'):
            s = defaults['filter']
        else:
            return ''
    possible_keys = ['gaussian', 'pixel']
    if possible_keys.count(s):
        return s
    else:
        raise RuntimeError("In Parser.creator.get_filter_keyword: unkown filter keyword '"
                           + s + "'")


def get_filter_args(s, variables, defaults):
    """
    Create a list of parameters and a dictionary of keyword parameters
    from a string of parameters for a filter function.
    """
    if s == '-':
        if list(defaults.keys()).count('filter_args'):
            s = defaults['filter_args']
        else:
            return [], {}
    return get_args(s, variables)    
