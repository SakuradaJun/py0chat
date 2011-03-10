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
        
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('res/main.ui',self)
                
        self.icon_new_message.addPixmap(QtGui.QPixmap('res/Images/mail-unread-new.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon_main.addPixmap(QtGui.QPixmap('res/Images/icon_16.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon_main)
        
        #self.chat_tabs.i
        self.originalPalette = QtGui.QApplication.palette()
        #self.changeStyle('GTK+')
        self.setStyleSheet(ReadFile('res/style/chat_message.css'))
        
        #self.chat_tabs.tabBar()
        QtGui.QApplication.setApplicationName(GLOBAL_VARS['window_title'])
        self.setWindowTitle(GLOBAL_VARS['window_title'])
        self.SetUpSignals()
        self.widget_Top.hide()

        self.show()
        self.CONF_O.Load()
        self.P.LoadPlugins(self)
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
        
        self.CreateTab(1)
        self.CreateTab(2)
        
        #self.CreateTab('0chan',('0chan.ru',1984,'http://0chan.ru/0chat'))
        #self.CreateTab('py-chat',('py-chat.tk',1984,'http://py-chat.tk'))
        #self.CreateTab('py-chat',('py-chat.tk',1984,'http://py-chat.tk'))
        #self.CreateTab('py-chat',('py-chat.tk',1984,'http://py-chat.tk'))
        #self.CreateTab('py-chat',('py-chat.tk',1984,'http://py-chat.tk'))
        #self.CreateTab('py-chat',('py-chat.tk',1984,'http://py-chat.tk'))
        
    def closeEvent(self, event): 
        c = self.chat_tabs.count()
        for x in xrange(0,c):
            self.chat_tabs.widget(x).OnClose(x)
        CONF_O.Save(); 
        app.quit();
        
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
    app =  QtGui.QApplication(sys.argv)
    CONF_O = Config()
    PLUGINH_O = PluginHandler()
    Chat_o = Chat()
    app.exec_()
