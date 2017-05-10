## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 08.05.2017

"""
@package CompoundPye.src.GUI.sensor_editor

This package provides a graphical editor for the user to add/remove/edit sensors 
(interface between surroundings and the circuit of neurons, 
sensors are considered as part of Circuit-objects, though).
"""

from PyQt4 import QtCore, QtGui

from ..Parser import creator
from widgets_for_sensor_editor.popup_ommatidial_map import PopupOmmatidialMap
from widgets_for_sensor_editor.editor_scroll_area import EditorScrollArea

import os
home = os.path.expanduser("~")

dict_of_sensors = creator.sensor_dict
list_of_filters = ['gaussian', 'pixel']


class EditorWidget(QtGui.QWidget):
    """
    The main or frame widget of the graphical sensor-editor.
    """
    def __init__(self, parent_Tab):
        """
        Initializes an 'EditorWidget'-object.
        """
        super(EditorWidget, self).__init__()
        self.parent_Tab = parent_Tab
        self.init_UI()
        
    def init_UI(self):
        """
        Initializes all widgets (labels, buttons, etc) displayed on this EditorWidget.
        """
        
        self.main_layout = QtGui.QGridLayout()
        self.setLayout(self.main_layout)        
        
        btn_load = QtGui.QPushButton('load')
        btn_save = QtGui.QPushButton('save')
        
        btn_load.clicked.connect(self.do_load)
        btn_save.clicked.connect(self.do_save)
        btn_load.setToolTip("Load sensor set-up from file.")
        btn_save.setToolTip("Save sensor set-up to file.")

        btn_OmmatidialMap = QtGui.QPushButton('create photoreceptors\nusing ommatidial map')
        btn_OmmatidialMap.clicked.connect(self.do_create_ommatidial_map)
        btn_OmmatidialMap.setToolTip("Create snesors using the predefined ommatidial map.")

        checkbox_neighbourhood_manually = QtGui.QCheckBox("determine neighbour-"
                                                          + "\nhood automatically")
        checkbox_neighbourhood_manually.stateChanged.connect(self.do_toggle_neighbourhood_mode)
        checkbox_neighbourhood_manually.setToolTip("If not checked, you will have to define"
                                                   + " \nmanually which sensors "
                                                   + "will count as neighbours.")

        layout_range = QtGui.QHBoxLayout()

        self.lbl_range = QtGui.QLabel('range')
        self.range_line = QtGui.QLineEdit()
        self.range_line.setText(str(
            self.parent_Tab.parent_UI.values['sensor_values']['neighbourhood_range']))
        self.range_line.editingFinished.connect(
            lambda: self.set_value('neighbourhood_range', float(self.range_line.text())))
        s_range = self.range_line.sizeHint()
        s_range.setWidth(int(s_range.width() * 0.7))
        self.range_line.setFixedSize(s_range)
    
        self.range_line.setToolTip("Maximum range in which sensors can"
                                   + " count as neighbours.\nRange in "
                                   + "relative extend of surroundings.")
        
        layout_range.addWidget(self.lbl_range)
        layout_range.addWidget(self.range_line, alignment=QtCore.Qt.AlignLeft)
        
        layout_max_n = QtGui.QHBoxLayout()

        self.lbl_max_n = QtGui.QLabel('max.\nneighbours')
        self.max_n_line = QtGui.QLineEdit()
        self.max_n_line.setText(str(
            self.parent_Tab.parent_UI.values['sensor_values']['max_neighbours']))
        self.max_n_line.editingFinished.connect(
            lambda: self.set_value('max_neighbours', int(self.max_n_line.text())))
        s_max = self.max_n_line.sizeHint()
        s_max.setWidth(int(s_max.width() * 0.7))
        self.max_n_line.setFixedSize(s_max)

        self.max_n_line.setToolTip("Maximum number of neighbours per "
                                   + "'direction'.\nDirections are currently"
                                   + " fixed at roughly left, right, up, down ...")

        layout_max_n.addWidget(self.lbl_max_n)
        layout_max_n.addWidget(self.max_n_line, alignment=QtCore.Qt.AlignLeft)
        
        if self.parent_Tab.parent_UI.values['sensor_values']['neighbourhood_manually'] is False:
            checkbox_neighbourhood_manually.toggle()
            self.show_neighbourhood_QWidgets(True)
        else:
            self.show_neighbourhood_QWidgets(True)        
        
        self.main_layout.addWidget(btn_load, 0, 0, 1, 1)
        self.main_layout.addWidget(btn_save, 1, 0, 1, 1)
        self.main_layout.addWidget(btn_OmmatidialMap, 2, 0, 1, 1)
        self.main_layout.addWidget(checkbox_neighbourhood_manually, 4, 0, 1, 1)
        self.main_layout.addLayout(layout_range, 5, 0)
        self.main_layout.addLayout(layout_max_n, 6, 0)                
        self.editor = EditorScrollArea(self)        
        self.main_layout.addWidget(self.editor, 0, 2, 9, 6)
        
    def show_neighbourhood_QWidgets(self, state):
        if state is False:
            self.lbl_range.setHidden(True)
            self.range_line.setHidden(True)
            self.lbl_max_n.setHidden(True)
            self.max_n_line.setHidden(True)
        else:
            self.lbl_range.setHidden(False)
            self.range_line.setHidden(False)
            self.lbl_max_n.setHidden(False)
            self.max_n_line.setHidden(False)
                
    def set_value(self, key, value):
        self.parent_Tab.parent_UI.values['sensor_values'][key] = value

    def do_toggle_neighbourhood_mode(self, state):
        """
        Toggle neighbourhood mode to determine neighbours automatically or manually.
        """
        if state:
            self.parent_Tab.parent_UI.values['sensor_values']['neighbourhood_manually'] = False            
        else:
            self.parent_Tab.parent_UI.values['sensor_values']['neighbourhood_manually'] = True
        self.show_neighbourhood_QWidgets(state)

    def do_create_ommatidial_map(self):
        self.popup_omma_map = PopupOmmatidialMap(self)
        self.popup_omma_map.show()

    def load_tmp_ommatidial_map_file(self):
        f = home + "/.tmp_ommatidial_map.txt"
         
        old_editor = self.main_layout.takeAt(self.main_layout.count() - 1) 
        old_editor.widget().deleteLater()
        self.editor = EditorScrollArea(self, f)
        self.main_layout.addWidget(self.editor, 0, 1, 9, 6)
       
    def do_load(self):
        """
        Load sensors from a sensor-file (text-file).
        
        Pops up a file-dialog to select a file to load. Kills the old EditorScrollArea 
        contained in this EditorWidget and sets up a new one containing the loaded sensors.
        """
        f = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                              self.parent_Tab.parent_UI.values[
                                                  'sensor_values']['last_file'])
        if f:
            self.parent_Tab.parent_UI.values['sensor_values']['last_file'] = f        
        old_editor = self.main_layout.takeAt(self.main_layout.count() - 1) 
        old_editor.widget().deleteLater()
        self.editor = EditorScrollArea(self, f)
        self.main_layout.addWidget(self.editor, 0, 1, 9, 6)
    
    def do_save(self):
        """
        Save sensors to a sensor-file (text-file).

        Pops up a file-dialog to select a destination file. 
        Saves all sensors currently shown in the editor widget.
        """
        fname = QtGui.QFileDialog.getSaveFileName(
            self, 'save file',
            self.parent_Tab.parent_UI.values['sensor_values']['last_file'])
        if fname:
            self.parent_Tab.parent_UI.values['sensor_values']['last_file'] = fname
        self.editor.do_save(fname)        
