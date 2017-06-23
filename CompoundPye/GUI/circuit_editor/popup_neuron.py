from PyQt4 import QtGui
from ..help_widget import WikiBtn
from ..styles import blue_tooltips
from ...Parser import creator

list_of_transfer_functions = creator.transf_func_dict.keys()


class PopupNeuron(QtGui.QWidget):
    """
    A widget in which the user can specify a neuron's parameters.
    Pops up when the user hits the button that shows the neuron's name.
    """
    def __init__(self, parent_CompWidget):
        """
        Initializes a 'PopupNeuron'-object.
        @param parent_CompWidget Requires a pointer to its parent CompWidget as input.
        """
        super(PopupNeuron, self).__init__()        
        self.new_values = parent_CompWidget.values.copy()
        self.parent_comp_widget = parent_CompWidget
        self.init_UI()

    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """
        self.setStyleSheet(blue_tooltips)
        global list_of_comps
        self.resize(900, 400)
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)        
        grid = QtGui.QGridLayout()
        vbox.addLayout(grid)    
        # ---------- name ----------------------
        lbl_name = QtGui.QLabel('name')
        le_name = QtGui.QLineEdit()
        le_name.setText(self.new_values['name'])
        grid.addWidget(lbl_name, 0, 0)
        grid.addWidget(le_name, 0, 1)
        le_name.editingFinished.connect(lambda: self.set_value('name', le_name.text()))
        # --------------------------------------
        # ----------- comp object --------------
        lbl_comp_obj = QtGui.QLabel('component object')
        self.combo_comp_obj = QtGui.QComboBox()
        for comp in list_of_comps:
            self.combo_comp_obj.addItem(comp)
        index = self.combo_comp_obj.findText(self.new_values['component_object'])
        self.combo_comp_obj.setCurrentIndex(index)
        self.combo_comp_obj.activated[str].connect(self.read_combo_comp)
        grid.addWidget(lbl_comp_obj, 1, 0)
        grid.addWidget(self.combo_comp_obj, 1, 1)
        # --------------------------------------
        # ------------ object args -------------
        lbl_obj_args = QtGui.QLabel('object arguments\n(comma separated, keywords possible)')
        self.le_obj_args = QtGui.QLineEdit()
        self.le_obj_args.setText(self.new_values['object_args'])
        self.le_obj_args.editingFinished.connect(lambda: self.set_value('object_args',
                                                                        self.le_obj_args.text()))
        grid.addWidget(lbl_obj_args, 2, 0)
        grid.addWidget(self.le_obj_args, 2, 1)
        # --------------------------------------
        self.update_comp_tooltip(self.new_values['component_object'])
        # ----------- transfer function --------
        lbl_tf = QtGui.QLabel('transfer function')
        self.combo_tf = QtGui.QComboBox()
        for tf in list_of_transfer_functions:
            self.combo_tf.addItem(tf)
        index = self.combo_tf.findText(self.new_values['transfer_func'])
        self.combo_tf.setCurrentIndex(index)
        self.combo_tf.activated[str].connect(self.read_combo_tf)
        grid.addWidget(lbl_tf, 3, 0)
        grid.addWidget(self.combo_tf, 3, 1)
        # --------------------------------------
        # ------- function args ----------------        
        lbl_fargs = QtGui.QLabel('function arguments\n(comma separated, keywords possible)')
        self.le_fargs = QtGui.QLineEdit()
        self.le_fargs.setText(self.new_values['func_args'])
        self.le_fargs.editingFinished.connect(
            lambda: self.set_value('func_args', self.le_fargs.text()))
        grid.addWidget(lbl_fargs, 4, 0)
        grid.addWidget(self.le_fargs, 4, 1)
        # --------------------------------------
        self.update_transferfunction_tooltip(self.new_values['transfer_func'])
        # ---------- axis and direcetion checkboxes ---------
        if self.parent_comp_widget.parent_UI.mode == 'between':

            hbox_attributes = QtGui.QHBoxLayout()            
            checkbox_axis = QtGui.QCheckBox('use axis attribute')
            checkbox_axis.stateChanged.connect(self.do_toggle_axis)
            checkbox_direction = QtGui.QCheckBox('use direction attribute')
            checkbox_direction.stateChanged.connect(self.do_toggle_direction)
            self.axis, self.direction = self.get_attributes_state()            
            if self.axis:
                checkbox_axis.toggle()
            if self.direction:
                checkbox_direction.toggle()
            hbox_attributes.addWidget(checkbox_axis)
            hbox_attributes.addWidget(checkbox_direction)
            vbox.addLayout(hbox_attributes)
        # ---------- buttoness -----------------
        hbox = QtGui.QHBoxLayout()
        vbox.addLayout(hbox)
        wiki_btn = WikiBtn("https://github.com/ilyasku/CompoundPye/wiki/GUI#output")
        hbox.addWidget(wiki_btn)
        hbox.addStretch(1)

        btn_cancel = QtGui.QPushButton('cancel')
        btn_done = QtGui.QPushButton('done')

        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)
        
        hbox.addWidget(btn_cancel)
        hbox.addWidget(btn_done)
        # ---------------------------------------

    def do_toggle_direction(self, state):
        """
        Toggles the direction attribute after checking/unchecking the direction checkbox.
        """
        if state:
            self.direction = True
        else:
            self.direction = False
        self.write_attributes_state()

    def do_toggle_axis(self, state):
        """
        Toggles axis attribute after checking/unchecking the axis checkbox.
        """
        if state:
            self.axis = True
        else:
            self.axis = False
        self.write_attributes_state()

    def get_attributes_state(self):
        """
        Parses the attributes string of a cell connecting neighbouring columns.
        """
        s = self.new_values['attributes']
        if s == '-' or s == '' or s is None or s == 'None':
            return False, False
        else:
            split = s.split(',')
            axis = False
            direction = False
            if split.count('axis'):
                axis = True
            if split.count('direction'):
                direction = True
            return axis, direction

    def write_attributes_state(self):
        """
        Creates a string to store attributes in a circuit file.
        """
        s = '-'
        if self.axis and self.direction:
            s = 'axis,direction'
        elif self.axis:
            s = 'axis'
        elif self.direction:
            s = 'direction'        
        self.new_values['attributes'] = s

    def read_combo_comp(self, combo_str):
        """
        Read the combo specifying the Component-object to use and 
        changes the entry in PopupNeuron.new_values accordingly.
        """
        combo_str = str(combo_str)
        self.new_values['component_object'] = combo_str
        self.update_comp_tooltip(combo_str)
    
    def update_comp_tooltip(self, comp_str):        
        exec("from " + creator.comp_dict[comp_str].rpartition('/')[-1].partition('.py')[0]
             + " import " + comp_str)
        exec("doc_str=" + comp_str + ".__doc__")
        exec("doc_str_init=" + comp_str + ".__init__.__doc__")
        if doc_str_init:
            doc_str_init = doc_str_init.lstrip().rstrip().replace('\n', '<br>')
        else:
            sorry = """<u>SORRY, NO DOCSTRING FOUND!</u><br>
 But here's a list of the constructor function's parameters:<br>"""
            import inspect
            exec("l=inspect.getargspec(" + comp_str + ".__init__)")
            for i in range(1, len(l.args)):
                arg = l.args[i]
                if i > len(l.args) - len(l.defaults):
                    arg = arg + " = " + str(l.defaults[i - (len(l.args) - len(l.defaults))])
                sorry = sorry + "<br>" + arg
            doc_str_init = sorry            

        self.combo_comp_obj.setToolTip("Copy of docstring for class <u>"
                                       + comp_str + "</u>:<br><br>" + doc_str)
        self.le_obj_args.setToolTip("Note, that you don't need to put in the frist and second "
                                    + "arguments,<br>as these will be filled in automatically "
                                    + " using the below input of this window!<br>Furthermore, "
                                    + "you don't need to care about any parameter named 'debug'."
                                    + "<br>Copy of docstring for class " + comp_str
                                    + "'s constructor function:<br><br>" + doc_str_init)

    def read_combo_tf(self, combo_str):
        """
        Read the combo specifying the transfer-function to use and 
        changes the entry in PopupNeuron.new_values accordingly.
        """
        combo_str = str(combo_str)
        self.new_values['transfer_func'] = combo_str
        self.update_transferfunction_tooltip(combo_str)

    def update_transferfunction_tooltip(self, tf_str):
        exec("from "
             + creator.transf_func_dict[tf_str].rpartition('/')[-1].partition('.py')[0]
             + " import " + tf_str)
        exec("doc_str=" + tf_str + ".__doc__")
        if not doc_str:
            doc_str = """SORRY, NO DOCSTRING FOUND! """
            
        self.combo_tf.setToolTip("Copy of " + tf_str
                                 + "'s docstring:<br><br>" + doc_str)

        param_tooltip = "<ul>"
        import inspect
        exec("l=inspect.getargspec(" + tf_str + ")")
        for i in range(1, len(l.args)):
            arg = "<li>" + l.args[i]
            if i > len(l.args) - len(l.defaults):
                arg = arg + " = " + str(l.defaults[i - (len(l.args) - len(l.defaults))])
            arg=arg + "</li>"
            param_tooltip = param_tooltip + "\n" + arg
        param_tooltip = "List of <u>" + tf_str + "'s</u> arguments:<br>" + param_tooltip + "</ul>"
        self.le_fargs.setToolTip(param_tooltip)

    def do_cancel(self):
        """
        Close the pop-up if the 'cancel'-button hit.
        """
        self.close()
        
    def do_done(self):
        """
        Copies the PopupNeurons.new_values-dictionary to replace the old 
        values-dictionary in the parent ComponentWidget's list of values 
        if the 'done'-button is clicked.
        """
        for key in self.parent_comp_widget.values.keys():
            self.parent_comp_widget.values[key] = self.new_values[key]
        self.parent_comp_widget.edited()
        self.close()

    def set_value(self, key, value):
        """
        Sets the value for the given key in the  PopupNeurons.values-dictionary.
        @param key Key of the value that is to be changed.
        @param value New value for the given key.
        """
        self.new_values[key] = value
