## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 15.01.15

"""
@package CompoundPye.src.GUI.sensor_editor

This package provides a graphical editor for the user to add/remove/edit sensors 
(interface between surroundings and the circuit of neurons, 
sensors are considered as part of Circuit-objects, though).
"""

from PyQt4 import QtCore,QtGui

from ..Parser import *
from .styles import *

import os
#here=os.path.dirname(os.path.abspath(__file__))
home=os.path.expanduser("~")


dict_of_sensors=creator.sensor_dict
list_of_filters=['gaussian','pixel']

class EditorWidget(QtGui.QWidget):
    """
    The main or frame widget of the graphical sensor-editor.
    """
    def __init__(self,parent_Tab):
        """
        Initializes an 'EditorWidget'-object.
        """
        super(EditorWidget,self).__init__()

        #self.last_file=''
        self.parent_Tab=parent_Tab


        self.init_UI()
        
    def init_UI(self):
        """
        Initializes all widgets (labels, buttons, etc) displayed on this EditorWidget.
        """
        
        self.main_layout=QtGui.QGridLayout()
        self.setLayout(self.main_layout)
        
        
        btn_load=QtGui.QPushButton('load')
        btn_save=QtGui.QPushButton('save')
        
        btn_load.clicked.connect(self.do_load)
        btn_save.clicked.connect(self.do_save)
        btn_load.setToolTip("Load sensor set-up from file.")
        btn_save.setToolTip("Save sensor set-up to file.")

        btn_OmmatidialMap=QtGui.QPushButton('create photoreceptors\nusing ommatidial map')
        btn_OmmatidialMap.clicked.connect(self.do_create_ommatidial_map)
        btn_OmmatidialMap.setToolTip("Create snesors using the predefined ommatidial map.")

        checkbox_neighbourhood_manually=QtGui.QCheckBox('determine neighbour-\nhood automatically')
        checkbox_neighbourhood_manually.stateChanged.connect(self.do_toggle_neighbourhood_mode)
        checkbox_neighbourhood_manually.setToolTip("If not checked, you will have to define \nmanually which sensors will count as neighbours.")

        layout_range=QtGui.QHBoxLayout()

        self.lbl_range=QtGui.QLabel('range')
        self.range_line=QtGui.QLineEdit()
        self.range_line.setText(str(self.parent_Tab.parent_UI.values['sensor_values']['neighbourhood_range']))
        self.range_line.editingFinished.connect(lambda: self.set_value('neighbourhood_range',float(self.range_line.text())))
        s_range=self.range_line.sizeHint()
        s_range.setWidth(int(s_range.width()*0.7))
        self.range_line.setFixedSize(s_range)
    
        self.range_line.setToolTip("Maximum range in which sensors can count as neighbours.\nRange in relative extend of surroundings.")
        
        layout_range.addWidget(self.lbl_range)
        layout_range.addWidget(self.range_line,alignment=QtCore.Qt.AlignLeft)
        

        layout_max_n=QtGui.QHBoxLayout()

        self.lbl_max_n=QtGui.QLabel('max.\nneighbours')
        self.max_n_line=QtGui.QLineEdit()
        self.max_n_line.setText(str(self.parent_Tab.parent_UI.values['sensor_values']['max_neighbours']))
        self.max_n_line.editingFinished.connect(lambda: self.set_value('max_neighbours',int(self.max_n_line.text())))
        s_max=self.max_n_line.sizeHint()
        s_max.setWidth(int(s_max.width()*0.7))
        self.max_n_line.setFixedSize(s_max)

        self.max_n_line.setToolTip("Maximum number of neighbours per 'direction'.\nDirections are currently fixed at roughly left, right, up, down ...")

        layout_max_n.addWidget(self.lbl_max_n)
        layout_max_n.addWidget(self.max_n_line,alignment=QtCore.Qt.AlignLeft)
        

        if self.parent_Tab.parent_UI.values['sensor_values']['neighbourhood_manually']==False:
            checkbox_neighbourhood_manually.toggle()
            self.show_neighbourhood_QWidgets(True)
        else:
            self.show_neighbourhood_QWidgets(True)
        

        
        self.main_layout.addWidget(btn_load,0,0,1,1)
        self.main_layout.addWidget(btn_save,1,0,1,1)
        self.main_layout.addWidget(btn_OmmatidialMap,2,0,1,1)
        self.main_layout.addWidget(checkbox_neighbourhood_manually,4,0,1,1)
        #self.main_layout.addWidget(self.lbl_range,4,0)
        #self.main_layout.addWidget(self.range_line,4,1)
        self.main_layout.addLayout(layout_range,5,0)
        #self.main_layout.addWidget(self.lbl_max_n,5,0)
        #self.main_layout.addWidget(self.max_n_line,5,1)
        self.main_layout.addLayout(layout_max_n,6,0)
                
        self.editor=EditorScrollArea(self)
        
        self.main_layout.addWidget(self.editor,0,2,9,6)
        
    def show_neighbourhood_QWidgets(self,state):
        if state==False:
            self.lbl_range.setHidden(True)
            self.range_line.setHidden(True)
            self.lbl_max_n.setHidden(True)
            self.max_n_line.setHidden(True)

        else:
            self.lbl_range.setHidden(False)
            self.range_line.setHidden(False)
            self.lbl_max_n.setHidden(False)
            self.max_n_line.setHidden(False)
        
        

    def set_value(self,key,value):
        self.parent_Tab.parent_UI.values['sensor_values'][key]=value


    def do_toggle_neighbourhood_mode(self,state):
        """
        Toggle neighbourhood mode to determine neighbours automatically or manually.
        """
        if state:
            self.parent_Tab.parent_UI.values['sensor_values']['neighbourhood_manually']=False
            
        else:
            self.parent_Tab.parent_UI.values['sensor_values']['neighbourhood_manually']=True

        self.show_neighbourhood_QWidgets(state)

    def do_create_ommatidial_map(self):
        self.popup_omma_map=PopupOmmatidialMap(self)
        self.popup_omma_map.show()

    def load_tmp_ommatidial_map_file(self):

        f=home+"/.tmp_ommatidial_map.txt"
         
        old_editor=self.main_layout.takeAt(self.main_layout.count()-1) 
        old_editor.widget().deleteLater()

        self.editor=EditorScrollArea(self,f)
        self.main_layout.addWidget(self.editor,0,1,9,6)
       

    def do_load(self):
        """
        Load sensors from a sensor-file (text-file).
        
        Pops up a file-dialog to select a file to load. Kills the old EditorScrollArea contained in this EditorWidget and sets up a new one containing the loaded sensors.
        """

        f = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self.parent_Tab.parent_UI.values['sensor_values']['last_file'])
        #print 'f='+f
        if f:
            self.parent_Tab.parent_UI.values['sensor_values']['last_file']=f
        
        old_editor=self.main_layout.takeAt(self.main_layout.count()-1) 
        old_editor.widget().deleteLater()

        self.editor=EditorScrollArea(self,f)
        self.main_layout.addWidget(self.editor,0,1,9,6)
    
    def do_save(self):
        """
        Save sensors to a sensor-file (text-file).

        Pops up a file-dialog to select a destination file. Saves all sensors currently shown in the editor widget.
        """
        fname=QtGui.QFileDialog.getSaveFileName(self, 'save file',self.parent_Tab.parent_UI.values['sensor_values']['last_file'])
        if fname:
            self.parent_Tab.parent_UI.values['sensor_values']['last_file']=fname
        self.editor.do_save(fname)
        
        
