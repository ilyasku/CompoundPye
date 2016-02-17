## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 15.01.15

"""
@package CompoundPye.src.GUI.ui_tabs

This package contains several QWidgets which are integrated into the main graphical user interface MotionDetectorModel.GUI.mdm_gui.MDM_GUI as tabs.
"""




from PyQt4 import QtGui


import circuit_editor as ce2

import sensor_editor as se

import stimuli_editor as stim




class TabOutput(QtGui.QWidget):
    """
    A tab (Widget) in which the user can specify the output parameters of the simulation.
    """
    

    def __init__(self,parent):
        """
        Initializes a TabOutput-object.

        @param parent Requires the parent MDM_GUI-object as parameter to access its dictionary in which all parameters are stored.
        """
        super(TabOutput,self).__init__()
        self.parent_GUI=parent
        #self.parent_GUI.values['output']={'dir':''}
        self.init_UI()

    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """
        vbox=QtGui.QVBoxLayout()
        self.setLayout(vbox)

        # ---------output dir-------------
        hbox_out=QtGui.QHBoxLayout()
        lbl_out=QtGui.QLabel('output directory')
        self.le_out=QtGui.QLineEdit()
        self.le_out.setText(self.parent_GUI.values['output']['dir'])
        self.le_out.editingFinished.connect(lambda: self.set_value('dir',self.le_out.text()))
        btn_browse=QtGui.QPushButton('browse')
        btn_browse.clicked.connect(self.choose_dir)

        hbox_out.addWidget(lbl_out)
        hbox_out.addWidget(self.le_out)
        hbox_out.addWidget(btn_browse)
        # --------------------------------
        
        # ------ line edits to specify which output to store ------

        hbox_n_by_index=QtGui.QHBoxLayout()
        lbl_n_by_index=QtGui.QLabel('indices of neurons of which to store the output\n(empty = all)')
        le_n_by_index=QtGui.QLineEdit()
        le_n_by_index.setText(self.parent_GUI.values['output']['n_by_index'])
        le_n_by_index.editingFinished.connect(lambda: self.set_value('n_by_index',le_n_by_index.text()))

        hbox_n_by_index.addWidget(lbl_n_by_index)
        hbox_n_by_index.addWidget(le_n_by_index)


        hbox_n_by_label=QtGui.QHBoxLayout()
        lbl_n_by_label=QtGui.QLabel('labels of neurons of which to store the output\n(empty = all)')
        le_n_by_label=QtGui.QLineEdit()
        le_n_by_label.setText(self.parent_GUI.values['output']['n_by_label'])
        le_n_by_label.editingFinished.connect(lambda: self.set_value('n_by_label',le_n_by_label.text()))

        hbox_n_by_label.addWidget(lbl_n_by_label)
        hbox_n_by_label.addWidget(le_n_by_label)

        hbox_s_by_index=QtGui.QHBoxLayout()
        
        lbl_s_by_index=QtGui.QLabel('indices of sensors of which to store the output\n(empty = all)')
        le_s_by_index=QtGui.QLineEdit()
        le_s_by_index.setText(self.parent_GUI.values['output']['s_by_index'])
        le_s_by_index.editingFinished.connect(lambda: self.set_value('s_by_index',le_s_by_index.text()))

        hbox_s_by_index.addWidget(lbl_s_by_index)
        hbox_s_by_index.addWidget(le_s_by_index)


        hbox_intensities_interval=QtGui.QHBoxLayout()
        lbl_intensities_interval=QtGui.QLabel("every x time steps the input intensities are stored;\nspecify x here")
        le_intensities_interval=QtGui.QLineEdit()
        le_intensities_interval.setText(self.parent_GUI.values['output']['intensities_interval'])
        le_intensities_interval.editingFinished.connect(lambda: self.set_value('intensities_interval',le_intensities_interval.text()))

        hbox_intensities_interval.addWidget(lbl_intensities_interval)
        hbox_intensities_interval.addWidget(le_intensities_interval)
        hbox_intensities_interval.addStretch(1)


        vbox.addLayout(hbox_out)
        vbox.addLayout(hbox_n_by_index)
        vbox.addLayout(hbox_n_by_label)
        vbox.addLayout(hbox_s_by_index)
        vbox.addLayout(hbox_intensities_interval)



        vbox.addStretch(1)

    def set_value(self,key,value):
        """
        Sets the value for the given key in the parent GUI's values-dictionary.
        @param key Key of the value that is to be changed.
        @param value New value for the given key.
        """
        self.parent_GUI.values['output'][key]=value

    def choose_dir(self):
        """
        Calls a file dialog to let the user specify an output directory.
        """
        path=QtGui.QFileDialog.getExistingDirectory(self,'select output directory',self.parent_GUI.values['output']['dir'])
        self.set_value('dir',path)
        self.le_out.setText(path)

class TabSystem(QtGui.QWidget):
    """
    A tab (Widget) in which the user can specify several system-parameters.
    """
    def __init__(self,parent):
        """
        Initializes a TabSystem-object.
        @param parent Requires the parent MDM_GUI-object as parameter to access its dictionary in which all parameters are stored.
        """
        super(TabSystem,self).__init__()
        self.parent_GUI=parent
        self.count=0
        self.initUI()


    def initUI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """

        
        #------ button test ------------------
        '''
        btn=QtGui.QPushButton('Buttonbrot')
        btn.setToolTip('clixclixclixme!')
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.count_up)

        self.lbl=QtGui.QLabel(str(self.count))
        
        
        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(btn)
        hbox.addWidget(self.lbl)
        
        frame=QtGui.QFrame()
        frame.setLayout(hbox)
        frame.setStyleSheet("background-color: rgb(0,0,0); margin:5px; border:1px solid rgb(255, 255, 255); ")
        '''
        #-------------------------------------
        
        hbox_grid=QtGui.QHBoxLayout()
        grid=QtGui.QGridLayout()
        hbox_grid.addLayout(grid)
        hbox_grid.addStretch(1)

        #----------------- dt --------------------
        lbl_dt=QtGui.QLabel('time step dt =')
        line_edit_dt=QtGui.QLineEdit()
        lbl_s0=QtGui.QLabel('s')

        line_edit_dt.setText(str(self.parent_GUI.values['system_values']['dt']))

        line_edit_dt.editingFinished.connect(lambda: self.set_value('dt',float(line_edit_dt.text())))

        grid.addWidget(lbl_dt,0,0)
        grid.addWidget(line_edit_dt,0,1)
        grid.addWidget(lbl_s0,0,2)

        #----------------------------------------------

        #---------------- relaxation time --------
        lbl_relax=QtGui.QLabel('relaxation time =')
        line_edit_relax=QtGui.QLineEdit()
        lbl_s1=QtGui.QLabel('s')
        
        line_edit_relax.setText(str(self.parent_GUI.values['system_values']['relaxation_time']))

        line_edit_relax.editingFinished.connect(lambda: self.set_value('relaxation_time',float(line_edit_relax.text())))

        grid.addWidget(lbl_relax,1,0)
        grid.addWidget(line_edit_relax,1,1)
        grid.addWidget(lbl_s1,1,2)

        #----------------------------------------------

        #--------------- relaxation intensity ---------

        lbl_int=QtGui.QLabel('relaxation intensity =')
        line_edit_int=QtGui.QLineEdit()
        lbl_s2=QtGui.QLabel('s')
        
        line_edit_int.setText(str(self.parent_GUI.values['system_values']['relaxation_intensity']))

        line_edit_int.editingFinished.connect(lambda: self.set_value('relaxation_intensity',float(line_edit_int.text())))
        grid.addWidget(lbl_int,2,0)
        grid.addWidget(line_edit_int,2,1)
        grid.addWidget(lbl_s2,2,2)
        

        #----------------------------------------------

        #-------------relax calculation type ----------

        lbl_relax_type=QtGui.QLabel('relax calculation type')
        combo=QtGui.QComboBox()
        combo.addItem('simple_photoreceptor')
        combo.addItem('none')
        combo.addItem('normal')
        index=combo.findText(self.parent_GUI.values['system_values']['relax_calculation'])
        combo.setCurrentIndex(index)

        combo.activated[str].connect(self.read_combo)

        grid.addWidget(lbl_relax_type,3,0)
        grid.addWidget(combo,3,1,1,2)

        #----------------------------------------------


        # ----------- simulation time -----------------

        lbl_sim_time=QtGui.QLabel('simulation time')
        le_sim_time=QtGui.QLineEdit()
        le_sim_time.setText(self.parent_GUI.values['system_values']['sim_time'])
        lbl_unit=QtGui.QLabel('s')

        grid.addWidget(lbl_sim_time,4,0)
        grid.addWidget(le_sim_time,4,1)
        grid.addWidget(lbl_unit,4,2)

        le_sim_time.editingFinished.connect(lambda: self.set_value('sim_time',le_sim_time.text()))

        # ---------------------------------------------

        vbox=QtGui.QVBoxLayout()
        #vbox.addWidget(frame)
        vbox.addLayout(hbox_grid)
        vbox.addStretch(1)

        self.setLayout(vbox)


    '''
    def count_up(self):
        self.count+=1
        #self.statusBar().showMessage(str(self.count))
        self.lbl.setText(str(self.count))
        #self.lbl.move(max(150,np.random.random()*self.frameGeometry().width()),50)
    '''

    def read_combo(self,s):
        """
        Set the type for the initial relaxation calculations as selected by the user in the provided combo-box.
        @param s String that is shown as text on the combo-box-widget.
        """
        self.parent_GUI.values['system_values']['relax_calculation']=s


    def set_value(self,value_key,value):
        """
        Change a value in the parent GUI's values-dictionary.
        @param value_key Key in the value-dictionary that receives a new value.
        @param value New value for specified key.
        """
        self.parent_GUI.values['system_values'][value_key]=value
        
