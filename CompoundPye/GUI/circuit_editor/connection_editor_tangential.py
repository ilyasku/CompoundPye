from PyQt4 import QtGui


class ConnectionEditTangential(QtGui.QWidget):
    """
    Creates a Widget to define parameters of a connection.
    """

    def __init__(self, parent_ConnectionWidget, default_source,
                 default_weight, default_target, default_parameters='-'):
        """
        Creates a ConnectionEditTangential object.
        @param parent_ConnectionWidget Parent ConnectionWidget (or rather a pointer to it).
        @param default_source Label of the default source neuron.
        @param default_weight Default weight.
        @param default_target Default target.
        @param default_parameters Default parameters string.
        """
        super(ConnectionEditTangential, self).__init__()
        self.parent_ConnectionWidget = parent_ConnectionWidget
        self.index = 0
        self.init_UI(default_source, default_weight, default_parameters)
        
    def init_UI(self, default_source, default_weight, default_parameters):
        """
        Initializes all graphical elements shown in the ConnectionEditTangential widget.
        """
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)

        # lbl_source=QtGui.QLabel('source:')
        combo_source = QtGui.QComboBox()
        combo_source.addItem('choose source ...')
        for n in self.parent_ConnectionWidget.n_list:
            combo_source.addItem(n)

        if str(default_source) == '':
            index = 0
        else:
            index = combo_source.findText(str(default_source))
        combo_source.setCurrentIndex(index)
        combo_source.activated[str].connect(self.edit_source)
        hbox.addWidget(combo_source)
        lbl_weight = QtGui.QLabel('weight')
        self.le_weight = QtGui.QLineEdit()
        self.le_weight.setText(str(default_weight))
        self.le_weight.editingFinished.connect(self.edit_weight)
        hbox.addWidget(lbl_weight)
        hbox.addWidget(self.le_weight)

        lbl_parameters = QtGui.QLabel('parameters')
        self.le_parameters = QtGui.QLineEdit(str(default_parameters))
        self.le_parameters.editingFinished.connect(self.edit_parameters)

        hbox.addWidget(lbl_parameters)
        hbox.addWidget(self.le_parameters)

        btn_remove = QtGui.QPushButton('remove')
        btn_remove.clicked.connect(self.do_remove)
        hbox.addWidget(btn_remove)

    def edit_parameters(self):
        """
        Passes changes made in the parameters line edit on to the connection dictionary.
        """
        c = list(self.parent_ConnectionWidget.connections[self.index])
        s = str(self.le_parameters.text())
        if s.isspace():
            s = '-'
        if len(c) > 3:
            c[3] = s
        else:
            c.append(s)
        self.parent_ConnectionWidget.connections[self.index] = tuple(c)

    def edit_source(self, s):
        """
        Read the combo-box specifying the target of this connection and 
        change values in the lists accordingly.
        @param s String of the selected combo-box item.
        """
        c = list(self.parent_ConnectionWidget.connections[self.index])
        c[0] = s
        self.parent_ConnectionWidget.connections[self.index] = tuple(c)

    def edit_weight(self):
        """
        Read the weight-value from the 'LineEdit'-Widget 
        and change the value in the connection-lists accordingly.
        """
        c = list(self.parent_ConnectionWidget.connections[self.index])        
        c[1] = str(self.le_weight.text())
        self.parent_ConnectionWidget.connections[self.index] = tuple(c)

    def do_remove(self):
        """
        Call the parent ConnectionWidget's remove-function 
        (ConnectionWidget.remove) with this ConnectionEdit's index as parameter.
        """
        self.parent_ConnectionWidget.remove(self.index)
        self.close()
