## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 16.01.15

"""
@package CompoundPye.src.GUI.stimuli_editor

Provides a stimuli-editor widget (StimuliWidget) that allows the user 
to add/remove/edit stimuli of the agent's Surroundings.

@todo How nice a stimulus preview would be! shouldn't be so hard, 
just need an animation of surroundings' intensities in a pop-up window.
"""

from PyQt4 import QtGui

from ..Parser import sc


class StimuliWidget(QtGui.QScrollArea):
    """
    Editor window in which the user can add/remove/edit stimuli.
    """
    def __init__(self,parent_Tab):
        """
        Initializes a StimuliWidget.
        @param parent_Tab Requires the parent SurroundingsTab (or rather a pointer to it) as input, to read its current settings and access its members.
        """
        super(StimuliWidget,self).__init__()
        self.parent_Tab=parent_Tab

        self.one_dim=None
        self.two_dim=None
        self.video=None

        self.init_UI()
        

    def init_UI(self):
        """
        Sets the central widget according to the kind of surroundings selected in the parent SurroundingsTab's combo-box.
        """
        self.setWidgetResizable(True)
        self.set_widget(self.parent_Tab.current_combo_str)


    def set_widget(self,s):
        """
        Figures out the current selection of the type of surroundings in the parent SurroundingsTab's combo-box.
        """
        if s=='two dimensional array':
            self.w=StimuliSubWidget(self,2)
        elif s=='one dimensional array':
            self.w=StimuliSubWidget(self,1)
        elif s=='video input':
            self.w=QtGui.QWidget()
            
        else:
            EH.handle(2,'in StimuliWidget.set_widget: wrong input string!')

        self.setWidget(self.w)

class DummyWidget(QtGui.QWidget):
    """
    A dummy widget that has an additional member DummyWidget.stimuli in case this is ever required...
    """
    def __init__(self):
        super(DummyWidget,self).__init__()
        self.stimuli=[]

class StimuliSubWidget(QtGui.QWidget):
    """
    A sub-widget shown in the parent StimuliWidget.
    """
    def __init__(self,parent_StimuliWidget,dim):
        """
        Initializes a StimuliSubWidget.
        @param parent_StimuliWidget Requires the sub-widget's parent StimuliWidget as input to access its variables.
        @param dim Integer, either ==1 or ==2, specifying the dimension of the surroundings.
        """
        super(StimuliSubWidget,self).__init__()
        self.parent_StimuliWidget=parent_StimuliWidget

        self.dim=dim

        if dim==1:
            self.stimuli=self.parent_StimuliWidget.parent_Tab.parent_GUI.values['surroundings_values']['stimuli']['one_dim']
        elif dim==2:
            self.stimuli=self.parent_StimuliWidget.parent_Tab.parent_GUI.values['surroundings_values']['stimuli']['two_dim']

        self.stim_lines=[]


        self.n=0
        self.n_lbl=0

        self.init_UI()
    
    def init_UI(self):
        """
        Initializes all the widgets (labels, buttons, etc.) displayed on this StimuliSubWidget.
        """
        self.layout=QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        btn_add_stim=QtGui.QPushButton('add stimulus')
        btn_add_stim.clicked.connect(self.do_add_stim)
        self.layout.addWidget(btn_add_stim)
    
        self.layout.addStretch(1)

        for s in self.stimuli:
            self.add_stim(s)


    def add_stim(self,values):
        """
        Add a stimulus ('StimLine'-widget) with given values.
        @param values Dictionary containing stimulus-values.
        """
        new_stim=StimLine(self,1,self.n,values)
        self.layout.insertWidget(self.n,new_stim)
        self.n+=1
        self.n_lbl+=1

        self.stim_lines.append(new_stim)

    def do_add_stim(self):
        """
        Add a new stimulus ('StimLine'-widget) with default values.
        """
        if self.dim==1:
            values={'name':'new stimulus '+str(self.n_lbl),'array_file':None,'extend':'0.0','starting_point':'0.0','velocity':'0.0','def':'','def_args':'','mode':'load','show':True,'selected_obj':'','obj_args':''}
        elif self.dim==2:
            values={'name':'new stimulus '+str(self.n_lbl),'path_to_file':'','extend':'0.0,0.0','starting_point':'0.0,0.0','velocity':'0.0,0.0','def':'','def_args':'','mode':'load','show':True,'selected_obj':'','obj_args':'','load':'array'}
        self.stimuli.append(values)
        new_stim=StimLine(self,1,self.n,values)
        self.layout.insertWidget(self.n,new_stim)
        self.n+=1
        self.n_lbl+=1

        self.stim_lines.append(new_stim)

    def do_remove(self,index):
        """
        Remove stimulus ('StimLine'-widget) with given index.
        @param index Index of the stimulus' 'StimLine'-widget in this StimuliSubWidget's layout.
        """
        item=self.layout.itemAt(index)
        self.stimuli.pop(index)
        self.n=self.n-1
        self.layout.removeItem(item)

        self.stim_lines.pop(index)

        item.widget().deleteLater()
        
        for i in range(0, len(self.stim_lines)):
            self.stim_lines[i].index=i
        

        #print self.layout.count()

