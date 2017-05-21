## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 15.01.15

"""
@package CompoundPye.src.GUI.mdm_gui

This package contains the main-GUI-class Main_GUI. 
It is the frame for all of the GUI's tabs and editors.
"""

from PyQt4 import QtGui

import os
here = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
import pickle

from .ui_tabs import TabSystem, TabSurroundings, TabCircuit, TabSensors, TabOutput
from .styles import blue_tooltips


class Main_GUI(QtGui.QWidget):
    """
    MDM_GUI is QtGui.QWidget which serves as frame for all the smaller widgets 
    of the GUI (tabs and editors).
    It stores the values and parameters the user specified in the GUI. Most of 
    the values get saved as defaults for the next session, only circuits and 
    sensors need to be safed separately in text-files.
    """    
    def __init__(self, parent_RunGUI):
        """
        Initializes a MDM_GUI-object.
        @param parent_RunGUI Needs to be initiated with the parent 
        RunGUI-object which holds this MDM_GUI-object.
        """
        super(Main_GUI, self).__init__()
        
        try:
            with open(home+"/.CompoundPyeGUIdefault.pkl", 'rb') as f:
                self.values = pickle.load(f)
        except:
            with open(here + '/default_values.pkl', 'rb') as f:
                self.values = pickle.load(f)                    
        self.parent_RunGUI = parent_RunGUI
        self.initUI()

    def initUI(self):
        """
        Initializes the graphical Qt-objects of the GUI; this function is 
        called automatically when a new Main_GUI-object is initialized.
        """
        self.setStyleSheet(blue_tooltips)

        self.resize(1360, 720)
        self.center()
        self.setWindowTitle('ParameterGUI')
        self.setWindowIcon(QtGui.QIcon('/home/ikuhlemann/Downloads/Zombie.png'))
        
        self.tabs = QtGui.QTabWidget()

        ## holds all the tabs of the GUI.
        self.tab_list = [TabSystem(self), TabSurroundings(self),
                         TabCircuit(self), TabSensors(self), TabOutput(self)]
        self.tab_names = ['System', 'Surroundings', 'Circuit', 'Sensors', 'Output']
        for i in range(0, len(self.tab_list)):            
            self.tabs.addTab(self.tab_list[i], self.tab_names[i])
        hbox = QtGui.QHBoxLayout()        
        self.checkbox_show_neighbourhood_plot = QtGui.QCheckBox('show neighbourhood plot')
        if self.values['output']['show_neighbourhood_plot']:
            self.checkbox_show_neighbourhood_plot.toggle()
        btn_create_template = QtGui.QPushButton("create template")
        btn_create_template.clicked.connect(self.parent_RunGUI.create_template)
        self.checkbox_show_neighbourhood_plot.stateChanged.connect(self.toggle_show_neighbourhood_plot)        
        btn_apply = QtGui.QPushButton('apply')
        btn_apply.clicked.connect(self.parent_RunGUI.apply)

        run = QtGui.QPushButton('run')
        run.setToolTip('run the simulation with currently specified parameters')
        run.clicked.connect(self.parent_RunGUI.run)
    
        hbox.addStretch(1)
        hbox.addWidget(btn_create_template)
        hbox.addWidget(self.checkbox_show_neighbourhood_plot)
        hbox.addWidget(btn_apply)
        hbox.addWidget(run)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tabs)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def center(self):
        """
        Function to put the GUI's window at the center of 
        the screen (is called upon initialization).
        """
        qr = self.frameGeometry()        
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        """
        Pops up a dialog-window when the user wants to close the GUI's window.
        """
        with open(home + '/.CompoundPyeGUIdefault.pkl', 'wb') as f:
            pickle.dump(self.values, f, pickle.HIGHEST_PROTOCOL)
        reply = QtGui.QMessageBox.question(self,
                                           'Message',
                                           "Do you really want to quit? \n(Saved everything etc.?)",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def toggle_show_neighbourhood_plot(self):
        self.values['output']['show_neighbourhood_plot'] = self.checkbox_show_neighbourhood_plot.isChecked()
        print(self.values['output']['show_neighbourhood_plot'])
