from PyQt4 import QtGui
from .component_widget import ComponentWidget


class ColumnEditor(QtGui.QFrame):
    """
    An ditor-widget that serves as content of the tabs of 'EditorTabs'-objects. 
    It allows the user to add/remove/edit neurons in a group specified by the tab.
    """
    def __init__(self, parent_EditorTabs, mode):
        """
        Initializes an 'Editor'-object.
        @param parent_EditorTabs Requires the parent 'EditorTabs'-object as parameter 
        to access its list and dictionries that store components/neurons and parameters.
        @param mode The mode can be 'column' or 'between', it tells the Editor 
        which list of neurons of the parent 'EditorTabs'-object it should read from/write to.
        """
        super(ColumnEditor, self).__init__()
        self.parent_EditorTabs = parent_EditorTabs
        self.mode = mode
        self.n = 0        
        self.neurons = self.parent_EditorTabs.neurons
        self.connections = self.parent_EditorTabs.connections
        self.init_UI()                

    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """
        wrap_vbox = QtGui.QVBoxLayout()
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)        
        widget_in_scroll_area = QtGui.QWidget()
        self.scrollArea.setWidget(widget_in_scroll_area)

        self.vbox = QtGui.QVBoxLayout()
        widget_in_scroll_area.setLayout(self.vbox)        
        wrap_vbox.addWidget(self.scrollArea)
        self.setLayout(wrap_vbox)

        self.btn_add = QtGui.QPushButton('add neuron')
        self.btn_add.clicked.connect(self.add_neuron)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.btn_add)
        hbox.addStretch(1)

        self.vbox.addLayout(hbox)
        self.vbox.addStretch(1)

        initial_copy = self.neurons[self.mode][:]
        self.neurons[self.mode] = []
        while len(initial_copy):
            self.add_neuron(initial_copy.pop(0))

    def add_neuron(self, initial=False):
        """
        Adds a neuron to the list of neurons, either with or without initial parameters.
        @param initial Can be initialized with a dictionary of parameters.
        """
        if initial is False:
            neuron = ComponentWidget(self)
        else:
            neuron = ComponentWidget(self, initial)
        self.vbox.insertWidget(self.n, neuron)        
        self.neurons[self.mode].append(neuron)        
        self.n += 1
        self.parent_EditorTabs.n_label += 1
    
    def removed(self, j):
        """
        Tells the 'Editor'-object, that the 'remove'-button of a neuron (CompWidget) 
        shown in the editor has been clicked and that the Editor has to remove it from its lists.
        @param j Index of the neuron (CompWidget) to be removed.
        """
        self.n = self.vbox.count() - 2
        
        label_of_removed_neuron = self.neurons[self.mode][j].name

        self.neurons[self.mode].pop(j)
        for i in range(len(self.neurons[self.mode])):
            self.neurons[self.mode][i].index = i

        for key in self.connections.keys():
            need_to_pop = []
            for i in range(0, len(self.connections[key])):
                c = self.connections[key][i]
                if c[0] == label_of_removed_neuron or c[2] == label_of_removed_neuron:
                    need_to_pop.append(i)
                else:
                    pass
            need_to_pop.reverse()
            for k in need_to_pop:
                self.connections[key].pop(k)

    def change_name(self, old, new):
        """
        Tells the 'Editor'-object that a neuron's (CompWidget's) name has been changed; scans 
        through the lists of connections to change the old name to the new name in those lists.
        @param old Old name of the neuron (CompWidget).
        @param new New name of the neuron (CompWidget).
        """
        for key in self.connections.keys():
            for i in range(0, len(self.connections[key])):
                c = self.connections[key][i]
                if c[0] == old:
                    l = list(c)
                    l[0] = new
                    c = tuple(l)
                if c[2] == old:
                    l = list(c)
                    l[2] = new
                    c = tuple(l)
                self.connections[key][i] = c
