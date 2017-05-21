## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 15.01.15

"""
@package CompoundPye.src.GUI.circuit_editor

This package contains a graphical circuit editor (QTabWidget), 
enabling the user to add/remove neurons and specify parameters and connections.
"""
from PyQt4 import QtCore, QtGui

## @todo understand that warning: "RuntimeWarning: PyOS_InputHook is
# not available for interactive use of PyGTK set_interactive(1)"
# which appeared after i added this import:
from ..Parser import *

from . import help_widget
from .styles import *

import os
here = os.path.dirname(os.path.abspath(__file__))

list_of_comps = list(creator.comp_dict.keys())
list_of_tfs = list(creator.transf_func_dict.keys())

## @todo for connections from 'column' to 'between' components I need
# 2 weights, one coming from left one from right.


class EditorTabs(QtGui.QTabWidget):
    """
    This class is a QTabWidget whose tabs contain two similar editor-widgets, 
    in which the user can build up and edit a circuit of neurons/components.
    Only 'column'-mode is implemented so far, which basically means that the 
    user adds/removes/edits neurons that appear in each column 
    (one column per sensor) or connecting two neighbouring columns.
    """
    def __init__(self,fname=None):
        """
        Initializes an 'EditorTabs'-object.
        @param fname Path to an initial file, None if no initial file is provided.
        """
        super(EditorTabs,self).__init__()

        self.neurons={'column':[],'between':[],'tangential':[]}
        self.connections={'column':[],'next_neighbour':[],'tangential_to':[],'tangential_from':[]}
        self.receiver=[]
        self.arrangement='column'
        
        self.variables={}


        if fname:
            self.load_file(fname)
        else:
            pass

        self.n_label=0

        editor_column=Editor(self,'column')
        editor_between=Editor(self,'between')
        editor_tangential=Editor(self,'tangential')

        self.addTab(editor_column,'cells in column')
        self.addTab(editor_between,'cells connecting neighbouring columns')
        self.addTab(editor_tangential,'tangential cells')

    def load_file(self,fname):
        """
        Loads the circuit-file fname.
        @param fname Path to the circuit(text)-file.
        """
        arrangement,variables,components,connections,receiver=cp.parse_file(fname)

        #print components
        #print 'connections:'
        #print connections
        print('receiver:')
        print(receiver)
        for name in list(components['column_components'].keys()):
            new_dict=components['column_components'][name]
            new_dict['name']=name
            self.neurons['column'].append(new_dict)

        print('after first for loop:')
        print(new_dict)

        for name in list(components['between_next_neighbour_components'].keys()):
            new_dict=components['between_next_neighbour_components'][name]
            new_dict['name']=name
            self.neurons['between'].append(new_dict)

        print('after second for loop:')
        print(new_dict)
            
        for name in list(components['tangential_components'].keys()):
            new_dict=components['tangential_components'][name]
            new_dict['name']=name
            self.neurons['tangential'].append(new_dict)

        print('after third for loop:')
        print(new_dict)


        for c in connections['column_connections']:
            self.connections['column'].append(c)
        for c in connections['next_neighbour_connections']:
            self.connections['next_neighbour'].append(c)
        for c in connections['tangential_to_connections']:
            self.connections['tangential_to'].append(c)
        for c in connections['tangential_from_connections']:
            self.connections['tangential_from'].append(c)

        self.receiver=receiver
        self.arrangement=arrangement
        self.variables=variables

    def save_file(self,fname):
        """
        Saves the current circuit in a circuit(text)-file.
        """
        cp.save_file(fname,self.arrangement,self.variables,self.neurons,self.connections,self.receiver)
        
