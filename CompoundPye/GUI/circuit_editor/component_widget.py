from PyQt4 import QtGui
from .popup_neuron import PopupNeuron
from .popup_connections_tangential import PopupConnectionsTangential
from .popup_connections import PopupConnections


class ComponentWidget(QtGui.QWidget):
    """
    A CompWidget is a graphical representation (just a line of buttons really) 
    of a neuron/component in an 'Editor'-object.
    The user can click its buttons to edit/remove the neuron.
    """
    def __init__(self, parent_UI, initial=False):
        """
        Initializes an 'CompWidget'-object.
        @param parent_UI Requires the parent 'Editor'-object as parameter to 
        access its list and dictionries to store this neuron's/component's parameters.
        @param initial The 'CompWidget'-object can be initialized with a dictionary of parameters.
        """
        super(ComponentWidget, self).__init__()
        self.parent_UI = parent_UI
        self.index = self.parent_UI.n
        if initial is False:
            self.values = {'name': 'new neuron ' + str(self.parent_UI.parent_EditorTabs.n_label),
                           'component_object': 'Component',
                           'object_args': '-',
                           'transfer_func': 'identity', 'func_args': '-',
                           'graph_pos': None, 'attributes': '-',
                           'single_time': '-'}
        else:
            self.values = initial
        self.name = self.values['name']
        self.popup_neuron = None
        self.popup_connection = None
        self.init_UI()
        
    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        self.btn_add_connection = QtGui.QPushButton('connections')
        self.btn_add_connection.clicked.connect(self.create_popup_connections)
        self.btn_add_connection.setToolTip("click to edit connections")
        self.btn_name = QtGui.QPushButton(self.values['name'])
        self.btn_name.clicked.connect(self.create_popup_neuron)
        self.btn_name.setToolTip("click to edit properties")
        self.btn_remove = QtGui.QPushButton('remove')
        self.btn_remove.clicked.connect(self.remove)        
        self.grid.addWidget(self.btn_name, 0, 0)
        self.grid.addWidget(self.btn_add_connection, 0, 1)
        self.grid.addWidget(self.btn_remove, 0, 2)

    def create_popup_neuron(self):
        """
        Pops up a 'PopupNeuron'-widget, in which the user can edit the neuron's parameters.
        """
        self.popup_neuron = PopupNeuron(self)
        self.popup_neuron.show()

    def create_popup_connections(self):
        """
        Pops up a 'PopupConnections'-widget, in which the user can edit/add/remove connections.
        """

        if self.parent_UI.mode == 'tangential':
            self.popup_connection = PopupConnectionsTangential(self.parent_UI,
                                                               self.values['name'])
        else:
            self.popup_connection = PopupConnections(self.parent_UI, self.values['name'])
        self.popup_connection.show()

    def remove(self):
        """
        Removes this 'CompWidget'-object from its parent 'Editor'-widget 
        (and all its entries in the 'Editor'-widgets lists and dictionaries).
        """
        item = self.parent_UI.vbox.itemAt(self.index)
        self.parent_UI.vbox.removeItem(item)
        self.parent_UI.removed(self.index)
        item.widget().close()

    def from_file_dict(self, name, comp_dict):
        """
        @todo SEEMS LIKE THIS IS NOT USED ANYWHERE?
        """
        self.values = comp_dict
        self.values['name'] = name
    
    def edited(self):
        """
        After editing in a 'PopupNeuron'-widget is finished, this neuron's name 
        is read from the values-dictionary and its button's label is set appropriately.
        """
        self.btn_name.setText(self.values['name'])
        self.parent_UI.change_name(self.name, self.values['name'])
        self.name = self.values['name']
