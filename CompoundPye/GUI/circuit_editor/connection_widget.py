from PyQt4 import QtGui
from .connection_editor_tangential import ConnectionEditTangential
from .connection_editor import ConnectionEdit


class ConnectionWidget(QtGui.QWidget):
    """
    A widget that allows the user to choose targets of 
    connections via combo-boxes and set the connections' weights.
    """
    def __init__(self, parent_editor, parent_PopupConnection,
                 neuron_name, widget_mode='column'):
        """
        Initializes a ConnectionWidget.
        @param parent_editor Requires the parent Editor (or rather a pointer to it) of the 
        'PopupConnections'-object as input to access its lists of connections.
        @param parent_PopupConnection Requires the parent PopupConnections (or rather a 
        pointer to it) as input to be able to call its remove-function.
        @param neuron_name Name of the neuron, required to read/write 
        the neuron's connections from/to the lists of connections.
        @param widget_mode String to specify if this neuron is in a column 
        (widget_mode=='column') or between columns (widget_mode=='next_neighbour').
        """
        super(ConnectionWidget, self).__init__()
        self.parent_editor = parent_editor
        self.parent_popup = parent_PopupConnection
        self.source = neuron_name
        self.widget_mode = widget_mode
        self.n = 0
        self.initial_connections = []
        number_of_deleted_items = 0
        if widget_mode == 'column':
            for i in range(0, len(self.parent_editor.connections['column'])):
                if self.parent_editor.connections[
                        'column'][i - number_of_deleted_items][0] == self.source:
                    self.initial_connections.append(
                        self.parent_editor.connections['column'].pop(i - number_of_deleted_items))
                    number_of_deleted_items += 1
        elif widget_mode == 'nn':            
            for i in range(0, len(self.parent_editor.connections['next_neighbour'])):
                if self.parent_editor.connections[
                        'next_neighbour'][i - number_of_deleted_items][0] == self.source:
                    self.initial_connections.append(
                        self.parent_editor.connections['next_neighbour'].pop(
                            i - number_of_deleted_items))
                    number_of_deleted_items += 1
        elif widget_mode == 'tangential_to':            
            self.target = self.source
            self.source = None
            for i in range(0, len(self.parent_editor.connections['tangential_to'])):
                if self.parent_editor.connections[
                        'tangential_to'][i - number_of_deleted_items][2] == self.target:
                    self.initial_connections.append(
                        self.parent_editor.connections['tangential_to'].pop(
                            i - number_of_deleted_items))
                    number_of_deleted_items += 1            
        elif widget_mode == 'tangential_from':            
            for i in range(0, len(self.parent_editor.connections['tangential_from'])):
                if self.parent_editor.connections[
                        'tangential_from'][i - number_of_deleted_items][0] == self.source:
                    self.initial_connections.append(
                        self.parent_editor.connections['tangential_from'].pop(
                            i - number_of_deleted_items))
                    number_of_deleted_items += 1
        self.connections = []
        self.ConnectionEdit_list = []
        self.init_UI(widget_mode)
        self.mode = widget_mode

    def init_UI(self, widget_mode):
        """
        Sets up all the widgets (buttons, labels, line-edits, etc) 
        contained by this ConnectionWidget.
        @param widget_mode String to specify if this ConnectionWidget's neuron is in 
        a column (widget_mode == 'column') or between columns (widget_mode == 'next_neighbour').
        """
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)
        self.n_list = []
        if widget_mode == 'column':
            for n in self.parent_editor.neurons['column']:
                self.n_list.append(n.values['name'])
        else:
            if widget_mode == 'nn':
                for key in self.parent_editor.neurons:
                    if key != 'tangential':
                        for n in self.parent_editor.neurons[key]:
                            self.n_list.append(n.values['name'])
            elif widget_mode == 'tangential_to':
                for key in self.parent_editor.neurons:
                    if key != 'tangential':
                        for n in self.parent_editor.neurons[key]:
                            self.n_list.append(n.values['name'])
            else:
                for key in self.parent_editor.neurons:
                    for n in self.parent_editor.neurons[key]:
                        self.n_list.append(n.values['name'])

        hbox_add = QtGui.QHBoxLayout()        
        if widget_mode == 'column':
            btn_add = QtGui.QPushButton('add connection within column')
        elif widget_mode == 'nn':
            btn_add = QtGui.QPushButton('add connection to neighbouring column')
        elif widget_mode == 'tangential_to':
            btn_add = QtGui.QPushButton('add connection to this tangential cell')
        else:
            btn_add = QtGui.QPushButton('add connection from this tangential\nto any other cell')

        if self.widget_mode == 'tangential_to':
            btn_add.clicked.connect(self.create_connect_edit_tangential_to)
        else:
            btn_add.clicked.connect(self.create_connect_edit)        
        hbox_add.addWidget(btn_add)
        hbox_add.addStretch(1)
        
        self.vbox.addLayout(hbox_add)
        self.vbox.addStretch(1)
        
        for i in range(0, len(self.initial_connections)):
            c = self.initial_connections[i]
            if self.widget_mode == 'tangential_to':
                self.create_connect_edit_tangential_to(c)
            elif self.widget_mode == 'tangential_from':
                self.create_connect_edit(c[2], c[1])
            else:
                self.create_connect_edit(c[2], c[1])
                
    def create_connect_edit_tangential_to(self, connection=None):
        """
        Creates a ConnectionEditTangential widget.
        @param connection Tuple defining an initial connection.
        """
        if not (type(connection) == list or type(connection) == tuple):
            connection = ('', 1.0, self.target, '')
        new_ConnectionEdit = ConnectionEditTangential(self, *connection)
        new_ConnectionEdit.index = self.n
        self.vbox.insertWidget(self.n, new_ConnectionEdit)
        self.connections.append(connection)
        self.ConnectionEdit_list.append(new_ConnectionEdit)
        self.n += 1

    def create_connect_edit(self, default_target='', default_weight=1.0):
        """
        Creates and adds a new line to the ConnectionWidget's connection editor.
        @param default_target Can be initialized with a target specified by this string.
        @param default_weight Can be initialized with a connection strength specified by this value.
        """
        new_ConnectionEdit = ConnectionEdit(self, default_target, default_weight)
        new_ConnectionEdit.index = self.n
        self.vbox.insertWidget(self.n, new_ConnectionEdit)
        self.connections.append((self.source, default_weight, default_target))
        self.ConnectionEdit_list.append(new_ConnectionEdit)
        self.n += 1

    def remove(self, i):
        """
        Remove line i in the ConnectionWidget editor window.
        @param i Index of the line to be removed.
        """
        item = self.vbox.itemAt(i)
        self.vbox.removeItem(item)
        self.n = self.vbox.count() - 2
        self.connections.pop(i)
        self.ConnectionEdit_list.pop(i)
        for j in range(len(self.ConnectionEdit_list)):
            self.ConnectionEdit_list[j].index = j

    def do_cancel(self):
        """
        Discard all changes made in this ConnectionWidget's editor window.
        """
        if self.widget_mode == 'column':
            mode = self.widget_mode
        elif self.widget_mode == 'nn':
            mode = 'next_neighbour'
        elif self.widget_mode == 'tangential_to':
            mode = 'tangential_to'
        else:
            mode = 'tangential_from'
        self.parent_editor.connections[mode] = self.parent_editor.connections[mode] \
                                               + self.initial_connections

    def do_done(self):
        """
        Store all changes made in this ConnectionWidget's editor 
        window to the parent Editor's lists.
        """
        if self.widget_mode == 'column':
            mode = self.widget_mode
        elif self.widget_mode == 'nn':
            mode = 'next_neighbour'
        elif self.widget_mode == 'tangential_to':
            mode = 'tangential_to'
        else:
            mode = 'tangential_from'
        self.parent_editor.connections[mode] = self.parent_editor.connections[mode] \
                                               + self.connections
