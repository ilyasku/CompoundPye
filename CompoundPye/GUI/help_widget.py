from PyQt4 import QtGui

import webbrowser

import os
here=os.path.dirname(os.path.abspath(__file__))

style_help_button="""background-color: rgb(20,20,240);
color: white;
font-weight: bold;"""

style_wiki_button="""background-color: black;
color: white;
font-weight: bold;"""



class WikiBtn(QtGui.QPushButton):

    def __init__(self,wiki_url):
        super(WikiBtn,self).__init__("wiki page")

        self.setStyleSheet(style_wiki_button)
        self.setIcon(QtGui.QIcon(here+"/icons/GitHub-Mark-Light.png"))
        self.clicked.connect(lambda: webbrowser.open(wiki_url))


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
        #msg=QtGui.QMessageBox.information(self, "Help Window", text, "If you say so!")
        dialog=Dialog(self,text)
        dialog.exec_()


class Dialog(QtGui.QDialog):

    def __init__(self,parent,text,title="Help window"):
        
        super(Dialog,self).__init__(parent)

        self.init_UI(text,title)

    def init_UI(self,text,title):

        self.setStyleSheet("""background-color: rgb(244,244,244);
""")


        self.setWindowTitle(title)

        vbox=QtGui.QVBoxLayout()
        self.setLayout(vbox)

        te=QtGui.QTextEdit()
        te.setReadOnly(True)
        te.setHtml(text)

        te.setStyleSheet(""" background-color: rgb(242,242,242);
color: black;
border: black solid 10px;
""")
        
        vbox.addWidget(te)

        btn_OK=QtGui.QPushButton("If you say so!")
        btn_OK.clicked.connect(self.done)
        btn_OK.setStyleSheet("""background-color: rgb(40,40,180);
color: white;
font-weight: bold;""")


        hbox_btn=QtGui.QHBoxLayout()
        hbox_btn.addStretch(1)
        hbox_btn.addWidget(btn_OK)
        vbox.addLayout(hbox_btn)