class Editor(QtGui.QFrame):
    """
    An ditor-widget that serves as content of the tabs of 'EditorTabs'-objects. 
    It allows the user to add/remove/edit neurons in a group specified by the tab.
    """
    def __init__(self,parent_EditorTabs,mode):
        """
        Initializes an 'Editor'-object.
        @param parent_EditorTabs Requires the parent 'EditorTabs'-object as parameter to access its list and dictionries that store components/neurons and parameters.
        @param mode The mode can be 'column' or 'between', it tells the Editor which list of neurons of the parent 'EditorTabs'-object it should read from/write to.
        """
        super(Editor,self).__init__()

        self.parent_EditorTabs=parent_EditorTabs
        self.mode=mode

        self.n=0
        
        self.neurons=self.parent_EditorTabs.neurons
        self.connections=self.parent_EditorTabs.connections

        self.init_UI()
        
        

    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """

        wrap_vbox=QtGui.QVBoxLayout()

        self.scrollArea=QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        
        widget_in_scroll_area=QtGui.QWidget()

        self.scrollArea.setWidget(widget_in_scroll_area)

        #self.setStyleSheet("margin:5px; border:1px solid rgb(0,0,0); ")
        #self.setStyleSheet("border:1px solid rgb(0,0,0); ")
        self.vbox=QtGui.QVBoxLayout()

        widget_in_scroll_area.setLayout(self.vbox)
        
        wrap_vbox.addWidget(self.scrollArea)
        self.setLayout(wrap_vbox)

        self.btn_add=QtGui.QPushButton('add neuron')
        self.btn_add.clicked.connect(self.add_neuron)
        
        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(self.btn_add)
        hbox.addStretch(1)

        self.vbox.addLayout(hbox)
        self.vbox.addStretch(1)

        initial_copy=self.neurons[self.mode][:]
        self.neurons[self.mode]=[]

        while len(initial_copy):
            self.add_neuron(initial_copy.pop(0))

    def add_neuron(self,initial=False):
        """
        Adds a neuron to the list of neurons, either with or without initial parameters.
        @param initial Can be initialized with a dictionary of parameters.
        """
        if initial==False:
            neuron=CompWidget(self)
        else:
            neuron=CompWidget(self,initial)
        self.vbox.insertWidget(self.n,neuron)
        
        self.neurons[self.mode].append(neuron)
        
        self.n+=1
        self.parent_EditorTabs.n_label+=1
    
    def removed(self,j):
        """
        Tells the 'Editor'-object, that the 'remove'-button of a neuron (CompWidget) shown in the editor has been clicked and that the Editor has to remove it from its lists.
        @param j Index of the neuron (CompWidget) to be removed.
        """
        self.n=self.vbox.count()-2
        
        label_of_removed_neuron=self.neurons[self.mode][j].name

        self.neurons[self.mode].pop(j)
        for i in range(len(self.neurons[self.mode])):
            self.neurons[self.mode][i].index=i

        for key in list(self.connections.keys()):
            need_to_pop=[]
            for i in range(0,len(self.connections[key])):
                c=self.connections[key][i]
                if c[0]==label_of_removed_neuron or c[2]==label_of_removed_neuron:
                    need_to_pop.append(i)
                else:
                    pass
            need_to_pop.reverse()
            for k in need_to_pop:
                self.connections[key].pop(k)

    def change_name(self,old,new):
        """
        Tells the 'Editor'-object that a neuron's (CompWidget's) name has been changed; scans through the lists of connections to change the old name to the new name in those lists.
        @param old Old name of the neuron (CompWidget).
        @param new New name of the neuron (CompWidget).
        """
        for key in list(self.connections.keys()):
            for i in range(0,len(self.connections[key])):
                c=self.connections[key][i]
                if c[0]==old:
                    l=list(c)
                    l[0]=new
                    c=tuple(l)
                if c[2]==old:
                    l=list(c)
                    l[2]=new
                    c=tuple(l)
                self.connections[key][i]=c

class CompWidget(QtGui.QWidget):
    """
    A CompWidget is a graphical representation (just a line of buttons really) of a neuron/component in an 'Editor'-object.
    The user can click its buttons to edit/remove the neuron.
    """
    def __init__(self,parent_UI,initial=False):
        """
        Initializes an 'CompWidget'-object.
        @param parent_UI Requires the parent 'Editor'-object as parameter to access its list and dictionries to store this neuron's/component's parameters.
        @param initial The 'CompWidget'-object can be initialized with a dictionary of parameters.
        """
        super(CompWidget,self).__init__()
        self.parent_UI=parent_UI
        self.index=self.parent_UI.n
        if initial==False:
            self.values={'name':'new neuron '+str(self.parent_UI.parent_EditorTabs.n_label),'component_object':'Component','object_args':'-',
                         'transfer_func':'identity','func_args':'-',
                         'graph_pos':None,'attributes':'-','single_time':'-'}
        else:
            self.values=initial
        self.name=self.values['name']
        self.popup_neuron=None
        self.popup_connection=None
        self.init_UI()
        
    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """
        self.grid=QtGui.QGridLayout()
        self.setLayout(self.grid)

        self.btn_add_connection=QtGui.QPushButton('connections')
        self.btn_add_connection.clicked.connect(self.create_popup_connections)
        self.btn_add_connection.setToolTip("click to edit connections")
        self.btn_name=QtGui.QPushButton(self.values['name'])
        self.btn_name.clicked.connect(self.create_popup_neuron)
        self.btn_name.setToolTip("click to edit properties")
        self.btn_remove=QtGui.QPushButton('remove')
        self.btn_remove.clicked.connect(self.remove)
        
        self.grid.addWidget(self.btn_name,0,0)
        self.grid.addWidget(self.btn_add_connection,0,1)
        self.grid.addWidget(self.btn_remove,0,2)

    def create_popup_neuron(self):
        """
        Pops up a 'PopupNeuron'-widget, in which the user can edit the neuron's parameters.
        """
        self.popup_neuron=PopupNeuron(self)
        self.popup_neuron.show()

    def create_popup_connections(self):
        """
        Pops up a 'PopupConnections'-widget, in which the user can edit/add/remove connections.
        """

        if self.parent_UI.mode=='tangential':
            self.popup_connection=PopupConnectionsTangential(self.parent_UI,self.values['name'])
        else:
            self.popup_connection=PopupConnections(self.parent_UI,self.values['name'])
        self.popup_connection.show()

    def remove(self):
        """
        Removes this 'CompWidget'-object from its parent 'Editor'-widget (and all its entries in the 'Editor'-widgets lists and dictionaries).
        """
        item=self.parent_UI.vbox.itemAt(self.index)
        self.parent_UI.vbox.removeItem(item)
        self.parent_UI.removed(self.index)
        item.widget().close()

    def from_file_dict(self,name,comp_dict):
        """
        @todo SEEMS LIKE THIS IS NOT USED ANYWHERE?
        """
        self.values=comp_dict
        self.values['name']=name
    
    def edited(self):
        """
        After editing in a 'PopupNeuron'-widget is finished, this neuron's name is read from the values-dictionary and its button's label is set appropriately.
        """
        self.btn_name.setText(self.values['name'])
        self.parent_UI.change_name(self.name,self.values['name'])
        self.name=self.values['name']