class EditorScrollArea(QtGui.QScrollArea):
    """
    This ScrollArea is the actual editor window in which the user can add/remove sensors and click on a sensor's button to edit its properties.
    """
    def __init__(self,parent_EditorWidget,initial_file=None):
        """
        Initializes an EditorScrollArea.
        @param parent_EditorWidget Requires the parent EditorWidget (or rather a pointer to it) which serves as frame for this EditorScrollArea as input, to access its variables.
        @param initial_file Can be initialized with a path to a sensor-file (text-file).
        """
        super(EditorScrollArea,self).__init__()
        
        self.n_sensors=0
        
        self.sensors=[]
        
        self.SensorLines=[]

        self.parent_EW=parent_EditorWidget
        
        self.init_UI(initial_file)
        
    def init_UI(self,initial_file):
        """
        Sets up all the widgets (graphical stuff like buttons, labels, etc.) displayed in this EditorScrollArea.
        """
        self.setWidgetResizable(True)

        w=QtGui.QWidget()

        self.setWidget(w)

        if initial_file==None:
            self.settings,self.variables,self.defaults,sensors={'neighbours':'x'},{},{},[]
        else:
            sensors=[]
            self.settings,self.variables,self.defaults,s=self.do_load(initial_file)
            # adding and removing widgets will be easier with a list than a dictionary --> put name inside dict
            for key in list(s.keys()):
                new_dict=s[key]
                new_dict['name']=key
                sensors.append(new_dict)
        
        #print 'sensors:'
        #print sensors
        
        self.vbox=QtGui.QVBoxLayout()
        w.setLayout(self.vbox)
        
        hbox_btn=QtGui.QHBoxLayout()
        
        btn_add=QtGui.QPushButton('add sensor')
        btn_add.clicked.connect(self.do_add_sensor)
        
        hbox_btn.addWidget(btn_add)
        hbox_btn.addStretch(1)
        
        self.vbox.addLayout(hbox_btn)
        self.vbox.addStretch(1)
        
        
        
        for s_i in sensors:
            self.add_sensor(s_i)
    
    def add_sensor(self,initial_values=None):
        """
        Adds a sensor ('SensorLine'-widget) to this EditorScrollArea and the sensor's values to this EditorScrollArea.sensor list.
        @param initial_values The new 'SensorLine'-widget can be initialized with a dictionary of sensor-values.
        """
        new_sline=SensorLine(self,self.n_sensors,initial_values)
        self.vbox.insertWidget(len(self.sensors),new_sline)
        self.sensors.append(new_sline.values)
        self.n_sensors+=1
        self.SensorLines.append(new_sline)
    
    def do_add_sensor(self):
        """
        Adds a new ('SensorLine'-widget) to this EditorScrollArea and default sensor values to the list EditorScrollArea.sensor.
        """
        new_sline=SensorLine(self,self.n_sensors)
        self.vbox.insertWidget(len(self.sensors),new_sline)
        self.sensors.append(new_sline.values)
        self.n_sensors+=1
        self.SensorLines.append(new_sline)
    
    def do_load(self,fname):
        """
        Load a sensor-file (text-file).
        @param fname Path to file to load.
        """
        return sp.parse_file(fname)

    def do_remove(self,index):
        """
        Remove the 'SensorLine'-widget with given index from the EditorScrollArea.
        @param index Index of the 'SensorLine'-widget to be removed.
        """
        item=self.vbox.itemAt(index)
        self.vbox.removeItem(item)
        self.sensors.pop(index)
        self.SensorLines.pop(index)
        self.n_sensors=self.n_sensors-1
        item.widget().close()

        for i in range(0,len(self.sensors)):
            self.SensorLines[i].index=i

    def do_save(self,fname):
        """
        Save the sensors currently shown on the EditorScrollArea to a sensor-file.
        @param fname Path to target file.
        """
        sp.save_file(fname,self.settings,self.variables,self.defaults,self.sensors)
        
        
