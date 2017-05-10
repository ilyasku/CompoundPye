from PyQt4 import QtGui

from sensor_popup import SensorPopup


class SensorLine(QtGui.QWidget):
    """
    A line representing a sensor in the editor window (EditorScrollArea), 
    containing a button showing the sensor's label and a remove-button.
    """
    def __init__(self, parent_ScrollArea, index, initial_values=None):
        """
        Initializes a 'SensorLine'-widget.
        @param parent_ScrollArea Requires the parent EditorScrollArea 
        (or rather a pointer to it) as input to access its variables 
        (lists of all sensors and their values, etc.).
        @param index Index of this'SensorLine'-widget in the parent EditorScrollArea's layout.
        @param initial_values Can be initialized with a dictionary of sensor-values.
        """
        super(SensorLine, self).__init__()
        self.parent_SA = parent_ScrollArea
        
        self.index = index

        if initial_values is None:
            self.values = {'name': 'new sensor ' + str(len(self.parent_SA.sensors)),
                           'filter': 'gaussian',
                           'filter_args': '[1,1]',
                           'neighbourhood': '-',
                           'obj_args': '-',
                           'sensor': 'Sensor',
                           'x': '0.0',
                           'y': '0.0'}            
        else:
            self.values = initial_values
            
        self.init_UI()
                
    def init_UI(self):
        """
        Set up all the widgets (labels, buttons, etc.) displayed on this SensorLine.
        """
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        self.btn_sensor = QtGui.QPushButton(self.values['name'])
        btn_remove = QtGui.QPushButton('remove')
        
        self.btn_sensor.clicked.connect(self.do_popup)
        btn_remove.clicked.connect(self.remove)

        grid.addWidget(self.btn_sensor, 0, 0)
        grid.addWidget(btn_remove, 0, 1)
        
    def edit_name(self):
        """
        Read the name of the sensor from the values-dictionary 
        and set the label of its button accordingly.
        """
        self.btn_sensor.setText(self.values['name'])
        
    def do_popup(self):
        """
        Pop up a 'SensorPopup'-widget to edit this sensor's values.
        """
        self.popup = SensorPopup(self)
        self.popup.show()

    def remove(self):
        """
        Remove this SensorLine from the parent EditorScrollArea.
        """
        self.parent_SA.do_remove(self.index)