class PopupNeuron(QtGui.QWidget):
    """
    A widget in which the user can specify a neuron's parameters.
    Pops up when the user hits the button that shows the neuron's name.
    """
    def __init__(self,parent_CompWidget):
        """
        Initializes a 'PopupNeuron'-object.
        @param parent_CompWidget Requires a pointer to its parent CompWidget as input.
        """
        super(PopupNeuron,self).__init__()
        
        self.new_values=parent_CompWidget.values.copy()
        self.CW=parent_CompWidget

        self.init_UI()

    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """

        self.setStyleSheet(blue_tooltips)

        global list_of_comps

        self.resize(900,400)

        vbox=QtGui.QVBoxLayout()
        self.setLayout(vbox)        

        grid=QtGui.QGridLayout()
        vbox.addLayout(grid)
        

        # ---------- name ----------------------
        lbl_name=QtGui.QLabel('name')
        le_name=QtGui.QLineEdit()
        le_name.setText(self.new_values['name'])
        grid.addWidget(lbl_name,0,0)
        grid.addWidget(le_name,0,1)
        le_name.editingFinished.connect(lambda: self.set_value('name',le_name.text()))
        # --------------------------------------

        # ----------- comp object --------------
        lbl_comp_obj=QtGui.QLabel('component object')
        self.combo_comp_obj=QtGui.QComboBox()
        for comp in list_of_comps:
            self.combo_comp_obj.addItem(comp)
        index=self.combo_comp_obj.findText(self.new_values['component_object'])
        self.combo_comp_obj.setCurrentIndex(index)
        self.combo_comp_obj.activated[str].connect(self.read_combo_comp)
        grid.addWidget(lbl_comp_obj,1,0)
        grid.addWidget(self.combo_comp_obj,1,1)
        # --------------------------------------
        # ------------ object args -------------
        lbl_obj_args=QtGui.QLabel('object arguments\n(comma separated, keywords possible)')
        self.le_obj_args=QtGui.QLineEdit()
        self.le_obj_args.setText(self.new_values['object_args'])
        self.le_obj_args.editingFinished.connect(lambda: self.set_value('object_args',self.le_obj_args.text()))
        grid.addWidget(lbl_obj_args,2,0)
        grid.addWidget(self.le_obj_args,2,1)
        # --------------------------------------
        self.update_comp_tooltip(self.new_values['component_object'])

        # ----------- transfer function --------
        lbl_tf=QtGui.QLabel('transfer function')
        self.combo_tf=QtGui.QComboBox()
        for tf in list_of_tfs:
            self.combo_tf.addItem(tf)
        index=self.combo_tf.findText(self.new_values['transfer_func'])
        self.combo_tf.setCurrentIndex(index)
        self.combo_tf.activated[str].connect(self.read_combo_tf)
        #combo_tf.activated[str].connect(lambda: self.set_value('transfer_func',str))

        grid.addWidget(lbl_tf,3,0)
        grid.addWidget(self.combo_tf,3,1)
        # --------------------------------------
        # ------- function args ----------------
        
        lbl_fargs=QtGui.QLabel('function arguments\n(comma separated, keywords possible)')
        self.le_fargs=QtGui.QLineEdit()
        self.le_fargs.setText(self.new_values['func_args'])
        self.le_fargs.editingFinished.connect(lambda: self.set_value('func_args',self.le_fargs.text()))

        grid.addWidget(lbl_fargs,4,0)
        grid.addWidget(self.le_fargs,4,1)
        # --------------------------------------
        self.update_transferfunction_tooltip(self.new_values['transfer_func'])



        # ---------- axis and direcetion checkboxes ---------

        if self.CW.parent_UI.mode=='between':

            hbox_attributes=QtGui.QHBoxLayout()
            
            checkbox_axis=QtGui.QCheckBox('use axis attribute')
            checkbox_axis.stateChanged.connect(self.do_toggle_axis)

            checkbox_direction=QtGui.QCheckBox('use direction attribute')
            checkbox_direction.stateChanged.connect(self.do_toggle_direction)

            self.axis,self.direction=self.get_attributes_state()
            
            if self.axis:
                checkbox_axis.toggle()
            if self.direction:
                checkbox_direction.toggle()

            hbox_attributes.addWidget(checkbox_axis)
            hbox_attributes.addWidget(checkbox_direction)

            vbox.addLayout(hbox_attributes)

        # ---------- buttoness -----------------

        hbox=QtGui.QHBoxLayout()
        vbox.addLayout(hbox)
        
        #hw=help_widget.HelpWidget("Turn to the wiki page for help!","https://github.com/ilyasku/CompoundPye/wiki/GUI#output")
        #wiki_btn=help_widget.WikiBtnOnly("https://github.com/ilyasku/CompoundPye/wiki/GUI#output")
        wiki_btn=help_widget.WikiBtn("https://github.com/ilyasku/CompoundPye/wiki/GUI#output")
        hbox.addWidget(wiki_btn)
        hbox.addStretch(1)

        btn_cancel=QtGui.QPushButton('cancel')
        btn_done=QtGui.QPushButton('done')

        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)
        
        hbox.addWidget(btn_cancel)
        hbox.addWidget(btn_done)
        # ---------------------------------------

    def do_toggle_direction(self,state):
        """
        Toggles the direction attribute after checking/unchecking the direction checkbox.
        """
        if state:
            self.direction=True
        else:
            self.direction=False
        self.write_attributes_state()

    def do_toggle_axis(self,state):
        """
        Toggles axis attribute after checking/unchecking the axis checkbox.
        """
        if state:
            self.axis=True
        else:
            self.axis=False
        self.write_attributes_state()


    def get_attributes_state(self):
        """
        Parses the attributes string of a cell connecting neighbouring columns.
        """
        s=self.new_values['attributes']
        if s=='-' or s=='' or s==None or s=='None':
            return False,False
        else:
            split=s.split(',')
            axis=False
            direction=False
            if split.count('axis'):
                axis=True
            if split.count('direction'):
                direction=True
            return axis,direction

    def write_attributes_state(self):
        """
        Creates a string to store attributes in a circuit file.
        """
        s='-'
        if self.axis and self.direction:
            s='axis,direction'
        elif self.axis:
            s='axis'
        elif self.direction:
            s='direction'
        
        self.new_values['attributes']=s


    def read_combo_comp(self,combo_str):
        """
        Read the combo specifying the Component-object to use and changes the entry in PopupNeuron.new_values accordingly.
        """
        combo_str=str(combo_str)
        self.new_values['component_object']=combo_str
        self.update_comp_tooltip(combo_str)
    
    def update_comp_tooltip(self,comp_str):
        
        exec("from "+creator.comp_dict[comp_str].rpartition('/')[-1].partition('.py')[0] + " import "+comp_str)
        exec("doc_str="+comp_str+".__doc__")
        exec("doc_str_init="+comp_str+".__init__.__doc__")

        if doc_str_init:
            doc_str_init=doc_str_init.lstrip().rstrip().replace('\n','<br>')
        else:
            sorry="""<u>SORRY, NO DOCSTRING FOUND!</u><br>