class StimLine(QtGui.QWidget):
    """
    A widget representing a stimulus in the graphical editor ('StimuliSubWidget'), consisting of buttons to edit/remove the stimulus.
    """
    def __init__(self,parent_StimSubWidget,mode,index,values):
        """
        Initialize a StimLine object.
        @param parent_StimSubWidget Requires its parent StimuliSubWidget (or rather a pointer to it) as input to access its variables.
        @param mode Dimension of the stimulus' surroundings, either '1' or '2'; not of any use at the moment, but something might be implemented later on...
        @param index Index of the StimLine in its parent StimuliSubWidget's layout (and also in some other lists). 
        @param values Dictionary of stimulus values.
        """
        super(StimLine,self).__init__()
        self.mode=mode
        self.parent_StimSubWidget=parent_StimSubWidget
        self.values=values
        self.index=index
    
        self.popup=None

        self.init_UI()

    def init_UI(self):
        """
        Initializes all graphical elements (widgets like buttons, labels, etc.) displayed on this 'StimLine'-object.
        """
        grid=QtGui.QGridLayout()
        self.setLayout(grid)

        self.btn_name=QtGui.QPushButton(self.values['name'])
        self.btn_name.clicked.connect(self.do_popup)

        grid.addWidget(self.btn_name,0,0)
        
        lbl_show_hide=QtGui.QLabel('show/hide stimulus:')
        self.toggle=self.values['show']
        self.btn_show_hide=QtGui.QPushButton('showing')
        if self.toggle==False:
            self.btn_show_hide.setText('hidden')
        
        
        self.btn_show_hide.clicked.connect(self.toggle_show_hide)
        

        grid.addWidget(lbl_show_hide,0,1)
        grid.addWidget(self.btn_show_hide,0,2)

        btn_remove=QtGui.QPushButton('remove')
        btn_remove.clicked.connect(self.do_remove)
        
        grid.addWidget(btn_remove,0,3)

    def do_remove(self):
        """
        Remove this StimLine from its parent StimuliSubWidget.
        """
        self.parent_StimSubWidget.do_remove(self.index)
        self.close()


    def toggle_show_hide(self):
        """
        Toggle whether the stimulus this StimLine is representing should be shown or hidden during a run of the simulation.
        """
        if self.parent_StimSubWidget.stimuli[self.index]['show']:
            self.parent_StimSubWidget.stimuli[self.index]['show']=False
            self.btn_show_hide.setText('hidden')
        else:
            self.parent_StimSubWidget.stimuli[self.index]['show']=True
            self.btn_show_hide.setText('showing')
        

    def do_popup(self):
        """
        Pops up a StimPopup in which the user can edit the stimulus' parameters.
        """
        if self.mode==1:
            self.popup=StimPopup(self)
        elif self.mode==2:
            self.popup=StimPopup(self)
        else:
            EH.handle(2,'in StimLine.do_popup: StimLine.mode=='+str(self.mode)+'! accepts only "1" or "2".')
        self.popup.show()