class SensorLine(QtGui.QWidget):
    """
    A line representing a sensor in the editor window (EditorScrollArea), containing a button showing the sensor's label and a remove-button.
    """
    def __init__(self,parent_ScrollArea,index,initial_values=None):
        """
        Initializes a 'SensorLine'-widget.
        @param parent_ScrollArea Requires the parent EditorScrollArea (or rather a pointer to it) as input to access its variables (lists of all sensors and their values, etc.).
        @param index Index of this'SensorLine'-widget in the parent EditorScrollArea's layout.
        @param initial_values Can be initialized with a dictionary of sensor-values.
        """
        super(SensorLine,self).__init__()
        self.parent_SA=parent_ScrollArea
        
        self.index=index

        if initial_values==None:
            self.values={'name':'new sensor '+str(len(self.parent_SA.sensors)),'filter':'gaussian','filter_args':'[1,1]','neighbourhood':'-','obj_args':'-','sensor':'Sensor','x':'0.0','y':'0.0'}
            
        else:
            self.values=initial_values
            
        
        
        self.init_UI()
        
        
    def init_UI(self):
        """
        Set up all the widgets (labels, buttons, etc.) displayed on this SensorLine.
        """

        grid=QtGui.QGridLayout()
        self.setLayout(grid)

        self.btn_sensor=QtGui.QPushButton(self.values['name'])
        btn_remove=QtGui.QPushButton('remove')
        
        self.btn_sensor.clicked.connect(self.do_popup)
        btn_remove.clicked.connect(self.remove)

        grid.addWidget(self.btn_sensor,0,0)
        grid.addWidget(btn_remove,0,1)

        
    def edit_name(self):
        """
        Read the name of the sensor from the values-dictionary and set the label of its button accordingly.
        """
        self.btn_sensor.setText(self.values['name'])
        
    def do_popup(self):
        """
        Pop up a 'SensorPopup'-widget to edit this sensor's values.
        """
        self.popup=SensorPopup(self)
        self.popup.show()

    def remove(self):
        """
        Remove this SensorLine from the parent EditorScrollArea.
        """
        self.parent_SA.do_remove(self.index)
        
        
        
