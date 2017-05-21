## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 19.01.15

"""
@package CompoundPye.src.Parser.circuit_parser

Provides functions to generate circuit information from a circuit-file (text-file) 
to be passed on to MotionDetectorModel.Parser.creator.create_circ_lists.
"""


def save_file(fname, arrangement, variables, neurons, connections, receiver):
    """
    Save circuit-data from the GUI's circuit-editor to file.
    """
    fstring = 'arrangement=' + arrangement + '\n'
    for var in list(variables.keys()):
        fstring = fstring + 'variable ' + var + '=' + str(variables[var]) + '\n'
    if arrangement == 'column':
        fstring = fstring + 'column_components{\n'
        for n in neurons['column']:
            component = n.values
            comp_line = component['name'].replace(' ', '_') + '\t'
            comp_line = comp_line + component['component_object'] + '\t'
            if str(component['object_args']).isspace() or len(str(component['object_args'])) == 0:
                comp_line = comp_line + '-'
            else:
                comp_line = comp_line + component['object_args'] + '\t'
            comp_line = comp_line + component['transfer_func'] + '\t'
            if str(component['func_args']).isspace() or len(str(component['func_args'])) == 0:
                comp_line = comp_line + '-'
            else:
                comp_line = comp_line + component['func_args'] + '\t'
            comp_line = comp_line + str(component['graph_pos']) + '\n'
            fstring = fstring + comp_line
        fstring = fstring + '}\n\n'
        
        fstring = fstring + 'receiver{\n'
        for r in receiver:
            fstring = fstring + r + '\n'
        fstring = fstring + '}\n\n'

        fstring = fstring + 'column_connections{\n'
        for c in connections['column']:
            connection_line = c[0] + '\t' + str(c[1]) + '\t' + c[2] + '\n'
            fstring = fstring + connection_line
        fstring = fstring + '}\n\n'

        fstring = fstring + 'between_next_neighbour_components{\n'
        ## write neurons between next neighbours
        for n in neurons['between']:
            component = n.values
            # replace whitespaces in names
            comp_line = component['name'].replace(' ', '_') + '\t'
            comp_line = comp_line + component['component_object'] + '\t'
            if str(component['object_args']).isspace() or len(str(component['object_args'])) == 0:
                comp_line = comp_line + '-\t'
            else:
                comp_line = comp_line + component['object_args'] + '\t'
            comp_line = comp_line + component['transfer_func'] + '\t'
            if str(component['func_args']).isspace() or len(str(component['func_args'])) == 0:
                comp_line = comp_line + '-\t'
            else:
                comp_line = comp_line + component['func_args'] + '\t'
            comp_line = comp_line + str(component['graph_pos']) + '\t'
            
            if str(component['attributes']).isspace() or len(str(component['attributes'])) == 0 or component['attributes'] is None:
                comp_line = comp_line + '-\n'
            else:
                comp_line = comp_line + component['attributes'] + '\n'
            fstring = fstring + comp_line
        fstring = fstring + '}\n\n'                

        fstring = fstring + 'tangential_components{\n'
        ## write neurons between next neighbours
        for neuron in neurons['tangential']:
            component = neuron.values
            # replace whitespaces in names
            comp_line = component['name'].replace(' ', '_') + '\t'
            comp_line = comp_line + component['component_object'] + '\t'
            if str(component['object_args']).isspace() or len(str(component['object_args'])) == 0:
                comp_line = comp_line + '-\t'
            else:
                comp_line = comp_line + component['object_args'] + '\t'
            comp_line = comp_line + component['transfer_func'] + '\t'
            if str(component['func_args']).isspace() or len(str(component['func_args'])) == 0:
                comp_line = comp_line + '-\t'
            else:
                comp_line = comp_line + component['func_args'] + '\t'
            comp_line = comp_line + str(component['graph_pos']) + '\t'
                        
            if (str(component['attributes']).isspace() or len(str(component['attributes'])) == 0 or component['attributes'] is None):
                comp_line = comp_line + '-\n'
            else:
                comp_line = comp_line + component['attributes'] + '\n'
            fstring = fstring + comp_line
        fstring = fstring + '}\n\n'

        fstring = fstring + 'next_neighbour_connections{\n'
        for c in connections['next_neighbour']:
            connection_line = ''
            for c_i in c:
                connection_line += str(c_i).replace(' ', '_') + '\t'
            connection_line = connection_line[:-1] + '\n'
            fstring = fstring + connection_line
        fstring = fstring + '}\n\n'

        fstring = fstring + 'tangential_to_connections{\n'
        for c in connections['tangential_to']:
            connection_line = ''
            for c_i in c:
                connection_line += str(c_i).replace(' ', '_') + '\t'
            connection_line = connection_line[:-1] + '\n'
            fstring = fstring + connection_line
        fstring = fstring + '}\n\n'

        fstring = fstring + 'tangential_from_connections{\n'
        for c in connections['tangential_from']:
            connection_line = ''
            for c_i in c:
                connection_line += str(c_i).replace(' ', '_') + '\t'
            connection_line = connection_line[:-1] + '\n'
            fstring = fstring + connection_line
        fstring = fstring + '}\n\n'
                    
        fstring = fstring + 'between_next_next_neighbour_components{}\n'
        fstring = fstring + 'next_next_neighbour_connections{}'
        
        f = open(fname, 'w')
        f.write(fstring)
        f.close()

    else:
        raise NotImplementedError("In circuit_parser.save_file: arrangement has to be \"column\","
                                  + "no other arrangement implemented so far")