class StimPopup(QtGui.QWidget):
    """
    A pop-up window allowing the user to edit the current parameters of the stimulus.
    """
    def __init__(self,parent_StimLine):
        """
        Initializes a StimPopup.
        @param parent_StimLine Requires the stimulus' StimLine as input, to access its variables.
        """
        super(StimPopup,self).__init__()

        self.parent_StimLine=parent_StimLine

        self.copy_values=self.parent_StimLine.values.copy()

        self.init_UI()

    def init_UI(self):
        """
        Initializes all graphical elements (widgets like buttons, labels, etc.) displayed on this 'StimLine'-object.
        """
        layout=QtGui.QVBoxLayout()
        
        self.setLayout(layout)

        # ------------------- name ----------------------------

        hbox_name=QtGui.QHBoxLayout()
        
        lbl_name=QtGui.QLabel('name')
        le_name=QtGui.QLineEdit()
        le_name.setText(self.copy_values['name'])
        le_name.editingFinished.connect(lambda: self.set_value('name',le_name.text()))
        
        hbox_name.addWidget(lbl_name)
        hbox_name.addWidget(le_name)

        layout.addLayout(hbox_name)
        
        # -----------------------------------------------------

        # -------------- mode ---------------------------------
        hbox_mode=QtGui.QHBoxLayout()
        lbl_mode=QtGui.QLabel('editor-mode')
        mode_combo=QtGui.QComboBox()
        #mode_combo.addItem('define function')
        mode_combo.addItem('define array')
        mode_combo.addItem('load array or image from file')
        mode_combo.addItem('select pre-defined stimulus')
        
        mode_combo.activated[str].connect(self.set_mode)

        if self.copy_values['mode']=='def':
            mode_combo.setCurrentIndex(0)
        elif self.copy_values['mode']=='load':
            mode_combo.setCurrentIndex(1)
        elif self.copy_values['mode']=='select':
            mode_combo.setCurrentIndex(2)

        hbox_mode.addWidget(lbl_mode)
        hbox_mode.addWidget(mode_combo)
        layout.addLayout(hbox_mode)
        # -----------------------------------------------------
        
        self.widget_def_load=QtGui.QWidget()
        self.layout_def_load=QtGui.QVBoxLayout()

        self.widget_def_load.setLayout(self.layout_def_load)

        if self.copy_values['mode']=='def':
            self.init_UI_define_array()
        elif self.copy_values['mode']=='load':
            self.init_UI_load_array()
        else:
            self.init_UI_select_obj()

        layout.addWidget(self.widget_def_load)
        # ----------------------------------------------------


        # ------------- extend -------------------------------

        hbox_extend=QtGui.QHBoxLayout()

        lbl_extend=QtGui.QLabel('size')
        le_extend=QtGui.QLineEdit()
        le_extend.setText(self.copy_values['extend'])
        le_extend.editingFinished.connect(lambda: self.set_value('extend',le_extend.text()))

        hbox_extend.addWidget(lbl_extend)
        hbox_extend.addWidget(le_extend)
        
        layout.addLayout(hbox_extend)
        
        


        # ------------- starting point -----------------------
        hbox_start=QtGui.QHBoxLayout()
        if self.parent_StimLine.parent_StimSubWidget.parent_StimuliWidget.parent_Tab.parent_GUI.values['surroundings_values']['spatial_unit']=="fraction":
            lbl_start=QtGui.QLabel('starting point\n(in relative lenght of the surroundings)')
        else:
            lbl_start=QtGui.QLabel('starting point\n(in degree)')
        le_start=QtGui.QLineEdit()
        le_start.setText(self.copy_values['starting_point'])

        le_start.editingFinished.connect(lambda: self.set_value('starting_point',le_start.text()))

        hbox_start.addWidget(lbl_start)
        hbox_start.addWidget(le_start)
        layout.addLayout(hbox_start)
        # ----------------------------------------------------


        # ------------- velocity -----------------------------
        hbox_velo=QtGui.QHBoxLayout()
        if self.parent_StimLine.parent_StimSubWidget.parent_StimuliWidget.parent_Tab.parent_GUI.values['surroundings_values']['spatial_unit']=="fraction":
            lbl_velo=QtGui.QLabel('velocity\n(length of surroundings/second)')
        else:
            lbl_velo=QtGui.QLabel('velocity\n(in deg/second)')
        le_velo=QtGui.QLineEdit()
        le_velo.setText(self.copy_values['velocity'])

        le_velo.editingFinished.connect(lambda: self.set_value('velocity',le_velo.text()))

        hbox_velo.addWidget(lbl_velo)
        hbox_velo.addWidget(le_velo)
        layout.addLayout(hbox_velo)
        # ----------------------------------------------------
        
        # ----------- buttons cancel/done --------------------
        
        hbox_btns=QtGui.QHBoxLayout()

        btn_cancel=QtGui.QPushButton('cancel')
        btn_done=QtGui.QPushButton('done')

        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)

        hbox_btns.addStretch(1)
        hbox_btns.addWidget(btn_cancel)
        hbox_btns.addWidget(btn_done)

        layout.addLayout(hbox_btns)
        # ----------------------------------------------------

    def init_UI_select_obj(self):
        """
        If the user selects to specify the stimulus via selecting a pre-defined stimulus, some widgets will be replaced by those in this function.
        """
        clearLayout(self.layout_def_load)

        layout_select=QtGui.QVBoxLayout()


        hbox_select=QtGui.QHBoxLayout()
        layout_select.addLayout(hbox_select)

        lbl_select=QtGui.QLabel('select stimulus-object')
        combo_select=QtGui.QComboBox()
        for obj in sc.two_dim_dict:
            combo_select.addItem(obj)
        if self.copy_values['selected_obj']:
            index=combo_select.findText(self.copy_values['selected_obj'])
            combo_select.setCurrentIndex(index)
            
        combo_select.activated[str].connect(self.set_select)
        
        hbox_select.addWidget(lbl_select)
        hbox_select.addWidget(combo_select)

        hbox_args=QtGui.QHBoxLayout()
        layout_select.addLayout(hbox_args)

        lbl_args=QtGui.QLabel('object arguments')
        le_args=QtGui.QLineEdit()
        le_args.setText(self.copy_values['obj_args'])
        le_args.editingFinished.connect(lambda: self.set_value('obj_args',le_args.text()))
        le_args.setToolTip('''don't put in px_x and px_y here!!!
Will be auto-filled in when creating the stimulus''')
        
        hbox_args.addWidget(lbl_args)
        hbox_args.addWidget(le_args)
        
        self.layout_def_load.addLayout(layout_select)

        


    def init_UI_define_array(self):
        """
        NOT IMPLEMENTED YET! If the user selects to specify the stimulus by defining a function that returns an array with intensities (==stimulus), this function replaces some widgets accordingly.
        """
        clearLayout(self.layout_def_load)
        

        self.layout_def=QtGui.QVBoxLayout()

        self.def_text_edit=QtGui.QTextEdit()
        self.def_text_edit.textChanged.connect(lambda: self.set_value('def',self.def_text_edit.toPlainText()))
        self.def_text_edit.setToolTip('''define an array here
        - name the array a (e.g. a=np.ones((100,100)) )
        - use python syntax
        - use numpy as 'np'
        - has to return a numpy-array of fitting dimension 
          (dimension depends on your surroundings)
        - the returned array represents the stimulus' intensity per pixel,
          but will be resized according to the rest of the parameters you specify''')
        if len(self.copy_values['def'])==0:
            self.def_text_edit.setText('''define an array here
        - name the array a (e.g. a=np.ones((100,100)) )
        - use python syntax
        - use numpy as 'np'
        - has to return a numpy-array of fitting dimension 
          (dimension depends on your surroundings)
        - the returned array represents the stimulus' intensity per pixel,
          but will be resized according to the rest of the parameters you specify''')
        else:
            self.def_text_edit.setText(self.copy_values['def'])

        self.layout_def.addWidget(self.def_text_edit)
        
        self.layout_def_load.addLayout(self.layout_def)

    def init_UI_load_array(self):
        """
        NOT IMPLEMENTED YET! If the user selects to load an array with intensities (==stimulus), this function replaces some widgets accordingly.
        """
        #item=self.layout_def_load.itemAt(0)
        #self.layout_def_load.removeItem(item)

        clearLayout(self.layout_def_load)


        self.layout_load=QtGui.QVBoxLayout()

        hbox_browse=QtGui.QHBoxLayout()

        self.le_file=QtGui.QLineEdit()
        btn_browse=QtGui.QPushButton('browse')
        
        self.le_file.editingFinished.connect(lambda: self.set_value('path_to_file',self.le_file.text()))

        self.le_file.setText(self.copy_values['path_to_file'])

        btn_browse.clicked.connect(self.do_browse)

        hbox_browse.addWidget(self.le_file)
        hbox_browse.addWidget(btn_browse)
        
        self.layout_load.addLayout(hbox_browse)

        radio_btn_array=QtGui.QRadioButton("input file holds an array",self)
        radio_btn_image=QtGui.QRadioButton("input file holds an image",self)

        radio_btn_array.toggled.connect(lambda: self.set_value("load","array"))
        radio_btn_image.toggled.connect(lambda: self.set_value("load","image"))

        if self.copy_values['load']=='array':
            radio_btn_array.toggle()
        else:
            radio_btn_image.toggle()

        self.layout_load.addWidget(radio_btn_array)
        self.layout_load.addWidget(radio_btn_image)

        self.layout_def_load.addLayout(self.layout_load)
        




    def set_mode(self,s):
        """
        Sets the mode how to create the stimulus (either select a pre-defined stimulus class, define a function that returns a stimulus-array, or load a stimulus-array from file).
        """
        if s=='define array':
            self.copy_values['mode']='def'
            self.init_UI_define_array()
        elif s=='load array or image from file':
            self.copy_values['mode']='load'
            self.init_UI_load_array()
        elif s=='select pre-defined stimulus':
            self.copy_values['mode']='select'
            self.init_UI_select_obj()

    def set_select(self,s):
        """
        Reads the string from the combo-box to select a class, sets the value accordingly.
        """
        self.copy_values['selected_obj']=s


    def set_value(self,key,value):
        """
        Assign a new value to given key in StimPopup.copy_values.
        @param key Key to which the new value will be assigned.
        @param value New value to be assigned to given key.
        """
        self.copy_values[key]=value

    def do_browse(self):
        """
        If selected mode is loading a stimulus-array from file, the user can browse for a file here.
        """
        fname=QtGui.QFileDialog.getOpenFileName(self, 'select file')
        self.le_file.setText(fname)
        self.set_value('path_to_file',fname)
        
        
    def do_cancel(self):
        """
        Close the pop-up discarding all changes.
        """
        self.close()

    def do_done(self):
        """
        Close the pop-up keeping all changes.
        """
        for key in list(self.parent_StimLine.values.keys()):
            self.parent_StimLine.values[key]=self.copy_values[key]
        self.parent_StimLine.btn_name.setText(self.copy_values['name'])
        self.close()


# ---------------------------------------------------------------------------------------------------
##### COPIED FROM: http://stackoverflow.com/questions/9374063/pyqt4-remove-widgets-and-layout-as-well 
##### USER: Avaris
##### DATE OF POST: Feb 21 '12 at 9:45
def clearLayout(layout):
    for i in reversed(list(range(layout.count()))):
        item = layout.itemAt(i)

        if isinstance(item, QtGui.QWidgetItem):
            #print "widget" + str(item)
            #item.widget().close()
            item.widget().deleteLater()
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