class TabSurroundings(QtGui.QWidget):
    """
    A tab (Widget) in which the user can specify several surroundings-parameters (dimension, size in pixel, etc.).
    """
    
    def __init__(self,parent):
        """
        Initializes a TabSurroundings-object.
        @param parent Requires the parent MDM_GUI-object as parameter to access its dictionary in which all parameters are stored.
        """
        super(TabSurroundings, self).__init__()
        self.parent_GUI=parent
        self.initUI()

    def initUI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """
        label=QtGui.QLabel('surroundings')
        
        combo=QtGui.QComboBox()
        #combo.addItem('choose ...')
        combo.addItem('one dimensional array')
        combo.addItem('two dimensional array')
        combo.addItem('video input')

        combo.activated[str].connect(self.read_combo)

        #self.parent_GUI.values['surroundings_values']['current_selected']='two dimensional array'

        

        self.current_combo_str=self.parent_GUI.values['surroundings_values']['current_selected']
        
        index=combo.findText(self.current_combo_str)
        combo.setCurrentIndex(index)

        btn_surroundings_trafo=QtGui.QPushButton("set properties of 2D projection")

        btn_surroundings_trafo.clicked.connect(self.create_projection_pop_up)

        radio_deg=QtGui.QRadioButton("spatial values in degree",self)
        radio_fraction=QtGui.QRadioButton("spatial values in fraction of shown surroundings",self)

        radio_deg.toggled.connect(lambda: self.set_spatial_unit("degree"))
        radio_fraction.toggled.connect(lambda: self.set_spatial_unit("fraction"))

        if self.parent_GUI.values['surroundings_values']['spatial_unit']=='degree':
            radio_deg.toggle()
        else:
            radio_fraction.toggle()

        self.grid=QtGui.QGridLayout()

        self.grid.addWidget(radio_deg,1,3,1,2)
        self.grid.addWidget(radio_fraction,2,3,1,2)

        self.surr_param_hbox=QtGui.QHBoxLayout()

        
        self.setLayout(self.grid)

        self.grid.addWidget(label,0,0)
        self.grid.addWidget(combo,0,1)

        self.grid.addWidget(btn_surroundings_trafo,0,3)

        self.grid.addLayout(self.surr_param_hbox,1,0,1,2)

        self.stimuli_widget=stim.StimuliWidget(self)
        
        self.grid.addWidget(self.stimuli_widget,3,0,5,5)

        init_str=self.current_combo_str
        self.current_combo_str='dummy str for UI initialization'

        self.read_combo(init_str)


    def set_spatial_unit(self,unit):
        if unit!=self.parent_GUI.values['surroundings_values']['spatial_unit']:
            if unit=="fraction" or unit=="degree":
                self.parent_GUI.values['surroundings_values']['spatial_unit']=unit
                
                convert=QtGui.QMessageBox.question(self,"convert units", 
                                                   "You changed the spatial unit to "+unit+". Do you want to convert spatial parameters (of stimuli) accordingly?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

                if convert==QtGui.QMessageBox.Yes:
                    self.convert_units(unit)
                else:
                    pass
                
        
    def convert_units(self,unit):
        surr_dict=self.parent_GUI.values['surroundings_values']
        stim_dict=surr_dict['stimuli']
        if unit=="degree":
            def convert(axis,old):
                new=old*(surr_dict['projection_values'][axis][1]-surr_dict['projection_values'][axis][0])+surr_dict['projection_values'][axis][0]
                return new
        elif unit=="fraction":
            def convert(axis,old):
                new=(old-surr_dict['projection_values'][axis][0])/(surr_dict['projection_values'][axis][1]-surr_dict['projection_values'][axis][0])
                return new
        #for stim in stim_dict:
            #stim_dict[stim]
            

    def read_combo(self,combo_str):
        """
        Reads the combo-box specifying the dimension (or video) of the surroundings and sets the widgets accordingly.
        """
        self.parent_GUI.values['surroundings_values']['current_selected']=combo_str
        if combo_str=='two dimensional array':
            if self.current_combo_str!=combo_str:
                clearLayout(self.surr_param_hbox)

                self.current_combo_str=combo_str
                self.parent_GUI.values['surroundings_values']['current_selected']=combo_str
                lbl=QtGui.QLabel('size of the surroundings in pixel:')
                lblx=QtGui.QLabel('x')
                font = QtGui.QFont()
                font.setWeight(30)
                lblx.setFont(font)

                line_edit1=QtGui.QLineEdit()
                line_edit2=QtGui.QLineEdit()

                line_edit1.setText(str(self.parent_GUI.values['surroundings_values']['px_x']))
                line_edit2.setText(str(self.parent_GUI.values['surroundings_values']['px_y']))

                self.surr_param_hbox.addWidget(lbl)
                self.surr_param_hbox.addWidget(line_edit1)
                self.surr_param_hbox.addWidget(lblx)
                self.surr_param_hbox.addWidget(line_edit2)
                self.surr_param_hbox.addStretch(1)

                line_edit1.editingFinished.connect(lambda: self.set_value('px_x',int(line_edit1.text())))
                line_edit2.editingFinished.connect(lambda: self.set_value('px_y',int(line_edit2.text())))
            else:
                pass

        elif combo_str=='one dimensional array':
            if self.current_combo_str!=combo_str:
                clearLayout(self.surr_param_hbox)

                self.current_combo_str=combo_str
                lbl=QtGui.QLabel('size of the surroundings in pixel:')
                line_edit=QtGui.QLineEdit()
                line_edit.setFrame(True)
                line_edit.setText(str(self.parent_GUI.values['surroundings_values']['px_x']))
                

                self.surr_param_hbox.addWidget(lbl)
                self.surr_param_hbox.addWidget(line_edit)
                self.surr_param_hbox.addStretch(1)


                line_edit.editingFinished.connect(lambda: self.set_value('px_x',int(line_edit.text())))
            else:
                pass

        elif combo_str=='video input':
            if self.current_combo_str!=combo_str:
                clearLayout(self.surr_param_hbox)

                self.video_file=''

                self.current_combo_str=combo_str

                grid=QtGui.QGridLayout()
                self.surr_param_hbox.addLayout(grid)

                lbl=QtGui.QLabel('path to file:')
                self.line_edit_video_file=QtGui.QLineEdit()
                self.line_edit_video_file.setText(self.parent_GUI.values['surroundings_values']['input_video'])
                browse=QtGui.QPushButton('browse')

                grid.addWidget(lbl,0,0,1,1)
                grid.addWidget(self.line_edit_video_file,0,1,1,5)
                grid.addWidget(browse,0,6,1,1)

                lbl_start=QtGui.QLabel('start at')
                video_start_t=QtGui.QLineEdit()
                lbl_unit1=QtGui.QLabel('s')
                lbl_unit2=QtGui.QLabel('s')

                lbl_end=QtGui.QLabel(';  end at')
                video_end_t=QtGui.QLineEdit()

                grid.addWidget(lbl_start,1,0)
                grid.addWidget(video_start_t,1,1)
                grid.addWidget(lbl_unit1,1,2)
                grid.addWidget(lbl_end,1,3)
                grid.addWidget(video_end_t,1,4)
                grid.addWidget(lbl_unit2,1,5)


                browse.clicked.connect(self.file_dialog)
                self.line_edit_video_file.editingFinished.connect(lambda: self.set_value('input_video',self.line_edit_video_file.text()))


        

            else:
                pass
        # @todo some error/exception-handling here?
        else:
            pass

        self.stimuli_widget.set_widget(self.current_combo_str)

    def set_value(self,value_key,value):
        """
        Sets the value for the given key in the parent GUI's values-dictionary.
        @param value_key Key of the value that is to be changed.
        @param value New value for the given key.
        """
        self.parent_GUI.values['surroundings_values'][value_key]=value



    def create_projection_pop_up(self):
        self.projection_pop_up=ProjectionPopup(self)
        self.projection_pop_up.show()


    def file_dialog(self):
        """
        Pops up a file dialog for the user to select a video input-file.
        """
        self.video_file = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        self.line_edit_video_file.setText(self.video_file)



class ProjectionPopup(QtGui.QWidget):
    
    def __init__(self,parent_surr_tab):
        super(ProjectionPopup,self).__init__()
        self.parent_surr_tab=parent_surr_tab
        self.copy_values=self.parent_surr_tab.parent_GUI.values['surroundings_values']['projection_values'].copy()
        self.init_UI()

    def init_UI(self):
        vbox=QtGui.QVBoxLayout()
        self.setLayout(vbox)


        hbox_description=QtGui.QHBoxLayout()

        description_te=QtGui.QTextEdit()
        description_te.setReadOnly(True)
        description_te.setHtml("Set which fraction of the agents' surroundings will be simulated. <br>This is important for spatial properties of the stimuli and the photoreceptors' receptive fields.<br>Specify horizontal angle <b>phi</b> in range <b>[-180,180]</b>,<br>and <b>theta</b> in range <b>[0,180]</b>.")

        #hbox_description.setMargin(100)

        #description_te.setFixedHeight(description_te.document().size().height())
        description_te.setFixedHeight(100)
        #description_te.setMinimumHeight(description_te.document().size().height())

        pal=QtGui.QPalette()
        #bgc=QtGui.QColor(255,255,255)
        bgc=self.palette().color(QtGui.QPalette.Window)
        pal.setColor(QtGui.QPalette.Base,bgc)
        textc=QtGui.QColor(0,0,0)
        pal.setColor(QtGui.QPalette.Text,textc)
        description_te.setPalette(pal)

        hbox_description.addWidget(description_te)
        vbox.addLayout(hbox_description)

        hbox_horizontal=QtGui.QHBoxLayout()

        horizontal_lbl=QtGui.QLabel("horizontal fraction")
        phi_min_lbl=QtGui.QLabel("phi_min=")
        phi_max_lbl=QtGui.QLabel("phi_max=")
        phi_min_line_edit=QtGui.QLineEdit(str(self.copy_values['horizontal'][0]))
        phi_max_line_edit=QtGui.QLineEdit(str(self.copy_values['horizontal'][1]))

        phi_min_line_edit.editingFinished.connect(lambda: self.set_value('horizontal',0,float(phi_min_line_edit.text())))
        phi_max_line_edit.editingFinished.connect(lambda: self.set_value('horizontal',1,float(phi_max_line_edit.text())))

        hbox_horizontal.addWidget(horizontal_lbl)
        hbox_horizontal.addWidget(phi_min_lbl)
        hbox_horizontal.addWidget(phi_min_line_edit)
        hbox_horizontal.addWidget(phi_max_lbl)
        hbox_horizontal.addWidget(phi_max_line_edit)
        
        vbox.addLayout(hbox_horizontal)

        hbox_vertical=QtGui.QHBoxLayout()

        vertical_lbl=QtGui.QLabel("vertical fraction")
        theta_min_lbl=QtGui.QLabel("theta_min=")
        theta_max_lbl=QtGui.QLabel("theta_max=")
        theta_min_line_edit=QtGui.QLineEdit(str(self.copy_values['vertical'][0]))
        theta_max_line_edit=QtGui.QLineEdit(str(self.copy_values['vertical'][1]))

        theta_min_line_edit.editingFinished.connect(lambda: self.set_value('vertical',0,float(theta_min_line_edit.text())))
        theta_max_line_edit.editingFinished.connect(lambda: self.set_value('vertical',1,float(theta_max_line_edit.text())))

        hbox_vertical.addWidget(vertical_lbl)
        hbox_vertical.addWidget(theta_min_lbl)
        hbox_vertical.addWidget(theta_min_line_edit)
        hbox_vertical.addWidget(theta_max_lbl)
        hbox_vertical.addWidget(theta_max_line_edit)
        
        vbox.addLayout(hbox_vertical)

        hbox_buttons=QtGui.QHBoxLayout()

        btn_cancel=QtGui.QPushButton("cancel")
        btn_done=QtGui.QPushButton("done")

        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)

        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_cancel)
        hbox_buttons.addWidget(btn_done)

        vbox.addLayout(hbox_buttons)
        

    def set_value(self,key,index,value):
        self.copy_values[key][index]=value
        

    def do_cancel(self):
        self.close()

    def do_done(self):
        for key in self.copy_values.keys():
            self.parent_surr_tab.parent_GUI.values['surroundings_values']['projection_values'][key]=self.copy_values[key]
        self.close()

class TabCircuit(QtGui.QWidget):
    """
    A tab (Widget) in which the user can add components and connections between components and specify several circuit-parameters.
    """
    def __init__(self,parent):
        """
        Initializes a TabCircuit-object.
        @param parent Requires the parent MDM_GUI-object as parameter to access its dictionary in which all parameters are stored.
        """
        super(TabCircuit,self).__init__()
        self.parent_UI=parent
        self.initUI()

    def initUI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """

        load=QtGui.QPushButton('load')
        load.setToolTip('Load circuit from file')
        load.resize(load.sizeHint())
        load.clicked.connect(self.do_load)



        save=QtGui.QPushButton('save')
        save.setToolTip('Write circuit to file')
        save.resize(save.sizeHint())
        save.clicked.connect(self.do_save)


        

        #appl=QtGui.QPushButton('apply')
        #appl.setToolTip('Apply changes to the circuit now\n(because it can take a few minutes and already start in the background)')
        #appl.resize(appl.sizeHint())


        self.editor=ce2.EditorTabs()

        self.grid=QtGui.QGridLayout()
        self.setLayout(self.grid)

        self.grid.addWidget(load,0,0)
        self.grid.addWidget(save,1,0)
        
        #self.grid.addWidget(appl,2,0)

        self.grid.addWidget(self.editor,0,1,9,5)

    def do_load(self):
        """
        Pops up a file dialog for the user to load a circuit-file (text-file).
        """
        f = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self.parent_UI.values['circuit_values']['last_file'])
        if f:
            self.parent_UI.values['circuit_values']['last_file']=f

        old_editor=self.grid.takeAt(self.grid.count()-1)
        old_editor.widget().deleteLater()

        self.editor=ce2.EditorTabs(f)
        self.grid.addWidget(self.editor,0,1,9,5)

    def do_save(self):
        """
        Pops up a file dialog for the user to save the current content of the editor to a circuit-file (text-file).
        """
        f = QtGui.QFileDialog.getSaveFileName(self, 'save file',self.parent_UI.values['circuit_values']['last_file'])

        if f:
            self.parent_UI.values['circuit_values']['last_file']=f
        
        self.editor.save_file(f)