class SensorPopup(QtGui.QWidget):
    """
    A (pop-up) widget in which the user can edit the properties of a sensor.
    """
    def __init__(self,parent_SensorLine):
        """
        Initializes a SensorPopup.
        @param parent_SensorLine Requires the parent SensorLine of the sensor this pop-up belongs to, to access its values-dictionary.
        """
        super(SensorPopup,self).__init__()

        self.parent_SensorLine=parent_SensorLine
        
        self.copy_values=self.parent_SensorLine.values.copy()

        self.init_UI()

    def init_UI(self):
        """
        Initializes all widgets (labels, buttons, etc.) displayed on this SensorPopup.
        """

        self.setStyleSheet(blue_tooltips)

        grid=QtGui.QGridLayout()
        self.setLayout(grid)

        # ------------- name --------------------------------------

        lbl_name=QtGui.QLabel('name')
        self.le_name=QtGui.QLineEdit()
        self.le_name.setText(self.copy_values['name'])
        self.le_name.editingFinished.connect(lambda: self.set_value('name',self.le_name.text()))
        
        grid.addWidget(lbl_name,0,0)
        grid.addWidget(self.le_name,0,1,1,2)

        # ---------------------------------------------------------

        # ------------------- sensor object -----------------------

        lbl_sensor=QtGui.QLabel('sensor object')
        self.combo_sensor=QtGui.QComboBox()
        for s in list(dict_of_sensors.keys()):
            self.combo_sensor.addItem(s)
        index=self.combo_sensor.findText(self.copy_values['sensor'])
        self.combo_sensor.setCurrentIndex(index)
        self.combo_sensor.activated[str].connect(self.set_sensor)

        grid.addWidget(lbl_sensor,1,0)
        grid.addWidget(self.combo_sensor,1,1,1,2)
        # ---------------------------------------------------------
        # ------------------ object args --------------------------
        
        lbl_obj_args=QtGui.QLabel('object arguments')
        self.le_obj_args=QtGui.QLineEdit()
        self.le_obj_args.setText(self.copy_values['obj_args'])
        self.le_obj_args.editingFinished.connect(lambda: self.set_value('obj_args',self.le_obj_args.text()))

        grid.addWidget(lbl_obj_args,2,0)
        grid.addWidget(self.le_obj_args,2,1,1,2)
        # ---------------------------------------------------------
        self.update_sensor_tooltips(self.copy_values['sensor'])


        # --------------------- filter ----------------------------
        lbl_filter=QtGui.QLabel('filter')
        combo_filter=QtGui.QComboBox()
        for f in list_of_filters:
            combo_filter.addItem(f)
        index=combo_filter.findText(self.copy_values['filter'])
        combo_filter.setCurrentIndex(index)
        combo_filter.activated[str].connect(self.set_filter)

        grid.addWidget(lbl_filter,3,0)
        grid.addWidget(combo_filter,3,1,1,2)
        # ---------------------------------------------------------


        # -------------------- filter args ------------------------
        lbl_f_args=QtGui.QLabel('filter arguments\n(comma separated, keywords possible\ndon\'t use empty spaces!)')
        self.le_f_args=QtGui.QLineEdit()
        self.le_f_args.setText(self.copy_values['filter_args'])
        self.le_f_args.editingFinished.connect(lambda: self.set_value('filter_args',self.le_f_args.text()))

        grid.addWidget(lbl_f_args,4,0)
        grid.addWidget(self.le_f_args,4,1,1,2)
        # ---------------------------------------------------------

        # ------------------- postition ---------------------------

        lbl_pos=QtGui.QLabel('position')
        le_x=QtGui.QLineEdit()
        le_y=QtGui.QLineEdit()

        le_x.setText(self.copy_values['x'])
        le_y.setText(self.copy_values['y'])
        
        le_x.setToolTip('x-coordinate\n(in relative width)')
        le_y.setToolTip('y-coordinate\n(in relative height)')
        

        le_x.editingFinished.connect(lambda: self.set_value('x',le_x.text()))
        le_y.editingFinished.connect(lambda: self.set_value('y',le_y.text()))

        grid.addWidget(lbl_pos,5,0)
        grid.addWidget(le_x,5,1)
        grid.addWidget(le_y,5,2)
        
        # ---------------- neighbourhood ----------------------------

        lbl_nbour=QtGui.QLabel('neighbourhood')
        le_nbour=QtGui.QLineEdit()
        le_nbour.setText(self.copy_values['neighbourhood'])
        le_nbour.editingFinished.connect(lambda: self.set_value('neighbourhood',le_nbour.text()))

        grid.addWidget(lbl_nbour,6,0)
        grid.addWidget(le_nbour,6,1,1,2)

        # ------------------------------------------------------------

        # ----------------- btns cancel/done -------------------------

        hbox_btns=QtGui.QHBoxLayout()

        btn_cancel=QtGui.QPushButton('cancel')
        btn_done=QtGui.QPushButton('done')

        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)

        hbox_btns.addStretch(1)
        hbox_btns.addWidget(btn_cancel)
        hbox_btns.addWidget(btn_done)

        grid.addLayout(hbox_btns,7,0,1,3)
        
    def do_cancel(self):
        """
        Close this SensorPopup, discarding all changes made in this pop-up.
        """
        self.close()

    def do_done(self):
        """
        Close this SensorPopup, saving all changes in the appropriate dictionaries and lists.
        """
        for key in list(self.parent_SensorLine.values.keys()):
            self.parent_SensorLine.values[key]=self.copy_values[key]
        self.parent_SensorLine.edit_name()
        self.close()


    def set_sensor(self,s):
        """
        Read the Sensor-object from the pop-up's combo-box and set the value in SensorPopup.copy_values accordingly.
        """
        s=str(s)
        self.copy_values['sensor']=s
        self.update_sensor_tooltips(s)

    def update_sensor_tooltips(self,sensor_str):
        exec("from "+creator.sensor_dict[sensor_str].rpartition('/')[-1].partition('.py')[0]+ " import "+sensor_str)
        exec("doc_str="+sensor_str+".__doc__")
        exec("doc_str_init="+sensor_str+".__init__.__doc__")

        if doc_str_init:
            doc_str_init=doc_str_init.lstrip().rstrip().replace('\n','<br>')
        else:
            sorry="""<u>SORRY, NO DOCSTRING FOUND!</u><br>
But here's a list of the constructor function's parameters:<br>"""
            import inspect
            exec("l=inspect.getargspec("+sensor_str+".__init__)")
            for i in range(1,len(l.args)):
                arg=l.args[i]
                if i>len(l.args)-len(l.defaults):
                    arg=arg+" = "+str(l.defaults[i-(len(l.args)-len(l.defaults))])
                sorry=sorry+"<br>"+arg
            doc_str_init=sorry


        self.combo_sensor.setToolTip("Copy of docstring for class <u>"+sensor_str+"</u>:<br><br>"+doc_str)
        self.le_obj_args.setToolTip("Copy of docstring for constructor of <u>"+sensor_str+"</u>:<br><br>"+doc_str_init)


    def set_filter(self,s):
        """
        Read the filter-function from the pop-up's combo-box and set the value in SensorPopup.copy_values accordingly.
        """
        self.copy_values['filter']=s

    def set_value(self,key,value):
        """
        Assign a value to specified key in SensorPopup.copy_values.
        @param key Key to which the new value is to be assigned.
        @param value New value to assign to given key.
        """
        self.copy_values[key]=value



