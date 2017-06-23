import os
here = os.path.dirname(os.path.abspath(__file__))
from PyQt4 import QtGui
from .connection_widget import ConnectionWidget
from ..help_widget import HelpWidget


class PopupConnectionsTangential(QtGui.QWidget):
    """
    Widget to edit a tangential cells connections, or rather the connections to this cell.
    Very similar to the PopupConnections class, only with two different features:
       - connections need to be specified from any cell to this 
         (tangential) cell rather than the other way around
       - some more parameters (for axis and direction) can be specified in a line edit.
    """
    def __init__(self, parent_editor, neuron_name):
        """
        Initializes a 'PopupConnection'-object.
        @param paren_Editor Requires a pointer to the parent 'Editor'-object 
        of the CompWidget which creates this PopupConnection 
        (to read/write values to the 'Editor'-object).
        @param neuron_name Name of the neuron (required to find its 
        connections in the Editor's lists of connections).
        """
        super(PopupConnectionsTangential, self).__init__()
        self.parent_editor = parent_editor
        self.source = neuron_name
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
        scroll_area_to = QtGui.QScrollArea()
        scroll_area_to.setWidgetResizable(True)
        self.ConnectionWidget_to = ConnectionWidget(self.parent_editor, self,
                                                    self.source, 'tangential_to')
        scroll_area_to.setWidget(self.ConnectionWidget_to)        
        vbox.addWidget(scroll_area_to)

        scroll_area_from = QtGui.QScrollArea()
        scroll_area_from.setWidgetResizable(True)

        self.ConnectionWidget_from = ConnectionWidget(self.parent_editor, self,
                                                      self.source, 'tangential_from')
        scroll_area_from.setWidget(self.ConnectionWidget_from)        
        vbox.addWidget(scroll_area_from)

        hbox_btns = QtGui.QHBoxLayout()
        help_widget = HelpWidget(here + '/help_texts/connection_popup_tangential.html',
                                 "https://github.com/ilyasku/CompoundPye/wiki/Connection-Pop-ups#connections-of-tangential-cells")
        hbox_btns.addWidget(help_widget)
        hbox_btns.addStretch(1)
        btn_cancel = QtGui.QPushButton('cancel')
        btn_done = QtGui.QPushButton('done')

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
        Close this pop-up and all ConnectionWidgets it contains, store 
        the ConnectionWidgets' contents in the parent Editor's lists.
        """
        self.ConnectionWidget_to.do_done()
        self.ConnectionWidget_from.do_done()
        self.close()
