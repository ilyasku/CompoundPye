from PyQt4 import QtGui


class ConnectionEdit(QtGui.QWidget):
    """
    A widget that allows the user to choose a target of a 
    connection via an combo-box and set the connection's weight.
    """
    def __init__(self, parent_ConnectionWidget,
                 default_target, default_weight):
        """
        Initializes a 'ConnectionEdit'-object.
        @param parent_ConnectionWidget Requires the parent ConnectionWidget object 
        on which this widget is shown, to access its members.
        @param default_target One must provide the name of the target or an empty 
        string if this ConnectionEdit represents a new connection.
        @param default_weight One must provide the weight of the connection.
        """
        super(ConnectionEdit, self).__init__()
        self.parent_ConnectionWidget = parent_ConnectionWidget        
        self.index = 0
        self.init_UI(default_target, default_weight)

    def init_UI(self, default_target, default_weight):
        """
        Sets up all widgets (line-edit, combo-box, button) shown on this 'ConnectionEdit'-widget.
        """
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)

        combo_target = QtGui.QComboBox()
        combo_target.addItem('choose target ...')
        for n in self.parent_ConnectionWidget.n_list:
            combo_target.addItem(n)

        if str(default_target) == '':
            index = 0
        else:
            index = combo_target.findText(str(default_target))
        combo_target.setCurrentIndex(index)
        combo_target.activated[str].connect(self.edit_target)
        hbox.addWidget(combo_target)
        lbl_weight = QtGui.QLabel('weight')
        self.le_weight = QtGui.QLineEdit()
        self.le_weight.setText(str(default_weight))
        self.le_weight.editingFinished.connect(self.edit_weight)
        
        hbox.addWidget(lbl_weight)
        hbox.addWidget(self.le_weight)

        btn_remove = QtGui.QPushButton('remove')
        btn_remove.clicked.connect(self.do_remove)

        hbox.addWidget(btn_remove)
        
    def edit_target(self, s):
        """
        Read the combo-box specifying the target of this connection and 
        change values in the lists accordingly.
        @param s String of the selected combo-box item.
        """
        c = list(self.parent_ConnectionWidget.connections[self.index])
        c[2] = s
        self.parent_ConnectionWidget.connections[self.index] = tuple(c)

    def edit_weight(self):
        """
        Read the weight-value from the 'LineEdit'-Widget and 
        change the value in the connection-lists accordingly.
        """
        c = list(self.parent_ConnectionWidget.connections[self.index])
        c[1] = str(self.le_weight.text())
        self.parent_ConnectionWidget.connections[self.index] = tuple(c)

    def do_remove(self):
        """
        Call the parent ConnectionWidget's remove-function (ConnectionWidget.remove) 
        with this ConnectionEdit's index as parameter.
        """
        self.parent_ConnectionWidget.remove(self.index)
        self.close()
