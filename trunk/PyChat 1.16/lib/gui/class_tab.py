#-*-coding: utf-8 -*-
'''
Created on 07.03.2011

@author: anon
'''
from PyQt4 import QtGui

class TAB(QtGui.QWidget):

    obj_mainWin = None
    obj_parent = None
    
    def CreateDebugWindow(self):
        self.Debug_Window = QtGui.QMainWindow()
        self.Debug_Window.centralWidget = QtGui.QWidget(self.Debug_Window);
        self.Debug_Window.gridLayout = QtGui.QGridLayout(self.Debug_Window.centralWidget);
        self.Debug_Window.gridLayout.setSpacing(6);
        self.Debug_Window.gridLayout.setContentsMargins(11, 11, 11, 11);
        self.Debug_Window.textEdit = QtGui.QPlainTextEdit(self.Debug_Window.centralWidget);
        self.Debug_Window.gridLayout.addWidget(self.Debug_Window.textEdit, 0, 0, 1, 1)
        self.Debug_Window.setCentralWidget(self.Debug_Window.centralWidget);
        self.Debug_Window.show()
        
    def AddDebug(self,text): self.Debug_Window.textEdit.insertPlainText('\n\n'+text_p+'\n')
    
    def tab_close_sig(self,i): pass ;#print 'Req close %s tab' % (i)
        
    def tab_GetName(self): return self.obj_parent.tabText(self.tab_GetSelfNum())
    
    def tab_SetName(self,name): self.obj_parent.setTabText(self.tab_GetSelfNum(),name)
    
    def tab_GetSelfNum(self): return self.obj_parent.indexOf(self)
    
    def OnClose(self,i): 
        pass
        #print "Close tab %s - %s" % (i,self.tab_GetName())
    
    def tab_SetIcon_Modifed(self):
        self.obj_parent.setTabIcon(self.tab_GetSelfNum(),self.obj_mainWin.icon_new_message)
        
    def tab_SetIcon_None(self):
        self.obj_parent.setTabIcon(self.tab_GetSelfNum(),QtGui.QIcon())
        
    def tab_IsActive(self):
        if self.obj_parent.currentIndex() == self.tab_GetSelfNum():
            return True
        else:
            return False
    def tab_OnActive(self,i=None):
        pass
        #print 'Active %s - %s ' % (self.tab_GetSelfNum(),self.tab_GetName())