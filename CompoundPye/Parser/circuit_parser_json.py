import json
from collections import namedtuple


def create_json_dict(arrangement, variables, neurons, connections, receiver):

    json_dict = {}
    json_dict["arrangement"] = arrangement
    json_dict["variables"] = variables
    
    column_neurons = _get_neurons_dict(neurons["column"])


def _get_neurons_dict(list_of_components):
    
    