But here's a list of the constructor function's parameters:<br>"""
            import inspect
            exec("l=inspect.getargspec("+comp_str+".__init__)")
            for i in range(1,len(l.args)):
                arg=l.args[i]
                if i>len(l.args)-len(l.defaults):
                    arg=arg+" = "+str(l.defaults[i-(len(l.args)-len(l.defaults))])
                sorry=sorry+"<br>"+arg
            doc_str_init=sorry
            

        self.combo_comp_obj.setToolTip("Copy of docstring for class <u>"+comp_str+"</u>:<br><br>"+doc_str)
        self.le_obj_args.setToolTip("Note, that you don't need to put in the frist and second arguments,<br>as these will be filled in automatically using the below input of this window!<br>Furthermore, you don't need to care about any parameter named 'debug'.<br>Copy of docstring for class "+comp_str+"'s constructor function:<br><br>"+doc_str_init )


    def read_combo_tf(self,combo_str):
        """
        Read the combo specifying the transfer-function to use and changes the entry in PopupNeuron.new_values accordingly.
        """
        combo_str=str(combo_str)
        self.new_values['transfer_func']=combo_str

        self.update_transferfunction_tooltip(combo_str)

    def update_transferfunction_tooltip(self, tf_str):
        exec("from "+creator.transf_func_dict[tf_str].rpartition('/')[-1].partition('.py')[0]+ " import "+tf_str)
        exec("doc_str="+tf_str+".__doc__")
        #print doc_str
        if not doc_str:
            doc_str="""SORRY, NO DOCSTRING FOUND! """
            
        self.combo_tf.setToolTip("Copy of "+tf_str+"'s docstring:<br><br>"+doc_str)

        param_tooltip="<ul>"
        import inspect
        exec("l=inspect.getargspec("+tf_str+")")
        for i in range(1,len(l.args)):
            arg="<li>"+l.args[i]
            if i>len(l.args)-len(l.defaults):
                arg=arg+" = "+str(l.defaults[i-(len(l.args)-len(l.defaults))])
            arg=arg+"</li>"
            param_tooltip=param_tooltip+"\n"+arg
        param_tooltip="List of <u>"+tf_str+"'s</u> arguments:<br>"+param_tooltip+"</ul>"
        self.le_fargs.setToolTip(param_tooltip)

    def do_cancel(self):
        """
        Close the pop-up if the 'cancel'-button hit.
        """
        self.close()
        
    def do_done(self):
        """
        Copies the PopupNeurons.new_values-dictionary to replace the old values-dictionary in the parent ComponentWidget's list of values if the 'done'-button is clicked.
        """
        for key in list(self.CW.values.keys()):
            self.CW.values[key]=self.new_values[key]
        #print self.CW.values
        self.CW.edited()
        self.close()

    def set_value(self,key,value):
        """
        Sets the value for the given key in the  PopupNeurons.values-dictionary.
        @param key Key of the value that is to be changed.
        @param value New value for the given key.
        """
        self.new_values[key]=value
    

class PopupConnections(QtGui.QWidget):
    """
    A widget in which the user can edit a neuron's connections.
    Pops up when the user hits the connection-button next to the button with a neuron's name on it.
    """
    def __init__(self,parent_editor,neuron_name):
        """
        Initializes a 'PopupConnection'-object.
        @param paren_Editor Requires a pointer to the parent 'Editor'-object of the CompWidget which creates this PopupConnection (to read/write values to the 'Editor'-object).
        @param neuron_name Name of the neuron (required to find its connections in the Editor's lists of connections).
        """
        super(PopupConnections,self).__init__()
        self.parent_editor=parent_editor
        self.source=neuron_name

        self.ConnectionWidgets_list=[]
        self.init_UI()

    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """        

        self.resize(600,400)

        vbox=QtGui.QVBoxLayout()
        self.setLayout(vbox)

        hbox_name=QtGui.QHBoxLayout()
        hbox_name.addStretch(1)
        lbl_name=QtGui.QLabel('connections of '+self.source)
        hbox_name.addWidget(lbl_name)
        hbox_name.addStretch(1)

        vbox.addLayout(hbox_name)

        vsplitter=QtGui.QSplitter(QtCore.Qt.Vertical)

        scroll_area_top=QtGui.QScrollArea()
        scroll_area_top.setWidgetResizable(True)
        #print self.source
        column_ConnectionWidget=ConnectionWidget(self.parent_editor,self,self.source,'column')
        scroll_area_top.setWidget(column_ConnectionWidget)
        self.ConnectionWidgets_list.append(column_ConnectionWidget)

        vsplitter.addWidget(scroll_area_top)
        
        scroll_area_middle=QtGui.QScrollArea()
        scroll_area_middle.setWidgetResizable(True)
        nn_ConnectionWidget=ConnectionWidget(self.parent_editor,self,self.source,'nn')
        scroll_area_middle.setWidget(nn_ConnectionWidget)
        self.ConnectionWidgets_list.append(nn_ConnectionWidget)

        vsplitter.addWidget(scroll_area_middle)

        vbox.addWidget(vsplitter)


        if self.parent_editor.mode=='column':
            hbox_receiver=QtGui.QHBoxLayout()

            checkbox_receiver=QtGui.QCheckBox("receive input from column's sensor")
            
            if self.parent_editor.parent_EditorTabs.receiver.count(self.source):
                checkbox_receiver.toggle()

            checkbox_receiver.stateChanged.connect(self.set_receiver)

            hbox_receiver.addWidget(checkbox_receiver)

            vbox.addLayout(hbox_receiver)


        hbox_btns=QtGui.QHBoxLayout()
        hbox_btns.addStretch(1)

        btn_cancel=QtGui.QPushButton('cancel')
        btn_done=QtGui.QPushButton('done')

        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)

        hbox_btns.addWidget(btn_cancel)
        hbox_btns.addWidget(btn_done)



        vbox.addLayout(hbox_btns)

    def set_receiver(self,state):
        """
        Toggles whether the neuron receives direkt input of the column's sensor or not.
        @param state True or False == receive input or do not.
        """
        if state==QtCore.Qt.Checked:
            self.parent_editor.parent_EditorTabs.receiver.append(self.source)
        else:
            self.parent_editor.parent_EditorTabs.receiver.pop(self.parent_editor.parent_EditorTabs.receiver.index(self.source))

    def do_cancel(self):
        """
        Close this pop-up and all ConnectionWidgets it contains.
        """
        for w in self.ConnectionWidgets_list:
            w.do_cancel()
        self.close()

    def do_done(self):
        """
        Close this pop-up and all ConnectionWidgets it contains, store the ConnectionWidgets' contents in the parent Editor's lists.
        """
        for w in self.ConnectionWidgets_list:
            w.do_done()
        self.close()



