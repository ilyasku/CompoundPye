from PyQt4 import QtGui

import webbrowser

import os
here=os.path.dirname(os.path.abspath(__file__))

style_help_button="""background-color: blue;
color: white;
font-weight: bold;"""

style_wiki_button="""background-color: black;
color: white;
font-weight: bold;"""


class HelpWidget(QtGui.QWidget):

    def __init__(self,hlp_text_file,wiki_url):
        super(HelpWidget,self).__init__()

        self.init_UI(hlp_text_file,wiki_url)

    def init_UI(self,hlp_text_file,wiki_url):
    
        if hlp_text_file:
            hlp_text=open(hlp_text_file,'r').read()
        else:
            hlp_text=''

        hbox=QtGui.QHBoxLayout()
        self.setLayout(hbox)

        btn_help=QtGui.QPushButton("help")
        btn_help.setStyleSheet(style_help_button)
        btn_help.setIcon(QtGui.QIcon(here+"/icons/question.svg"))
        btn_help.clicked.connect(lambda: self.show_message_box(hlp_text))
        hbox.addWidget(btn_help)

        btn_wiki=QtGui.QPushButton("wiki page")
        btn_wiki.setStyleSheet(style_wiki_button)
        btn_wiki.setIcon(QtGui.QIcon(here+"/icons/GitHub-Mark-Light.png"))
        btn_wiki.clicked.connect(lambda: webbrowser.open(wiki_url))
        hbox.addWidget(btn_wiki)

        hbox.addStretch(1)

    def show_message_box(self,text):
        msg=QtGui.QMessageBox.information(self, "Help Window", text, "If you say so!")