class PopupOmmatidialMap(QtGui.QWidget):

    def __init__(self,parent_EditorWidget):
        
        super(PopupOmmatidialMap,self).__init__()

        self.parent_EditorWidget=parent_EditorWidget

        self.phi=self.parent_EditorWidget.parent_Tab.parent_UI.values['surroundings_values']['projection_values']['horizontal'][:]
        self.theta=self.parent_EditorWidget.parent_Tab.parent_UI.values['surroundings_values']['projection_values']['vertical'][:]

        self.animal = self.parent_EditorWidget.parent_Tab.parent_UI.values['animal']

        self.copy_values=self.parent_EditorWidget.parent_Tab.parent_UI.values['sensor_values']['ommatidia'].copy()

        #self.border=[0.0,0.0,0.0,0.0] #left,right,bottom,top

        self.init_UI()

    def init_UI(self):
        
        vbox=QtGui.QVBoxLayout()
        self.setLayout(vbox)
        
        checkbox_use_surroundings_values=QtGui.QCheckBox("use values from surroundings settings\n(values can't be edited unless you turn this off)")
        checkbox_use_surroundings_values.stateChanged.connect(self.do_toggle_use_values)
        self.use_surroundings_values=False
        vbox.addWidget(checkbox_use_surroundings_values)

        hbox_phi=QtGui.QHBoxLayout()
        
        lbl_phi_min=QtGui.QLabel("phi_min")
        self.le_phi_min=QtGui.QLineEdit()
        self.le_phi_min.setText(str(self.phi[0]))
        self.le_phi_min.editingFinished.connect(lambda: self.set_phi_min(float(self.le_phi_min.text())))

        lbl_phi_max=QtGui.QLabel("phi_max")
        self.le_phi_max=QtGui.QLineEdit()
        self.le_phi_max.setText(str(self.phi[1]))
        self.le_phi_max.editingFinished.connect(lambda: self.set_phi_max(float(self.le_phi_max.text())))
        
        hbox_phi.addWidget(lbl_phi_min)
        hbox_phi.addWidget(self.le_phi_min)
        hbox_phi.addWidget(lbl_phi_max)
        hbox_phi.addWidget(self.le_phi_max)
        
        vbox.addLayout(hbox_phi)

        hbox_theta=QtGui.QHBoxLayout()
        
        lbl_theta_min=QtGui.QLabel("theta_min")
        self.le_theta_min=QtGui.QLineEdit()
        self.le_theta_min.setText(str(self.theta[0]))
        self.le_theta_min.editingFinished.connect(lambda: self.set_theta_min(float(self.le_theta_min.text())))

        lbl_theta_max=QtGui.QLabel("theta_max")
        self.le_theta_max=QtGui.QLineEdit()
        self.le_theta_max.setText(str(self.theta[1]))
        self.le_theta_max.editingFinished.connect(lambda: self.set_theta_max(float(self.le_theta_max.text())))
        
        hbox_theta.addWidget(lbl_theta_min)
        hbox_theta.addWidget(self.le_theta_min)
        hbox_theta.addWidget(lbl_theta_max)
        hbox_theta.addWidget(self.le_theta_max)
        
        vbox.addLayout(hbox_theta)

        hbox_border=QtGui.QHBoxLayout()
        
        lbl_border=QtGui.QLabel("border")
        self.le_border=QtGui.QLineEdit()
        self.le_border.setText(str(self.copy_values['border']))
        self.le_border.editingFinished.connect(lambda: self.set_border(self.le_border.text()))

        hbox_border.addStretch(1)
        hbox_border.addWidget(lbl_border)
        hbox_border.addWidget(self.le_border)
        hbox_border.addStretch(1)
        
        vbox.addLayout(hbox_border)
        
        checkbox_use_surroundings_values.toggle()


        #########################################
        # > some radio buttons                  #
        #########################################
        hbox_radio_buttons = QtGui.QHBoxLayout()
        vbox.addLayout(hbox_radio_buttons)

        #########################################
        # >>      select eye (left/right/both)  #
        #########################################
        group_box_eye = QtGui.QGroupBox("select eye")
        hbox_radio_buttons.addWidget(group_box_eye)

        vbox_eye = QtGui.QVBoxLayout()
        group_box_eye.setLayout(vbox_eye)

        self.button_group_eye = QtGui.QButtonGroup(self)
        
        radio_left=QtGui.QRadioButton("use left eye (phi around range [0,180])")

        radio_right=QtGui.QRadioButton("use right eye (phi around range [-180,0])")
        
        radio_both=QtGui.QRadioButton("use both eyes")

        self.button_group_eye.addButton(radio_left)
        self.button_group_eye.addButton(radio_right)
        self.button_group_eye.addButton(radio_both)

        if self.copy_values['eyes']=='left':
            radio_left.toggle()
        elif self.copy_values['eyes']=='right':
            radio_right.toggle()
        else:
            radio_both.toggle()

        radio_left.toggled.connect(self.set_left)
        radio_right.toggled.connect(self.set_right)
        radio_both.toggled.connect(self.set_both)

        vbox_eye.addWidget(radio_left)
        vbox_eye.addWidget(radio_right)
        vbox_eye.addWidget(radio_both)

        #########################################
        # >>  select animal (droso/calli/bee)   #
        #########################################

        group_box_animal = QtGui.QGroupBox("select animal")
        hbox_radio_buttons.addWidget(group_box_animal)

        vbox_animal = QtGui.QVBoxLayout()
        group_box_animal.setLayout(vbox_animal)

        self.button_group_animal = QtGui.QButtonGroup(self)
        
        radio_droso=QtGui.QRadioButton("Drosophila")

        ## exclude calliphora for now ... ommatidial data not prepared yet
        #radio_calli=QtGui.QRadioButton("Calliphora")
        
        radio_bee=QtGui.QRadioButton("Apis mellifera")

        self.button_group_animal.addButton(radio_droso)
        #self.button_group_animal.addButton(radio_calli)
        self.button_group_animal.addButton(radio_bee)

 
        if self.animal=='droso':
            radio_droso.toggle()
        #elif self.animal == 'calli':
        #radio_calli.toggle()
        else:
            radio_bee.toggle()

        radio_droso.toggled.connect(lambda: self.set_animal('droso'))
        #radio_calli.toggled.connect(lambda: self.set_animal('calli'))
        radio_bee.toggled.connect(lambda: self.set_animal('bee'))

        vbox_animal.addWidget(radio_droso)
        #vbox_animal.addWidget(radio_calli)
        vbox_animal.addWidget(radio_bee)

        
        #########################################
        #       buttons cancel/create           #
        #########################################
        
        hbox_buttons=QtGui.QHBoxLayout()

        btn_cancel=QtGui.QPushButton("cancel")
        btn_create=QtGui.QPushButton("create")
        
        btn_cancel.clicked.connect(self.do_cancel)
        btn_create.clicked.connect(self.do_create)
        
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_cancel)
        hbox_buttons.addWidget(btn_create)

        vbox.addLayout(hbox_buttons)

    def set_animal(self, animal):
        self.animal = animal
        
    def set_left(self):
        self.copy_values['eyes']='left'

    def set_right(self):
        self.copy_values['eyes']='right'

    def set_both(self):
        self.copy_values['eyes']='both'

    def set_border(self,value):
        self.copy_values['border']=value
        #print self.copy_values['border']

    def set_phi_min(self,value):
        self.phi[0]=value
        #print self.phi

    def set_phi_max(self,value):
        self.phi[1]=value
        #print self.phi
        
    def set_theta_min(self,value):
        self.theta[0]=value
        #print self.theta

    def set_theta_max(self,value):
        self.theta[1]=value
        #print self.theta

    def do_toggle_use_values(self):

        if self.use_surroundings_values:
            self.use_surroundings_values=False
            self.le_phi_min.setReadOnly(False)
            self.le_phi_max.setReadOnly(False)
            self.le_theta_min.setReadOnly(False)
            self.le_theta_max.setReadOnly(False)
            
        else:
            self.use_surroundings_values=True 
            self.le_phi_min.setReadOnly(True)
            self.le_phi_max.setReadOnly(True)
            self.le_theta_min.setReadOnly(True)
            self.le_theta_max.setReadOnly(True)

            self.phi=self.parent_EditorWidget.parent_Tab.parent_UI.values['surroundings_values']['projection_values']['horizontal'][:]
            self.theta=self.parent_EditorWidget.parent_Tab.parent_UI.values['surroundings_values']['projection_values']['vertical'][:]

       
            self.le_phi_min.setText(str(self.phi[0]))
            self.le_phi_max.setText(str(self.phi[1]))

            self.le_theta_min.setText(str(self.theta[0]))
            self.le_theta_max.setText(str(self.theta[1]))


    def do_cancel(self):
        self.close()

    def do_create(self):
        
        from ..OmmatidialMap import read_ommatidia
        import numpy as np

        s=read_ommatidia.write_sphere_coords_spheric_to_sensor_file_buffer(np.array(self.phi)*np.pi/180.,np.array(self.theta)*np.pi/180.,self.copy_values['border'],self.copy_values['eyes'], animal = self.animal)

        f=open(home+"/.tmp_ommatidial_map.txt",'w')
        f.write(s)
        f.close()

        self.parent_EditorWidget.load_tmp_ommatidial_map_file()

        os.system("rm "+home+"/.tmp_ommatidial_map.txt")

        self.parent_EditorWidget.parent_Tab.parent_UI.values['sensor_values']['ommatidia']=self.copy_values
        self.parent_EditorWidget.parent_Tab.parent_UI.values['animal'] = self.animal

        self.close()

