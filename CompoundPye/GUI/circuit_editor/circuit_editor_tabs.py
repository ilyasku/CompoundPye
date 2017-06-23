import logging
logger = logging.getLogger("CompoundPye...circuit_editor_tabs")
from PyQt4 import QtGui
from .column_editor import ColumnEditor
from ...Parser import circuit_parser


class CircuitEditorTabs(QtGui.QTabWidget):
    """
    This class is a QTabWidget whose tabs contain two similar editor-widgets, 
    in which the user can build up and edit a circuit of neurons/components.
    Only 'column'-mode is implemented so far, which basically means that the 
    user adds/removes/edits neurons that appear in each column 
    (one column per sensor) or connecting two neighbouring columns.
    """
    def __init__(self, fname=None):
        """
        Initializes an 'EditorTabs'-object.
        @param fname Path to an initial file, None if no initial file is provided.
        """
        super(CircuitEditorTabs, self).__init__()
        self.neurons = {'column': [], 'between': [], 'tangential': []}
        self.connections = {'column': [], 'next_neighbour': [],
                            'tangential_to': [], 'tangential_from': []}
        self.receiver = []
        self.arrangement = 'column'        
        self.variables = {}
        if fname:
            self.load_file(fname)
        self.n_label = 0
        editor_column = ColumnEditor(self, 'column')
        editor_between = ColumnEditor(self, 'between')
        editor_tangential = ColumnEditor(self, 'tangential')

        self.addTab(editor_column, 'cells in column')
        self.addTab(editor_between, 'cells connecting neighbouring columns')
        self.addTab(editor_tangential, 'tangential cells')

    def load_file(self, fname):
        """
        Loads the circuit-file fname.
        @param fname Path to the circuit(text)-file.
        """
        arrangement, variables, components, connections, receiver = circuit_parser.parse_file(fname)

        msg = 'receiver:'
        msg += str(receiver)
        logger.debug(msg)
        for name in components['column_components'].keys():
            new_dict = components['column_components'][name]
            new_dict['name'] = name
            self.neurons['column'].append(new_dict)

        msg = 'after first for loop:\n'
        msg += str(new_dict)
        logger.debug(msg)

        for name in components['between_next_neighbour_components'].keys():
            new_dict = components['between_next_neighbour_components'][name]
            new_dict['name'] = name
            self.neurons['between'].append(new_dict)

        msg = 'after second for loop:\n'
        msg += str(new_dict)
        logger.debug(msg)
            
        for name in components['tangential_components'].keys():
            new_dict = components['tangential_components'][name]
            new_dict['name'] = name
            self.neurons['tangential'].append(new_dict)

        msg = 'after third for loop:\n'
        msg += str(new_dict)
        logger.debug(msg)

        for c in connections['column_connections']:
            self.connections['column'].append(c)
        for c in connections['next_neighbour_connections']:
            self.connections['next_neighbour'].append(c)
        for c in connections['tangential_to_connections']:
            self.connections['tangential_to'].append(c)
        for c in connections['tangential_from_connections']:
            self.connections['tangential_from'].append(c)

        self.receiver = receiver
        self.arrangement = arrangement
        self.variables = variables
        
    def save_file(self, fname):
        """
        Saves the current circuit in a circuit(text)-file.
        """
        circuit_parser.save_file(fname, self.arrangement, self.variables,
                                 self.neurons, self.connections, self.receiver)