def parse_file(fname):
    """
    Parse circuit-data from file to several lists and dictionaries.
    @param fname Name of circuit file.
    @return Tuple of 5 items: 
            (1) arrangement-keyword (currently only 'column' allowed)
            (2) Dictionary of variables defined in circuit file header.
            (3) Dictionary of components, separated into 4 categories:
                (I) 'column_components' -> Components inside one columnd
                (II) 'between_next_neighbour_components' -> Components considered to be
                     inbetween two columns.
                (III) 'tangential_components' -> Not in columns, global/tangential components.
                (IV) ... Not in use currently
            (4) Dictionary defining connections.
            (5) List of components receiving input of photoreceptors.
    """
    f = open(fname, 'r')
    complete_string = f.read()
    header, sections = separate_sections(complete_string)
    arrangement, variables = parse_header(header)
    components, connections, receiver = parse_sections(arrangement, sections)
    return arrangement, variables, components, connections, receiver


def separate_sections(s):
    """
    Separate the given string (read from a circuit-file) into its header and different sections.
    """
    first_split = s.split('{')
    header = first_split[0].split('\n')
    first_split = first_split[1:]
    first_split.insert(0, header[-1])
    sections = []
    section_name = first_split[0].lstrip()
    for i in range(1, len(first_split)):
        split_i = first_split[i].split('}')
        sections.append([section_name, split_i[0]])
        section_name = split_i[1].lstrip()
    header = header[:-1]
    return header, sections


def parse_sections(arrangement, sections):
    """
    Parse the strings of different sections ('components'-sections,'connections'-sections and 
    a 'receiver'-section) to dictionaries and lists.
    """
    if arrangement == 'column':
        components = {}
        connections = {}
        r = []
        for s in sections:
            if s[0].split('_')[-1] == 'components':
                components[s[0]] = parse_component_section(s[1])
            elif s[0].split('_')[-1] == 'connections':
                connections[s[0]] = parse_connection_section(s[1])
            elif s[0] == 'receiver':
                for line in s[1].split('\n'):
                    if line.lstrip().rstrip():
                        r.append(line.lstrip().rstrip())
        return components, connections, r
    else:
        raise RuntimeError('In circuit_parser.parse_sections: arrangement unknown!')

    
def parse_connection_section(content):
    """
    Parse the string of a single 'connections'-section.
    @param content String of the 'connections'-section.
    @return List of connection tuples.
    """
    lines = content.split('\n')
    connections = []
    for line in lines:
        if line:
            if line.lstrip()[0] == '#':
                pass
            else:
                split = line.split()
                connections.append(split)
                
    return connections


def parse_component_section(content):
    """
    Parse a 'components'-section to a dictionary.
    @param content String of the 'components'-section.
    @return Dictionary holding one dictionary (with information of a component) 
    per component in the section.
    """
    lines = content.split('\n')
    components = {}
    for line in lines:        
        if line:
            if not line.lstrip()[0] == '#':                
                parse_component_line(components, line)
    return components


def parse_component_line(d, line):
    """
    Parse a single line of a 'components'-section (one line = information of one component) 
    to a dictionary; add this dictionary to given d.
    @param d Dictionary holding one dictionary (with information of a component)
    per component in the whole 'components'-section.
    @param line Single line to be parsed.
    """
    split = line.split()
    name = split[0]
    component_object = split[1]
    object_args = split[2]
    transfer_func = split[3]
    func_args = split[4]
    graph_pos = split[5]
    
    attributes = None
    single_time = None

    if len(split) > 6:
        attributes = split[6]
        if len(split) > 7:
            single_time = split[7]
            
    d[name] = {'component_object': component_object, 'object_args': object_args,
               'transfer_func': transfer_func, 'func_args': func_args,
               'graph_pos': graph_pos, 'attributes': attributes, 'single_time': single_time}

    
def parse_header(h):
    """
    Parse the header of the file, read some settings and variables from it.
    @param h Header string.
    @return A list of settings and a dictionary with variables defined in the header.

    @todo Needs refactor!
    """
    arrangement = None
    variables = {}
    for line in h:
        if line:
            if line.lstrip()[0] == '#':
                pass
            elif len(line) > 9:
                if line[:9] == 'variable ':
                    name, value = line[9:].split('=')
                    name = name.lstrip().rstrip()
                    variables[name] = float(value)

                else:
                    if len(line) > 11:
                        if line[:11] == 'arrangement':
                            arrangement = line.split('=')[1]
                        else:
                            print('invalid input "' + line + '"')
                    else:
                        print('invalid input "' + line + '"')

            else:
                print('invalid input "' + line + '"')
    return arrangement, variables
