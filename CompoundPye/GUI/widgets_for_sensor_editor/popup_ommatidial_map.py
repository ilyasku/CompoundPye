from PyQt4 import QtGui

import os
home = os.path.expanduser("~")


class PopupOmmatidialMap(QtGui.QWidget):
    
    def __init__(self, parent_EditorWidget):
        
        super(PopupOmmatidialMap, self).__init__()

        self.parent_EditorWidget = parent_EditorWidget

        self.phi = self.parent_EditorWidget.parent_Tab.parent_UI.values['surroundings_values']['projection_values']['horizontal'][:]
        self.theta = self.parent_EditorWidget.parent_Tab.parent_UI.values['surroundings_values']['projection_values']['vertical'][:]
        self.animal = self.parent_EditorWidget.parent_Tab.parent_UI.values['animal']
        self.copy_values = self.parent_EditorWidget.parent_Tab.parent_UI.values['sensor_values']['ommatidia'].copy()

        self.init_UI()

    def init_UI(self):        
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)        
        checkbox_use_surroundings_values = QtGui.QCheckBox("use values from surroundings "
                                                           + "settings\n(values can't be "
                                                           + "edited unless you turn this off)")
        checkbox_use_surroundings_values.stateChanged.connect(self.do_toggle_use_values)
        self.use_surroundings_values = False
        vbox.addWidget(checkbox_use_surroundings_values)
        hbox_phi = QtGui.QHBoxLayout()        
        lbl_phi_min = QtGui.QLabel("phi_min")
        self.le_phi_min = QtGui.QLineEdit()
        self.le_phi_min.setText(str(self.phi[0]))
        self.le_phi_min.editingFinished.connect(
            lambda: self.set_phi_min(float(self.le_phi_min.text())))

        lbl_phi_max = QtGui.QLabel("phi_max")
        self.le_phi_max = QtGui.QLineEdit()
        self.le_phi_max.setText(str(self.phi[1]))
        self.le_phi_max.editingFinished.connect(
            lambda: self.set_phi_max(float(self.le_phi_max.text())))
        
        hbox_phi.addWidget(lbl_phi_min)
        hbox_phi.addWidget(self.le_phi_min)
        hbox_phi.addWidget(lbl_phi_max)
        hbox_phi.addWidget(self.le_phi_max)
        
        vbox.addLayout(hbox_phi)

        hbox_theta = QtGui.QHBoxLayout()
        
        lbl_theta_min = QtGui.QLabel("theta_min")
        self.le_theta_min = QtGui.QLineEdit()
        self.le_theta_min.setText(str(self.theta[0]))
        self.le_theta_min.editingFinished.connect(
            lambda: self.set_theta_min(float(self.le_theta_min.text())))

        lbl_theta_max = QtGui.QLabel("theta_max")
        self.le_theta_max = QtGui.QLineEdit()
        self.le_theta_max.setText(str(self.theta[1]))
        self.le_theta_max.editingFinished.connect(
            lambda: self.set_theta_max(float(self.le_theta_max.text())))
        
        hbox_theta.addWidget(lbl_theta_min)
        hbox_theta.addWidget(self.le_theta_min)
        hbox_theta.addWidget(lbl_theta_max)
        hbox_theta.addWidget(self.le_theta_max)
        
        vbox.addLayout(hbox_theta)

        hbox_border = QtGui.QHBoxLayout()
        
        lbl_border = QtGui.QLabel("border")
        self.le_border = QtGui.QLineEdit()
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
        
        radio_left = QtGui.QRadioButton("use left eye (phi around range [0,180])")

        radio_right = QtGui.QRadioButton("use right eye (phi around range [-180,0])")
        
        radio_both = QtGui.QRadioButton("use both eyes")

        self.button_group_eye.addButton(radio_left)
        self.button_group_eye.addButton(radio_right)
        self.button_group_eye.addButton(radio_both)

        if self.copy_values['eyes'] == 'left':
            radio_left.toggle()
        elif self.copy_values['eyes'] == 'right':
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
        
        radio_droso = QtGui.QRadioButton("Drosophila")

        ## exclude calliphora for now ... ommatidial data not prepared yet
        # radio_calli=QtGui.QRadioButton("Calliphora")
        
        radio_bee = QtGui.QRadioButton("Apis mellifera")

        self.button_group_animal.addButton(radio_droso)
        # self.button_group_animal.addButton(radio_calli)
        self.button_group_animal.addButton(radio_bee)

        if self.animal == 'droso':
            radio_droso.toggle()
        # elif self.animal == 'calli':
        # radio_calli.toggle()
        else:
            radio_bee.toggle()

        radio_droso.toggled.connect(lambda: self.set_animal('droso'))
        # radio_calli.toggled.connect(lambda: self.set_animal('calli'))
        radio_bee.toggled.connect(lambda: self.set_animal('bee'))

        vbox_animal.addWidget(radio_droso)
        # vbox_animal.addWidget(radio_calli)
        vbox_animal.addWidget(radio_bee)
        
        #########################################
        #       buttons cancel/create           #
        #########################################        
        hbox_buttons = QtGui.QHBoxLayout()

        btn_cancel = QtGui.QPushButton("cancel")
        btn_create = QtGui.QPushButton("create")
        
        btn_cancel.clicked.connect(self.do_cancel)
        btn_create.clicked.connect(self.do_create)
        
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_cancel)
        hbox_buttons.addWidget(btn_create)

        vbox.addLayout(hbox_buttons)

    def set_animal(self, animal):
        self.animal = animal
        
    def set_left(self):
        self.copy_values['eyes'] = 'left'

    def set_right(self):
        self.copy_values['eyes'] = 'right'

    def set_both(self):
        self.copy_values['eyes'] = 'both'

    def set_border(self, value):
        self.copy_values['border'] = value
        
    def set_phi_min(self, value):
        self.phi[0] = value
        
    def set_phi_max(self, value):
        self.phi[1] = value
                
    def set_theta_min(self, value):
        self.theta[0] = value
        
    def set_theta_max(self, value):
        self.theta[1] = value
        
    def do_toggle_use_values(self):

        if self.use_surroundings_values:
            self.use_surroundings_values = False
            self.le_phi_min.setReadOnly(False)
            self.le_phi_max.setReadOnly(False)
            self.le_theta_min.setReadOnly(False)
            self.le_theta_max.setReadOnly(False)            
        else:
            self.use_surroundings_values = True 
            self.le_phi_min.setReadOnly(True)
            self.le_phi_max.setReadOnly(True)
            self.le_theta_min.setReadOnly(True)
            self.le_theta_max.setReadOnly(True)

            self.phi = self.parent_EditorWidget.parent_Tab.parent_UI.values['surroundings_values']['projection_values']['horizontal'][:]
            self.theta = self.parent_EditorWidget.parent_Tab.parent_UI.values['surroundings_values']['projection_values']['vertical'][:]
       
            self.le_phi_min.setText(str(self.phi[0]))
            self.le_phi_max.setText(str(self.phi[1]))

            self.le_theta_min.setText(str(self.theta[0]))
            self.le_theta_max.setText(str(self.theta[1]))

    def do_cancel(self):
        self.close()

    def do_create(self):        
        from ...OmmatidialMap import read_ommatidia
        import numpy as np

        s = read_ommatidia.write_sphere_coords_spheric_to_sensor_file_buffer(
            np.array(self.phi) * np.pi / 180.,
            np.array(self.theta) * np.pi / 180.,
            self.copy_values['border'], self.copy_values['eyes'],
            animal=self.animal)

        f = open(home + "/.tmp_ommatidial_map.txt", 'w')
        f.write(s)
        f.close()

        self.parent_EditorWidget.load_tmp_ommatidial_map_file()

        os.system("rm " + home + "/.tmp_ommatidial_map.txt")

        self.parent_EditorWidget.parent_Tab.parent_UI.values['sensor_values']['ommatidia'] = self.copy_values
        self.parent_EditorWidget.parent_Tab.parent_UI.values['animal'] = self.animal
        self.close()