class PopupConnectionsTangential(QtGui.QWidget):
    """
    Widget to edit a tangential cells connections, or rather the connections to this cell.
    Very similar to the PopupConnections class, only with two different features:
       - connections need to be specified from any cell to this (tangential) cell rather than the other way around
       - some more parameters (for axis and direction) can be specified in a line edit.
    """
    def __init__(self,parent_editor,neuron_name):
        """
        Initializes a 'PopupConnection'-object.
        @param paren_Editor Requires a pointer to the parent 'Editor'-object of the CompWidget which creates this PopupConnection (to read/write values to the 'Editor'-object).
        @param neuron_name Name of the neuron (required to find its connections in the Editor's lists of connections).
        """
        super(PopupConnectionsTangential,self).__init__()
        self.parent_editor=parent_editor
        self.source=neuron_name


        self.init_UI()


    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """        

        self.resize(600,400)

        vbox=QtGui.QVBoxLayout()
        self.setLayout(vbox)

        hbox_name=QtGui.QHBoxLayout()
        hbox_name.addStretch(1)
        lbl_name=QtGui.QLabel('connections of '+self.source)
        hbox_name.addWidget(lbl_name)
        hbox_name.addStretch(1)

        vbox.addLayout(hbox_name)

        scroll_area_to=QtGui.QScrollArea()
        scroll_area_to.setWidgetResizable(True)

        self.ConnectionWidget_to=ConnectionWidget(self.parent_editor,self,self.source,'tangential_to')
        scroll_area_to.setWidget(self.ConnectionWidget_to)
        

        vbox.addWidget(scroll_area_to)


        scroll_area_from=QtGui.QScrollArea()
        scroll_area_from.setWidgetResizable(True)

        self.ConnectionWidget_from=ConnectionWidget(self.parent_editor,self,self.source,'tangential_from')
        scroll_area_from.setWidget(self.ConnectionWidget_from)
        

        vbox.addWidget(scroll_area_from)
        


        hbox_btns=QtGui.QHBoxLayout()

        hw = help_widget.HelpWidget(here+'/help_texts/connection_popup_tangential.html',"https://github.com/ilyasku/CompoundPye/wiki/Connection-Pop-ups#connections-of-tangential-cells")
        hbox_btns.addWidget(hw)


        hbox_btns.addStretch(1)

        btn_cancel=QtGui.QPushButton('cancel')
        btn_done=QtGui.QPushButton('done')

        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)

        hbox_btns.addWidget(btn_cancel)
        hbox_btns.addWidget(btn_done)

        vbox.addLayout(hbox_btns)


    def do_cancel(self):
        """
        Close this pop-up and all ConnectionWidgets it contains.
        """
        self.ConnectionWidget_to.do_cancel()
        self.ConnectionWidget_from.do_cancel()
        self.close()

    def do_done(self):
        """
        Close this pop-up and all ConnectionWidgets it contains, store the ConnectionWidgets' contents in the parent Editor's lists.
        """
        self.ConnectionWidget_to.do_done()
        self.ConnectionWidget_from.do_done()
        self.close()



class ConnectionWidget(QtGui.QWidget):
    """
    A widget that allows the user to choose targets of connections via combo-boxes and set the connections' weights.
    """

    def __init__(self,parent_editor,parent_PopupConnection,neuron_name,widget_mode='column'):
        """
        Initializes a ConnectionWidget.
        @param parent_editor Requires the parent Editor (or rather a pointer to it) of the 'PopupConnections'-object as input to access its lists of connections.
        @param parent_PopupConnection Requires the parent PopupConnections (or rather a pointer to it) as input to be able to call its remove-function.
        @param neuron_name Name of the neuron, required to read/write the neuron's connections from/to the lists of connections.
        @param widget_mode String to specify if this neuron is in a column (widget_mode=='column') or between columns (widget_mode=='next_neighbour').
        """
        super(ConnectionWidget,self).__init__()
        self.parent_editor=parent_editor
        self.parent_popup=parent_PopupConnection
        self.source=neuron_name
        self.widget_mode=widget_mode

        self.n=0
        #dummy_list=[('me',12,'huhnold')]
        #self.initial_connections=dummy_list
        self.initial_connections=[]

        n_deleted=0
        if widget_mode=='column':
            #print 'enter loop in COLUMN-mode'
            #loop_copy=self.parent_editor.connections['column'][:]
            
            for i in range(0,len(self.parent_editor.connections['column'])):
                #print 'i='+str(i)
                #print self.parent_editor.connections['column'][i-n_deleted]
                if self.parent_editor.connections['column'][i-n_deleted][0]==self.source:
                    self.initial_connections.append(self.parent_editor.connections['column'].pop(i-n_deleted))
                    n_deleted+=1
        elif widget_mode=='nn':
            
            for i in range(0,len(self.parent_editor.connections['next_neighbour'])):

                if self.parent_editor.connections['next_neighbour'][i-n_deleted][0]==self.source:
                    self.initial_connections.append(self.parent_editor.connections['next_neighbour'].pop(i-n_deleted))
                    n_deleted+=1

        elif widget_mode=='tangential_to':
            
            self.target=self.source
            self.source=None

            for i in range(0,len(self.parent_editor.connections['tangential_to'])):
                if self.parent_editor.connections['tangential_to'][i-n_deleted][2]==self.target:
                    self.initial_connections.append(self.parent_editor.connections['tangential_to'].pop(i-n_deleted))
                    n_deleted+=1
            
        elif widget_mode=='tangential_from':
            
            for i in range(0,len(self.parent_editor.connections['tangential_from'])):
                if self.parent_editor.connections['tangential_from'][i-n_deleted][0]==self.source:
                    self.initial_connections.append(self.parent_editor.connections['tangential_from'].pop(i-n_deleted))
                    n_deleted+=1

        #print 'column length after pop: '+str(len(self.parent_editor.connections['column']))
        #print 'next_neighbour length after pop: '+str(len(self.parent_editor.connections['next_neighbour']))
        self.connections=[]
        self.ConnectionEdit_list=[]

        self.init_UI(widget_mode)

        self.mode=widget_mode

    def init_UI(self,widget_mode):
        """
        Sets up all the widgets (buttons, labels, line-edits, etc) contained by this ConnectionWidget.
        @param widget_mode String to specify if this ConnectionWidget's neuron is in a column (widget_mode=='column') or between columns (widget_mode=='next_neighbour').
        """
        self.vbox=QtGui.QVBoxLayout()

        self.setLayout(self.vbox)

        self.n_list=[]
        if widget_mode=='column':
            for n in self.parent_editor.neurons['column']:
                #print n.values
                #print n.values['name']
                self.n_list.append(n.values['name'])

        else:
            if widget_mode=='nn':
                for key in self.parent_editor.neurons:
                    if key!='tangential':
                        for n in self.parent_editor.neurons[key]:
                            self.n_list.append(n.values['name'])
            elif widget_mode=='tangential_to':
                for key in self.parent_editor.neurons:
                    if key!='tangential':
                        for n in self.parent_editor.neurons[key]:
                            self.n_list.append(n.values['name'])

            else:
                for key in self.parent_editor.neurons:
                    for n in self.parent_editor.neurons[key]:
                        self.n_list.append(n.values['name'])

        hbox_add=QtGui.QHBoxLayout()
        

        if widget_mode=='column':
            btn_add=QtGui.QPushButton('add connection within column')
        elif widget_mode=='nn':
            btn_add=QtGui.QPushButton('add connection to neighbouring column')
        elif widget_mode=='tangential_to':
            btn_add=QtGui.QPushButton('add connection to this tangential cell')
        else:
            btn_add=QtGui.QPushButton('add connection from this tangential\nto any other cell')

        if self.widget_mode=='tangential_to':
            btn_add.clicked.connect(self.create_connect_edit_tangential_to)
        #elif self.widget_mode=='tangential_from':
            #btn_add.clicked.connect(self.create_connect_edit)
        else:
            btn_add.clicked.connect(self.create_connect_edit)
        
        hbox_add.addWidget(btn_add)
        hbox_add.addStretch(1)


        self.vbox.addLayout(hbox_add)
        self.vbox.addStretch(1)

        
        for i in range(0,len(self.initial_connections)):
            c=self.initial_connections[i]
            #print i
            if self.widget_mode=='tangential_to':
                self.create_connect_edit_tangential_to(c)
            elif self.widget_mode=='tangential_from':
                self.create_connect_edit(c[2],c[1])
            else:
                self.create_connect_edit(c[2],c[1])
            
    
    def create_connect_edit_tangential_to(self,connection=None):
        """
        Creates a ConnectionEditTangential widget.
        @param connection Tuple defining an initial connection.
        """
        if not (type(connection)==list or type(connection)==tuple):
            connection=('',1.0,self.target,'')
        print(connection)
        new_ConnectionEdit=ConnectionEditTangential(self,*connection)
        new_ConnectionEdit.index=self.n
        self.vbox.insertWidget(self.n,new_ConnectionEdit)
        self.connections.append(connection)
        self.ConnectionEdit_list.append(new_ConnectionEdit)
        self.n+=1


    def create_connect_edit(self,default_target='',default_weight=1.0):
        """
        Creates and adds a new line to the ConnectionWidget's connection editor.
        @param default_target Can be initialized with a target specified by this string.
        @param default_weight Can be initialized with a connection strength specified by this value.
        """
        new_ConnectionEdit=ConnectionEdit(self,default_target,default_weight)
        new_ConnectionEdit.index=self.n
        self.vbox.insertWidget(self.n,new_ConnectionEdit)
        #if default_target=='':
        self.connections.append((self.source,default_weight,default_target))
        #print 'added new connection to list!'
        self.ConnectionEdit_list.append(new_ConnectionEdit)
        self.n+=1

    def remove(self,i):
        """
        Remove line i in the ConnectionWidget editor window.
        @param i Index of the line to be removed.
        """
        item=self.vbox.itemAt(i)
        self.vbox.removeItem(item)
        self.n=self.vbox.count()-2
        self.connections.pop(i)
        self.ConnectionEdit_list.pop(i)
        for j in range(len(self.ConnectionEdit_list)):
            self.ConnectionEdit_list[j].index=j

    def do_cancel(self):
        """
        Discard all changes made in this ConnectionWidget's editor window.
        """
        if self.widget_mode=='column':
            mode=self.widget_mode
        elif self.widget_mode=='nn':
            mode='next_neighbour'
        elif self.widget_mode=='tangential_to':
            mode='tangential_to'
        else:
            mode='tangential_from'
        self.parent_editor.connections[mode]=self.parent_editor.connections[mode]+self.initial_connections
        #print mode +' length after cancel: '+str(len(self.parent_editor.connections[mode]))

    def do_done(self):
        """
        Store all changes made in this ConnectionWidget's editor window to the parent Editor's lists.
        """
        if self.widget_mode=='column':
            mode=self.widget_mode
        elif self.widget_mode=='nn':
            mode='next_neighbour'
        elif self.widget_mode=='tangential_to':
            mode='tangential_to'
        else:
            mode='tangential_from'
        self.parent_editor.connections[mode]=self.parent_editor.connections[mode]+self.connections
        #print mode +' length after cancel: '+str(len(self.parent_editor.connections[mode]))


class ConnectionEdit(QtGui.QWidget):
    """
    A widget that allows the user to choose a target of a connection via an combo-box and set the connection's weight.
    """
    def __init__(self,parent_ConnectionWidget,default_target,default_weight):
        """
        Initializes a 'ConnectionEdit'-object.
        @param parent_ConnectionWidget Requires the parent ConnectionWidget object on which this widget is shown, to access its members.
        @param default_target One must provide the name of the target or an empty string if this ConnectionEdit represents a new connection.
        @param default_weight One must provide the weight of the connection.
        """
        super(ConnectionEdit,self).__init__()
        self.parent_ConnectionWidget=parent_ConnectionWidget
        
        print(id(self.parent_ConnectionWidget.parent_editor.connections))

        self.index=0
        self.init_UI(default_target,default_weight)

    def init_UI(self,default_target,default_weight):
        """
        Sets up all widgets (line-edit, combo-box, button) shown on this 'ConnectionEdit'-widget.
        """
        hbox=QtGui.QHBoxLayout()
        self.setLayout(hbox)

        #lbl_target=QtGui.QLabel('target:')
        combo_target=QtGui.QComboBox()
        combo_target.addItem('choose target ...')

        for n in self.parent_ConnectionWidget.n_list:
            combo_target.addItem(n)


        if str(default_target)=='':

            index=0
        else:

            index=combo_target.findText(str(default_target))

        combo_target.setCurrentIndex(index)
        combo_target.activated[str].connect(self.edit_target)


        hbox.addWidget(combo_target)

        lbl_weight=QtGui.QLabel('weight')
        self.le_weight=QtGui.QLineEdit()
        self.le_weight.setText(str(default_weight))
        self.le_weight.editingFinished.connect(self.edit_weight)


        hbox.addWidget(lbl_weight)
        hbox.addWidget(self.le_weight)



        btn_remove=QtGui.QPushButton('remove')
        btn_remove.clicked.connect(self.do_remove)


        hbox.addWidget(btn_remove)

    def edit_target(self,s):
        """
        Read the combo-box specifying the target of this connection and change values in the lists accordingly.
        @param s String of the selected combo-box item.
        """
        c=list(self.parent_ConnectionWidget.connections[self.index])
        c[2]=s
        self.parent_ConnectionWidget.connections[self.index]=tuple(c)

    def edit_weight(self):
        """
        Read the weight-value from the 'LineEdit'-Widget and change the value in the connection-lists accordingly.
        """
        c=list(self.parent_ConnectionWidget.connections[self.index])
        #c[1]=float(self.le_weight.text())
        c[1]=str(self.le_weight.text())
        self.parent_ConnectionWidget.connections[self.index]=tuple(c)

    def do_remove(self):
        """
        Call the parent ConnectionWidget's remove-function (ConnectionWidget.remove) with this ConnectionEdit's index as parameter.
        """
        self.parent_ConnectionWidget.remove(self.index)
        self.close()


class ConnectionEditTangential(QtGui.QWidget):
    """
    Creates a Widget to define parameters of a connection.
    """

    def __init__(self,parent_ConnectionWidget,default_source,default_weight,default_target,default_parameters='-'):
        """
        Creates a ConnectionEditTangential object.
        @param parent_ConnectionWidget Parent ConnectionWidget (or rather a pointer to it).
        @param default_source Label of the default source neuron.
        @param default_weight Default weight.
        @param default_target Default target.
        @param default_parameters Default parameters string.
        """
        super(ConnectionEditTangential,self).__init__()
        self.parent_ConnectionWidget=parent_ConnectionWidget

        self.index=0
        self.init_UI(default_source,default_weight,default_parameters)

        
    def init_UI(self,default_source,default_weight,default_parameters):
        """
        Initializes all graphical elements shown in the ConnectionEditTangential widget.
        """
        hbox=QtGui.QHBoxLayout()
        self.setLayout(hbox)

        #lbl_source=QtGui.QLabel('source:')
        combo_source=QtGui.QComboBox()
        combo_source.addItem('choose source ...')

        for n in self.parent_ConnectionWidget.n_list:
            combo_source.addItem(n)


        if str(default_source)=='':

            index=0
        else:

            index=combo_source.findText(str(default_source))

        combo_source.setCurrentIndex(index)
        combo_source.activated[str].connect(self.edit_source)


        hbox.addWidget(combo_source)

        lbl_weight=QtGui.QLabel('weight')
        self.le_weight=QtGui.QLineEdit()
        self.le_weight.setText(str(default_weight))
        self.le_weight.editingFinished.connect(self.edit_weight)


        hbox.addWidget(lbl_weight)
        hbox.addWidget(self.le_weight)


        lbl_parameters=QtGui.QLabel('parameters')
        self.le_parameters=QtGui.QLineEdit(str(default_parameters))
        self.le_parameters.editingFinished.connect(self.edit_parameters)

        hbox.addWidget(lbl_parameters)
        hbox.addWidget(self.le_parameters)

        btn_remove=QtGui.QPushButton('remove')
        btn_remove.clicked.connect(self.do_remove)


        hbox.addWidget(btn_remove)

    def edit_parameters(self):
        """
        Passes changes made in the parameters line edit on to the connection dictionary.
        """
        c=list(self.parent_ConnectionWidget.connections[self.index])
        s=str(self.le_parameters.text())
        if s.isspace():
            s='-'
        if len(c)>3:
            c[3]=s
        else:
            c.append(s)
        self.parent_ConnectionWidget.connections[self.index]=tuple(c)


    def edit_source(self,s):
        """
        Read the combo-box specifying the target of this connection and change values in the lists accordingly.
        @param s String of the selected combo-box item.
        """
        c=list(self.parent_ConnectionWidget.connections[self.index])
        c[0]=s
        self.parent_ConnectionWidget.connections[self.index]=tuple(c)

    def edit_weight(self):
        """
        Read the weight-value from the 'LineEdit'-Widget and change the value in the connection-lists accordingly.
        """
        c=list(self.parent_ConnectionWidget.connections[self.index])
        #c[1]=float(self.le_weight.text())
        c[1]=str(self.le_weight.text())
        self.parent_ConnectionWidget.connections[self.index]=tuple(c)

    def do_remove(self):
        """
        Call the parent ConnectionWidget's remove-function (ConnectionWidget.remove) with this ConnectionEdit's index as parameter.
        """
        self.parent_ConnectionWidget.remove(self.index)
        self.close()
