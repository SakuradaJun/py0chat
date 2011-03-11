#!/usr/bin/python
#-*-coding: utf-8 -*-
'''
Created on 02.03.2011

@author: anon
'''
#pyrcc4 -o resources.py resources.qrc
from lib.utilits import *
CONF_O = None
P = None
GLOBAL_VARS={'window_title':'PyChat 1.16 (dbg,plugin)'}

#try:
import sys
import os
from PyQt4 import QtCore, QtGui, uic
#import pysideuic
from lib.class_Config import Config
from lib.class_plugin_core import PluginHandler
from lib.class_ChatConnection import ChatConnection
from lib.gui.class_tab_connection import TAB_Connection
from lib.gui.class_word_filter import WordFilter_Widget
#except Exception,err:
    #print str(err)
    #sys.exit()
#TODO: Проверка новых версий svn на гугле файл
'''
 >>32056 Вордфильтр, удобный, с возможностью выделить слово и внести его туда, Ня!=^_^=. 
 Блок одним кликом, функция обрезания постов больше n длинны, Ня!=^_^=. 
 Возможность игнора всех символов кроме латиницы и кириллицы, Ня!=^_^=.
 Всплывающие окна, оповещение о смене онлайна, Ня!=^_^=.
 Ах да, ещё хоткеи, Ня!=^_^=.
 Игнор капса, Ня!=^_^=.
 
 Сохранить буфер сообщений чята в файл
'''

class Chat(QtGui.QMainWindow):
    
    paths = {'config_dir':'./'}
    tabs = []
    icon_new_message = QtGui.QIcon()
    icon_main = QtGui.QIcon()
    icons_conn = []
    
    def __init__(self):
        self.paths['config_dir'] = script_dir; CONF_O.paths = self.paths
        self.P = PLUGINH_O
        self.CONF_O = CONF_O
        
        if False: 
            self.chat_tabs = QtGui.QTabWidget()
            self.tab_bar = QtGui.QTabBar()
        super(Chat,self).__init__()
        uic.loadUi('res/main.ui',self)
            
        self.icon_new_message.addPixmap(QtGui.QPixmap('res/Images/mail-unread-new.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon_main.addPixmap(QtGui.QPixmap('res/Images/icon_16.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon_main)
        qapp.setWindowIcon(self.icon_main)
        
        #self.chat_tabs.i
        self.originalPalette = QtGui.QApplication.palette()
        #self.changeStyle('GTK+')
        #self.setStyleSheet(ReadFile())
        
        #self.chat_tabs.tabBar()
        QtGui.QApplication.setApplicationName(GLOBAL_VARS['window_title'])
        self.setWindowTitle(GLOBAL_VARS['window_title'])
        self.SetUpSignals()
        self.widget_Top.hide()
        self.show()
        
        self.CONF_O.Load()
        self.P.LoadPlugins(self)
        
        
        #self.installEventFilter(self)
        #print QtGui.QMainWindow.__subclasses__()
        
        #self.connect(self.Button_Connect, QtCore.SIGNAL("clicked()"), lambda x=0: Plugin_CMD(('connect','0chan')) )
        #self.chat_tabs.removeTab(0)
        #self.chat_tabs.removeTab(0)
        #self.CreateTab()
        #self.CreateTab()
        #self.timer = QtCore.QTimer()
        #self.timer.start(2300)
        #self.connect(self.timer, QtCore.SIGNAL("timeout()"), lambda: self.P.Event('chat_message', None) )
        #self.chat_tabs.changeEvent_OLD = self.chat_tabs.changeEvent
        #self.CreateTab(1).AddText(u'[20:39:39] <b>&lt;<a href="event:insert,28793"><font color="#000000">28793</font></a></b><b>&gt;</b> Test ТЕСТ')
        self.CreateTab(1)
        self.CreateTab(2)
        #o = WebKitStyle()
        #print WebKitStyle.Build()
        
    def keyReleaseEvent(self,event):
        if event.key() == QtCore.Qt.Key_F11:
            self.emit(QtCore.SIGNAL('main_win_miniStyle()'))
        QtGui.QMainWindow.keyReleaseEvent(self,event)
        
    def eventFilter(self,Qobj, event):
        #TODO: not work: TypeError: invalid result type from Chat.eventFilter()
        '''If you delete the receiver object in this function, be sure to return true. Otherwise, 
        Qt will forward the event to the deleted object and the program might crash.'''
        #return (Qobj, event)
        #super(Chat,self).eventFilter(Qobj, event)
        #super(QMainWindow, self).eventFilter(Qobj, event)
        #return qapp.eventFilter(Qobj, event)
        #return QtGui.QMainWindow.eventFilter(self,Qobj, event)
        #return QtCore.QObject.eventFilter(Qobj, event)
        #return QtGui.QMainWindow.eventFilter(Qobj, event)
        #return Chat.eventFilter(Qobj, event)
        return
        if Qobj == self and event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_F11):
                print 'F11 press'
                self.emit(QtCore.SIGNAL('main_win_miniStyle()'))
                return True
        
    
    def closeEvent(self, event): 
        c = self.chat_tabs.count()
        for x in xrange(0,c):
            self.chat_tabs.widget(x).OnClose(x)
        CONF_O.Save(); 
        qapp.quit();
        
    def WordFilterWindow(self):
        WordFilter_Widget().exec_()
    
    def GET_icons(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtCore.QUrl('http://py-chat.tk/favicon.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icons_conn.append(icon)
        self.setWindowIcon(icon)
        
    def changeStyle(self, styleName, Load = False):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(styleName))
        CONF_O.settings['view']['style'] = styleName
        if Load != True:
            self.changePalette()  
    
    def changePalette(self):
        #if CONF_O.settings in ['style_color']['originalPalette']:
        #    QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        #else:
        QtGui.QApplication.setPalette(self.originalPalette)
        
                
    def setWindowTitle(self,title):
        #QtGui.QMainWindow.setWindowTitle(title)
        QtGui.QMainWindow.setWindowTitle(self,title+' [*]')
        #self.setWindowTitle(QtGui.QApplication.translate("MainWindow", gloal_windowsTitle+" - "+conf_o.settings['servers'][conf_o.settings['current_server']]['host']+":"+str(conf_o.settings['servers'][conf_o.settings['current_server']]['port']), None, QtGui.QApplication.UnicodeUTF8))
    
    def SetUpSignals(self): 
        self.connect(self.Button_NewTab, QtCore.SIGNAL("clicked()"), lambda: self.CreateTab() )
        self.connect(self.chat_tabs, QtCore.SIGNAL("currentChanged(int)"), lambda i: self.setWindowTitle(GLOBAL_VARS['window_title']+' - '+self.chat_tabs.tabText(i)) )
        self.connect(self.chat_tabs, QtCore.SIGNAL("tabCloseRequested(int)"), self.CloseTAB )

    def CloseTAB(self,i):
        self.chat_tabs.widget(i).OnClose(i)
        self.chat_tabs.removeTab(i)
        
    def CreateTab(self,connIndex=None,TabName='',conn_par=None,IsAutoConn=False):
        tab = TAB_Connection()
        self.chat_tabs.addTab(tab, TabName)
        tab.init_TWO(connIndex,conn_par, self, IsAutoConn)
        #self.tabs.append(tab)
        return tab

    def eventFilter(self,Qobj, event):
        pass
    
if __name__ == '__main__':
    #os.system('clear')
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(script_dir)
    qapp =  QtGui.QApplication(sys.argv)
    CONF_O = Config()
    PLUGINH_O = PluginHandler()
    Chat_o = Chat()
    qapp.exec_()
