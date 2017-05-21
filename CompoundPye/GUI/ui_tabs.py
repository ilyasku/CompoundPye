## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 15.01.15

"""
@package CompoundPye.src.GUI.ui_tabs

This package contains several QWidgets which are integrated into the main 
graphical user interface MotionDetectorModel.GUI.mdm_gui.MDM_GUI as tabs.
"""

from PyQt4 import QtGui

from . import circuit_editor as ce2

from . import sensor_editor as se

from . import stimuli_editor as stim

from . import help_widget


import os
here = os.path.dirname(os.path.abspath(__file__))


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

        for w in [lbl_out,self.le_out]:
            w.setToolTip("""Set where to save the output.
Either type the (absolute) path here, or use the 'browse' button to the right.""")
        btn_browse.setToolTip("""Use file browser to specify output path.""")
        
        # --------------------------------
        
        # ------ line edits to specify which output to store ------

        hbox_n_by_index=QtGui.QHBoxLayout()
        lbl_n_by_index=QtGui.QLabel('indices of neurons of which to store the output\n(empty = all)')
        le_n_by_index=QtGui.QLineEdit()
        le_n_by_index.setText(self.parent_GUI.values['output']['n_by_index'])
        le_n_by_index.editingFinished.connect(lambda: self.set_value('n_by_index',le_n_by_index.text()))

        for w in [lbl_n_by_index,le_n_by_index]:
            w.setToolTip("""In Python syntax, specify a list of neuron indices, of which you want to store the output.<br>
With the exception of very small simulations, it will be very hard to figure out which indices are assigned to neurons.<br>
Thus, a more comfortable way might be to use the next row, where you can specify by name of which neurons you want to store the output.<br>
On the other hand, that might result in a huge amount of data, e.g. if you specify a neuron type that is present in each column (and if you have a few hundred columns).<br><br>
<u>example:</u> [0,1,12,13,14]""")

        hbox_n_by_index.addWidget(lbl_n_by_index)
        hbox_n_by_index.addWidget(le_n_by_index)


        hbox_n_by_label=QtGui.QHBoxLayout()
        lbl_n_by_label=QtGui.QLabel('labels of neurons of which to store the output\n(empty = all)')
        le_n_by_label=QtGui.QLineEdit()
        le_n_by_label.setText(self.parent_GUI.values['output']['n_by_label'])
        le_n_by_label.editingFinished.connect(lambda: self.set_value('n_by_label',le_n_by_label.text()))

        for w in [lbl_n_by_label,le_n_by_label]:
            w.setToolTip("""In Python syntax, specify a list of neuron labels, of which you want to store the output.<br>
BEWARE: This might result in a huge amount of data, e.g. if you specify a neuron type that is present in each column (and if you have a few hundred columns).<br><br>
<u>example:</u> ['HS','T4','T5']""")

        hbox_n_by_label.addWidget(lbl_n_by_label)
        hbox_n_by_label.addWidget(le_n_by_label)

        hbox_s_by_index=QtGui.QHBoxLayout()
        
        lbl_s_by_index=QtGui.QLabel('indices of sensors of which to store the output\n(empty = all)')
        le_s_by_index=QtGui.QLineEdit()
        le_s_by_index.setText(self.parent_GUI.values['output']['s_by_index'])
        le_s_by_index.editingFinished.connect(lambda: self.set_value('s_by_index',le_s_by_index.text()))

        for w in [lbl_s_by_index,le_s_by_index]:
            w.setToolTip("""In Python syntax, specify a list of sensor indices, of which you want to store the output.<br><br>
            <u>example:</u> [0,1,5]""")

        hbox_s_by_index.addWidget(lbl_s_by_index)
        hbox_s_by_index.addWidget(le_s_by_index)


        hbox_intensities_interval=QtGui.QHBoxLayout()
        lbl_intensities_interval=QtGui.QLabel("every x time steps the input intensities are stored;\nspecify x here")
        le_intensities_interval=QtGui.QLineEdit()
        le_intensities_interval.setText(self.parent_GUI.values['output']['intensities_interval'])
        le_intensities_interval.editingFinished.connect(lambda: self.set_value('intensities_interval',le_intensities_interval.text()))

        for w in [lbl_intensities_interval,le_intensities_interval]:
            w.setToolTip("""Intensities of surroundings is only stored every x steps.<br>
This is only for you to check whether the intensities look as you wanted them to.<br>
Specify integer x here.<br><br>
<u>example:</u> 3000""")

        hbox_intensities_interval.addWidget(lbl_intensities_interval)
        hbox_intensities_interval.addWidget(le_intensities_interval)
        hbox_intensities_interval.addStretch(1)


        vbox.addLayout(hbox_out)
        vbox.addLayout(hbox_n_by_index)
        vbox.addLayout(hbox_n_by_label)
        vbox.addLayout(hbox_s_by_index)
        vbox.addLayout(hbox_intensities_interval)



        vbox.addStretch(1)


        # ------ HELP buttons -----------
        hw=help_widget.HelpWidget(here+'/help_texts/tab_output.html',"https://github.com/ilyasku/CompoundPye/wiki/GUI#output")
        vbox.addWidget(hw)



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

        
        #line_edit_dt.setToolTip('I test tool <span style="color: white"> tips</span>, <b> yo</b> !')
        #lbl_dt.setToolTip('non-fancy')

        line_edit_dt.setText(str(self.parent_GUI.values['system_values']['dt']))

        line_edit_dt.editingFinished.connect(lambda: self.set_value('dt',float(line_edit_dt.text())))

        grid.addWidget(lbl_dt,0,0)
        grid.addWidget(line_edit_dt,0,1)
        grid.addWidget(lbl_s0,0,2)

        for w in [lbl_dt,line_edit_dt,lbl_s0]:
            w.setToolTip("""<b>Set time step of the simulation.</b>""")


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

        for w in  [lbl_relax,line_edit_relax,lbl_s1]:
            w.setToolTip("""<b>Set duration of relaxation prior to the actual simulation.<br>
Depending on the selcted relaxation type, this might be very similar <br>
to running an actual simulation, but with static stimuli. <br>
If time and disk space allows for it, I would recommend <br>
to forgo relaxation and instead increase simulation time.</b>""")


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

        for w in [lbl_int,line_edit_int,lbl_s2]:
            w.setToolTip("<b>In case you run a simulation, specify intensity shown to all sensors here.</b>")
        

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

        for w in [lbl_relax_type,combo]:
            w.setToolTip("""<b>Select type of relaxation calculation.<br>
<u>simple_photoreceptor</u>: use one receptor for relexation calculation (using relaxation intensity), apply same values to all photoreceptors afterwards (fast).<br>
<u>none</u>: skip relaxation.<br>
<u>normal</u>: run relaxation for all photoreceptors, using static surroundings (slow).</b>""")
        #----------------------------------------------


        # ----------- simulation time -----------------

        lbl_sim_time=QtGui.QLabel('simulation time')
        le_sim_time=QtGui.QLineEdit()
        le_sim_time.setText(self.parent_GUI.values['system_values']['sim_time'])
        lbl_unit=QtGui.QLabel('s')

        grid.addWidget(lbl_sim_time,4,0)
        grid.addWidget(le_sim_time,4,1)
        grid.addWidget(lbl_unit,4,2)

        for w in [lbl_sim_time,le_sim_time,lbl_unit]:
            w.setToolTip("""<b>Specify time span to be simulated.</b>""")


        le_sim_time.editingFinished.connect(lambda: self.set_value('sim_time',le_sim_time.text()))

        # ---------------------------------------------

        vbox=QtGui.QVBoxLayout()
        #vbox.addWidget(frame)
        vbox.addLayout(hbox_grid)
        vbox.addStretch(1)

        self.setLayout(vbox)

        # ------ HELP buttons -----------
        hw=help_widget.HelpWidget(here+'/help_texts/tab_system.html',"https://github.com/ilyasku/CompoundPye/wiki/GUI#system")
        vbox.addWidget(hw)


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

        combo.addItem('one dimensional array')
        combo.addItem('two dimensional array')
        combo.addItem('video input')

        combo.activated[str].connect(self.read_combo)

        for w in [label,combo]:
            w.setToolTip("""Select basic structure of your simulated surroundings.<br>
<u>one dimensional array:</u> This is currently quite experimental. Better use one of the other options!<br>
<u>two dimentional array:</u> This is the 'normal' and 'intuitive mode'.<br>
    Will use two dimensional surroundings (planar projection of the agent's (spheric) surroundings).<br>
<u>video input:</u> Allows for specification of a video as surroundings (two-dimensional image information).<br>
    Resolution in pixel will be set to match the video's resolution.
""")

        self.current_combo_str=self.parent_GUI.values['surroundings_values']['current_selected']
        
        index=combo.findText(self.current_combo_str)
        combo.setCurrentIndex(index)

        btn_surroundings_trafo=QtGui.QPushButton("set properties of 2D projection")
        btn_surroundings_trafo.clicked.connect(self.create_projection_pop_up)



        radio_deg=QtGui.QRadioButton("spatial values in degree",self)
        radio_fraction=QtGui.QRadioButton("spatial values in fraction of shown surroundings",self)
        self.radio_fraction=radio_fraction

        radio_deg.toggled.connect(lambda: self.set_spatial_unit('degree'))
        radio_fraction.toggled.connect(lambda: self.set_spatial_unit('fraction'))

        if self.parent_GUI.values['surroundings_values']['spatial_unit']=='degree':
            #radio_deg.toggle()
            radio_deg.setChecked(True)
        else:
            #radio_fraction.toggle()
            radio_fraction.setChecked(True)

        ## tmp


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

        # ------ HELP buttons -----------
        hw=help_widget.HelpWidget(here+'/help_texts/tab_surroundings.html',"https://github.com/ilyasku/CompoundPye/wiki/GUI#surroundings")
        self.grid.addWidget(hw,8,0,1,5)



    def set_spatial_unit(self,unit):


        if unit=='degree' and not self.radio_fraction.isChecked():
            msg=QtGui.QMessageBox.information(self, "Not implemented yet!", "You'll have to do with fractional\nspatial values for now!", "Too bad.")
            #self.radio_fraction.toggle()
            self.radio_fraction.setChecked(True)
        elif unit=="fraction":
            self.parent_GUI.values['surroundings_values']['spatial_unit']="fraction"


        # The following block becomes useful only after conversion is fully implemented. 
        # Otherwise, just use the above one, that doesn't allow a conversion!
        '''
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
        '''
                
        
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

                lbl.setToolTip("Set size of simulated surroundings in pixel.")
                line_edit1.setToolTip("Size of x-direction (horizontal) in pixel.")
                line_edit2.setToolTip("Size of y-direction (vertical) in pixel.")

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
                
                
                lbl.setToolTip("Set size of simulated surroundings in pixel.")
                line_edit.setToolTip("Size in pixel.")



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

                for w in [lbl,self.line_edit_video_file]:
                    w.setToolTip("Specify (absolute) path to video file. You can also use the 'browse' button to the right.")
                browse.setToolTip("Browse for a video file to use as input.")

                grid.addWidget(lbl,0,0,1,1)
                grid.addWidget(self.line_edit_video_file,0,1,1,5)
                grid.addWidget(browse,0,6,1,1)

                lbl_start=QtGui.QLabel('start at')
                video_start_t=QtGui.QLineEdit()
                lbl_unit1=QtGui.QLabel('s')
                lbl_unit2=QtGui.QLabel('s')

                lbl_end=QtGui.QLabel(';  end at')
                video_end_t=QtGui.QLineEdit()

                for w in [lbl_start,video_start_t,lbl_unit1, lbl_unit2, lbl_end,video_end_t]:
                    w.setToolTip("""CURRENTLY NOT IMPLEMENTED<br>
Idea: Specify which time span to use of given video file.""")

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
        for key in list(self.copy_values.keys()):
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

        #vbox=QtGui.QVBoxLayout()
        #vbox.addLayout(self.grid)
        #self.setLayout(vbox)

        # ------ HELP buttons -----------
        hw=help_widget.HelpWidget(here+'/help_texts/tab_circuit.html',"https://github.com/ilyasku/CompoundPye/wiki/GUI#circuit")
        self.grid.addWidget(hw,9,0,1,6)
        #vbox.addWidget(hw)


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

        #vbox=QtGui.QVBoxLayout()
        self.editor=se.EditorWidget(self)
        #vbox.addWidget(self.editor)
        #self.setLayout(vbox)

        grid=QtGui.QGridLayout()
        grid.addWidget(self.editor,0,0,9,5)
        self.setLayout(grid)

        # ------ HELP buttons -----------
        hw=help_widget.HelpWidget(here+'/help_texts/tab_sensors.html',"https://github.com/ilyasku/CompoundPye/wiki/GUI#sensors")
        #vbox.addWidget(hw)
        grid.addWidget(hw,9,0,1,1)


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
    for i in reversed(list(range(layout.count()))):
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
