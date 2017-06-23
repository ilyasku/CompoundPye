from PyQt4 import QtGui, QtCore
from .connection_widget import ConnectionWidget


class PopupConnections(QtGui.QWidget):
    """
    A widget in which the user can edit a neuron's connections.
    Pops up when the user hits the connection-button next to the button with a neuron's name on it.
    """
    def __init__(self, parent_editor, neuron_name):
        """
        Initializes a 'PopupConnection'-object.
        @param paren_Editor Requires a pointer to the parent 'Editor'-object of the 
        CompWidget which creates this PopupConnection (to read/write values to the 'Editor'-object).
        @param neuron_name Name of the neuron (required to find its connections 
        in the Editor's lists of connections).
        """
        super(PopupConnections, self).__init__()
        self.parent_editor = parent_editor
        self.source = neuron_name
        self.ConnectionWidgets_list = []
        self.init_UI()

    def init_UI(self):
        """
        Initializes all Widgets (labels,buttons,etc.) that are shown in this tab.
        """        
        self.resize(600, 400)
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        hbox_name = QtGui.QHBoxLayout()
        hbox_name.addStretch(1)
        lbl_name = QtGui.QLabel('connections of ' + self.source)
        hbox_name.addWidget(lbl_name)
        hbox_name.addStretch(1)
        vbox.addLayout(hbox_name)

        vsplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        scroll_area_top = QtGui.QScrollArea()
        scroll_area_top.setWidgetResizable(True)
        column_ConnectionWidget = ConnectionWidget(self.parent_editor, self,
                                                   self.source, 'column')
        scroll_area_top.setWidget(column_ConnectionWidget)
        self.ConnectionWidgets_list.append(column_ConnectionWidget)

        vsplitter.addWidget(scroll_area_top)
        
        scroll_area_middle = QtGui.QScrollArea()
        scroll_area_middle.setWidgetResizable(True)
        nn_ConnectionWidget = ConnectionWidget(self.parent_editor, self,
                                               self.source, 'nn')
        scroll_area_middle.setWidget(nn_ConnectionWidget)
        self.ConnectionWidgets_list.append(nn_ConnectionWidget)

        vsplitter.addWidget(scroll_area_middle)
        vbox.addWidget(vsplitter)

        if self.parent_editor.mode == 'column':
            hbox_receiver = QtGui.QHBoxLayout()
            checkbox_receiver = QtGui.QCheckBox("receive input from column's sensor")            
            if self.parent_editor.parent_EditorTabs.receiver.count(self.source):
                checkbox_receiver.toggle()
            checkbox_receiver.stateChanged.connect(self.set_receiver)
            hbox_receiver.addWidget(checkbox_receiver)
            vbox.addLayout(hbox_receiver)
        hbox_btns = QtGui.QHBoxLayout()
        hbox_btns.addStretch(1)
        btn_cancel = QtGui.QPushButton('cancel')
        btn_done = QtGui.QPushButton('done')
        btn_cancel.clicked.connect(self.do_cancel)
        btn_done.clicked.connect(self.do_done)
        hbox_btns.addWidget(btn_cancel)
        hbox_btns.addWidget(btn_done)
        vbox.addLayout(hbox_btns)

    def set_receiver(self, state):
        """
        Toggles whether the neuron receives direkt input of the column's sensor or not.
        @param state True or False == receive input or do not.
        """
        if state == QtCore.Qt.Checked:
            self.parent_editor.parent_EditorTabs.receiver.append(self.source)
        else:
            self.parent_editor.parent_EditorTabs.receiver.pop(
                self.parent_editor.parent_EditorTabs.receiver.index(self.source))

    def do_cancel(self):
        """
        Close this pop-up and all ConnectionWidgets it contains.
        """
        for w in self.ConnectionWidgets_list:
            w.do_cancel()
        self.close()

    def do_done(self):
        """
        Close this pop-up and all ConnectionWidgets it contains, store the 
        ConnectionWidgets' contents in the parent Editor's lists.
        """
        for w in self.ConnectionWidgets_list:
            w.do_done()
        self.close()
