#-*-coding: utf-8 -*-
from Radio import *
import sys
from PyQt4.QtGui import QApplication
from Configuration_win import *
from Main_win import *
from Popup import *
from ImageWindow import *

app =  QApplication(sys.argv)

class MessageBox(QtGui.QMessageBox):
    
    def __init__(self,text = "Message Here",title = u'Сообщение:',type = QtGui.QMessageBox.NoIcon):
        super(QtGui.QMessageBox, self).__init__(None)
        self.setText(text)
        self.setIcon(type); 
        self.setWindowTitle(title)
        self.exec_()

# хуита для тестов
class dial (QtGui.QStackedWidget):
    
    def __init__(self,parent=None):
       
       super(QtGui.QStackedWidget, self).__init__(parent)
       #self.stackedWidget = QtGui.QStackedWidget(self)
       self.Label_Test = QtGui.QLabel(self)
       self.Label_Test.setText('ТЕСТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТТ!')
       
       self.Messages = ChatPlainTextEdit(self)
       #self.stackedWidget.addWidget()
       self.show()
    
#from PyQt4 import QtGui, uic
#Window_From_UI = uic.loadUi('gui/demo.ui')