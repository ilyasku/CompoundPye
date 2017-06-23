from PyQt4 import QtGui
from sensor_line import SensorLine
from ...Parser import sensor_parser as sp


class EditorScrollArea(QtGui.QScrollArea):
    """
    This ScrollArea is the actual editor window in which the user can 
    add/remove sensors and click on a sensor's button to edit its properties.
    """
    def __init__(self, parent_EditorWidget, initial_file=None):
        """
        Initializes an EditorScrollArea.
        @param parent_EditorWidget Requires the parent EditorWidget 
        (or rather a pointer to it) which serves as frame for this 
        EditorScrollArea as input, to access its variables.
        @param initial_file Can be initialized with a path to a sensor-file (text-file).
        """
        super(EditorScrollArea, self).__init__()
        
        self.n_sensors = 0        
        self.sensors = []    
        self.SensorLines = []
        self.parent_EW = parent_EditorWidget        
        self.init_UI(initial_file)
        
    def init_UI(self, initial_file):
        """
        Sets up all the widgets (graphical stuff like buttons, 
        labels, etc.) displayed in this EditorScrollArea.
        """
        self.setWidgetResizable(True)
        w = QtGui.QWidget()
        self.setWidget(w)
        if initial_file is None:
            self.settings, self.variables, self.defaults, sensors = {'neighbours': 'x'}, {}, {}, []
        else:
            sensors = []
            self.settings, self.variables, self.defaults, s = self.do_load(initial_file)
            # adding and removing widgets will be easier with a list than
            # a dictionary --> put name inside dict
            for key in s.keys():
                new_dict = s[key]
                new_dict['name'] = key
                sensors.append(new_dict)
        
        self.vbox = QtGui.QVBoxLayout()
        w.setLayout(self.vbox)
        
        hbox_btn = QtGui.QHBoxLayout()
        
        btn_add = QtGui.QPushButton('add sensor')
        btn_add.clicked.connect(self.do_add_sensor)
        
        hbox_btn.addWidget(btn_add)
        hbox_btn.addStretch(1)
        
        self.vbox.addLayout(hbox_btn)
        self.vbox.addStretch(1)                
        
        for s_i in sensors:
            self.add_sensor(s_i)
    
    def add_sensor(self, initial_values=None):
        """
        Adds a sensor ('SensorLine'-widget) to this EditorScrollArea 
        and the sensor's values to this EditorScrollArea.sensor list.
        @param initial_values The new 'SensorLine'-widget can be 
        initialized with a dictionary of sensor-values.
        """
        new_sline = SensorLine(self, self.n_sensors, initial_values)
        self.vbox.insertWidget(len(self.sensors), new_sline)
        self.sensors.append(new_sline.values)
        self.n_sensors += 1
        self.SensorLines.append(new_sline)
    
    def do_add_sensor(self):
        """
        Adds a new ('SensorLine'-widget) to this EditorScrollArea 
        and default sensor values to the list EditorScrollArea.sensor.
        """
        new_sline = SensorLine(self, self.n_sensors)
        self.vbox.insertWidget(len(self.sensors), new_sline)
        self.sensors.append(new_sline.values)
        self.n_sensors += 1
        self.SensorLines.append(new_sline)
    
    def do_load(self, fname):
        """
        Load a sensor-file (text-file).
        @param fname Path to file to load.
        """
        return sp.parse_file(fname)

    def do_remove(self, index):
        """
        Remove the 'SensorLine'-widget with given index from the EditorScrollArea.
        @param index Index of the 'SensorLine'-widget to be removed.
        """
        item = self.vbox.itemAt(index)
        self.vbox.removeItem(item)
        self.sensors.pop(index)
        self.SensorLines.pop(index)
        self.n_sensors = self.n_sensors - 1
        item.widget().close()
        for i in range(0, len(self.sensors)):
            self.SensorLines[i].index = i
            
    def do_save(self, fname):
        """
        Save the sensors currently shown on the EditorScrollArea to a sensor-file.
        @param fname Path to target file.
        """
        sp.save_file(fname, self.settings, self.variables,
                     self.defaults, self.sensors)                