class TabSensors(QtGui.QWidget):
    """
    A tab (Widget) in which the user can add sensors and specify several sensor-parameters.
    """
    
    def __init__(self,parent_UI):
        """
        Initializes a TabCircuit-object.
        @param parent Requires the parent MDM_GUI-object as parameter to access its dictionary in which all parameters are stored.
        """

        super(TabSensors,self).__init__()
        self.parent_UI=parent_UI
        self.init_UI()

    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """

        vbox=QtGui.QVBoxLayout()
        self.editor=se.EditorWidget(self)
        vbox.addWidget(self.editor)
        self.setLayout(vbox)


# ---------------------------------------------------------------------------------------------------
##### COPIED FROM: http://stackoverflow.com/questions/9374063/pyqt4-remove-widgets-and-layout-as-well 
##### USER: Avaris
##### DATE OF POST: Feb 21 '12 at 9:45
def clearLayout(layout):
    """
    Removes and deletes all widgets from given layout.

##### COPIED FROM: http://stackoverflow.com/questions/9374063/pyqt4-remove-widgets-and-layout-as-well 
##### USER: Avaris
##### DATE OF POST: Feb 21 '12 at 9:45    
    @param layout Layout that is to be cleared.
    """
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)

        if isinstance(item, QtGui.QWidgetItem):
            #print "widget" + str(item)
            item.widget().close()
            # or
            # item.widget().setParent(None)
        elif isinstance(item, QtGui.QSpacerItem):
            pass
            #print "spacer " + str(item)
            # no need to do extra stuff
        else:
            #print "layout " + str(item)
            clearLayout(item.layout())

        # remove the item from layout
        layout.removeItem(item)   
# ---------------------------------------------------------------------------------------------------
