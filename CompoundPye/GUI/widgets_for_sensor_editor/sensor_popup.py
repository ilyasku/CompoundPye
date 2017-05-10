from PyQt4 import QtGui

from ..styles import blue_tooltips
from ...Parser import creator
dict_of_sensors = creator.sensor_dict
list_of_filters = ['gaussian', 'pixel']


class SensorPopup(QtGui.QWidget):
    """
    A (pop-up) widget in which the user can edit the properties of a sensor.
    """
    def __init__(self, parent_SensorLine):
        """
        Initializes a SensorPopup.
        @param parent_SensorLine Requires the parent SensorLine of the 
        sensor this pop-up belongs to, to access its values-dictionary.
        """
        super(SensorPopup, self).__init__()
        self.parent_SensorLine = parent_SensorLine        
        self.copy_values = self.parent_SensorLine.values.copy()

        self.init_UI()

    def init_UI(self):
        """
        Initializes all widgets (labels, buttons, etc.) displayed on this SensorPopup.
        """
        self.setStyleSheet(blue_tooltips)
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        # ------------- name --------------------------------------
        lbl_name = QtGui.QLabel('name')
        self.le_name = QtGui.QLineEdit()
        self.le_name.setText(self.copy_values['name'])
        self.le_name.editingFinished.connect(
            lambda: self.set_value('name', self.le_name.text()))        
        grid.addWidget(lbl_name, 0, 0)
        grid.addWidget(self.le_name, 0, 1, 1, 2)
        # ---------------------------------------------------------
        # ------------------- sensor object -----------------------
        lbl_sensor = QtGui.QLabel('sensor object')
        self.combo_sensor = QtGui.QComboBox()
        for s in dict_of_sensors.keys():
            self.combo_sensor.addItem(s)
        index = self.combo_sensor.findText(self.copy_values['sensor'])
        self.combo_sensor.setCurrentIndex(index)
        self.combo_sensor.activated[str].connect(self.set_sensor)
        grid.addWidget(lbl_sensor, 1, 0)
        grid.addWidget(self.combo_sensor, 1, 1, 1, 2)
        # ---------------------------------------------------------
        # ------------------ object args --------------------------        
        lbl_obj_args = QtGui.QLabel('object arguments')
        self.le_obj_args = QtGui.QLineEdit()
        self.le_obj_args.setText(self.copy_values['obj_args'])
        self.le_obj_args.editingFinished.connect(
            lambda: self.set_value('obj_args', self.le_obj_args.text()))
        grid.addWidget(lbl_obj_args, 2, 0)
        grid.addWidget(self.le_obj_args, 2, 1, 1, 2)
        # ---------------------------------------------------------
        self.update_sensor_tooltips(self.copy_values['sensor'])
        # --------------------- filter ----------------------------
        lbl_filter = QtGui.QLabel('filter')
        combo_filter = QtGui.QComboBox()
        for f in list_of_filters:
            combo_filter.addItem(f)
        index = combo_filter.findText(self.copy_values['filter'])
        combo_filter.setCurrentIndex(index)
        combo_filter.activated[str].connect(self.set_filter)
        grid.addWidget(lbl_filter, 3, 0)
        grid.addWidget(combo_filter, 3, 1, 1, 2)
        # ---------------------------------------------------------
        # -------------------- filter args ------------------------
        lbl_f_args = QtGui.QLabel("filter arguments\n(comma separated, keywords "
                                  + "possible\ndon\'t use empty spaces!)")
        self.le_f_args = QtGui.QLineEdit()
        self.le_f_args.setText(self.copy_values['filter_args'])
        self.le_f_args.editingFinished.connect(
            lambda: self.set_value('filter_args', self.le_f_args.text()))
        grid.addWidget(lbl_f_args, 4, 0)
        grid.addWidget(self.le_f_args, 4, 1, 1, 2)
        # ---------------------------------------------------------
        # ------------------- postition ---------------------------
        lbl_pos = QtGui.QLabel('position')
        le_x = QtGui.QLineEdit()
        le_y = QtGui.QLineEdit()
        le_x.setText(self.copy_values['x'])
        le_y.setText(self.copy_values['y'])        
        le_x.setToolTip('x-coordinate\n(in relative width)')
        le_y.setToolTip('y-coordinate\n(in relative height)')        
        le_x.editingFinished.connect(lambda: self.set_value('x', le_x.text()))
        le_y.editingFinished.connect(lambda: self.set_value('y', le_y.text()))

        grid.addWidget(lbl_pos, 5, 0)
        grid.addWidget(le_x, 5, 1)
        grid.addWidget(le_y, 5, 2)        
        # ---------------- neighbourhood ----------------------------
        lbl_nbour = QtGui.QLabel('neighbourhood')
        le_nbour = QtGui.QLineEdit()
        le_nbour.setText(self.copy_values['neighbourhood'])
        le_nbour.editingFinished.connect(
            lambda: self.set_value('neighbourhood', le_nbour.text()))
        grid.addWidget(lbl_nbour, 6, 0)
        grid.addWidget(le_nbour, 6, 1, 1, 2)
        # ------------------------------------------------------------
        # ----------------- btns cancel/done -------------------------
        hbox_btns = QtGui.QHBoxLayout()
        btn_cancel = QtGui.QPushButton('cancel')
        btn_done = QtGui.QPushButton('done')
        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)
        hbox_btns.addStretch(1)
        hbox_btns.addWidget(btn_cancel)
        hbox_btns.addWidget(btn_done)
        grid.addLayout(hbox_btns, 7, 0, 1, 3)
        
    def do_cancel(self):
        """
        Close this SensorPopup, discarding all changes made in this pop-up.
        """
        self.close()

    def do_done(self):
        """
        Close this SensorPopup, saving all changes in the appropriate dictionaries and lists.
        """
        for key in self.parent_SensorLine.values.keys():
            self.parent_SensorLine.values[key] = self.copy_values[key]
        self.parent_SensorLine.edit_name()
        self.close()

    def set_sensor(self, s):
        """
        Read the Sensor-object from the pop-up's combo-box 
        and set the value in SensorPopup.copy_values accordingly.
        """
        s = str(s)
        self.copy_values['sensor'] = s
        self.update_sensor_tooltips(s)

    def update_sensor_tooltips(self, sensor_str):
        exec("from "
             + creator.sensor_dict[sensor_str].rpartition('/')[-1].partition('.py')[0]
             + " import " + sensor_str)
        exec("doc_str=" + sensor_str + ".__doc__")
        exec("doc_str_init=" + sensor_str + ".__init__.__doc__")

        if doc_str_init:
            doc_str_init = doc_str_init.lstrip().rstrip().replace('\n', '<br>')
        else:
            sorry = """<u>SORRY, NO DOCSTRING FOUND!</u><br>
But here's a list of the constructor function's parameters:<br>"""
            import inspect
            exec("l=inspect.getargspec(" + sensor_str + ".__init__)")
            for i in range(1, len(l.args)):
                arg = l.args[i]
                if i > len(l.args) - len(l.defaults):
                    arg = arg + " = " + str(l.defaults[i - (len(l.args) - len(l.defaults))])
                sorry = sorry + "<br>" + arg
            doc_str_init = sorry

        self.combo_sensor.setToolTip("Copy of docstring for class <u>"
                                     + sensor_str + "</u>:<br><br>" + doc_str)
        self.le_obj_args.setToolTip("Copy of docstring for constructor of <u>"
                                    + sensor_str + "</u>:<br><br>" + doc_str_init)

    def set_filter(self, s):
        """
        Read the filter-function from the pop-up's combo-box 
        and set the value in SensorPopup.copy_values accordingly.
        """
        self.copy_values['filter'] = s

    def set_value(self, key, value):
        """
        Assign a value to specified key in SensorPopup.copy_values.
        @param key Key to which the new value is to be assigned.
        @param value New value to assign to given key.
        """
        self.copy_values[key] = value
