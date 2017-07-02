import json
from collections import namedtuple


def create_json_dict(arrangement, variables, neurons, connections, receiver):

    json_dict = {}
    json_dict["arrangement"] = arrangement
    json_dict["variables"] = variables
    
    neuron_list_column = _get_neuron_list(neurons["column"])
    neuron_list_between = _get_neuron_list(neurons["between"])
    neuron_list_tangential = _get_neuron_list(neurons["tangential"])

    json_dict["neurons"] = {"column": neuron_list_column,
                            "between": neuron_list_between,
                            "tangential": neuron_list_tangential}

    

def _get_neuron_list(list_of_component_widgets):
    components_list = []
    for component_widget in list_of_component_widgets:
        component = component_widget.values
        components_list.append(component)
    return components_list
