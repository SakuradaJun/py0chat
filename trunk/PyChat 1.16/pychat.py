#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 02.03.2011 
@author: anon <index4376867067@yandex.ru>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
   
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
   
    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    MA 02110-1301, USA.
'''
#Create pyrc: pyrcc4 -o resources.py resources.qrc

CONF_O = None
P = None
GLOBAL_VARS={'window_title':'PyChat 1.16 (dbg,plugin)'}

import gc
gc.enable()
#gc.set_debug(gc.DEBUG_STATS)
import sys
import os
from PyQt4 import QtCore, QtGui, uic
from lib.utilits import *
from lib.class_Config import Config
from lib.class_plugin_core import PluginHandler
from lib.class_ChatConnection import ChatConnection
from lib.gui.class_tab_connection import TAB_Connection
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
    
    paths = {'config_dir':os.path.abspath('./')}
    tabs = []
    icon_new_message = QtGui.QIcon()
    icon_main = QtGui.QIcon()
    icons_conn = []
    
    def __init__(self):
        super(Chat,self).__init__()        
        self.P = PLUGINH_O
        self.CONF_O = CONF_O
        self.CONF_O.paths = self.paths
        
        if False: # Hack for eclipse IDE 
            self.chat_tabs = QtGui.QTabWidget()
            self.tab_bar = QtGui.QTabBar()
            
        self.SetupUI()
        
        self.CONF_O.Load()
        self.P.LoadPlugins(self)
        self.CreateTab(1)
        self.CreateTab(2)
        
    def SetupUI(self):
        uic.loadUi('res/main.ui',self)
        self.icon_new_message.addPixmap(QtGui.QPixmap('res/Images/mail-unread-new.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon_main.addPixmap(QtGui.QPixmap('res/Images/icon_16.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon_main)
        qapp.setWindowIcon(self.icon_main)
        
        self.originalPalette = QtGui.QApplication.palette()
        #qapp.setStyleSheet(WebKitStyle.getAppStyle())
        
        
        QtGui.QApplication.setApplicationName(GLOBAL_VARS['window_title'])
        self.setWindowTitle(GLOBAL_VARS['window_title'])
        self.SetUpSignals()
        self.widget_Top.hide()
        
        self.action_GetGetter = QtGui.QAction(self)
        self.action_GetGetter.setText('Get...')
        self.action_GetGetter.setShortcut("Ctrl+`")
        def CurrentTabGet_exec():
            tab_w = self.chat_tabs.currentWidget()
            if hasattr(tab_w, 'GET'):
                tab_w.GET()

        self.action_GetGetter.triggered.connect(lambda: self.chat_tabs.currentWidget().GET())
        #self.chat_tabs.tabBar().addAction(self.action_GetGetter)
        #self.CreateTrayIcon()
        self.action_SwitchMiniStyle.triggered.connect(lambda b: self.emit(QtCore.SIGNAL("SwitchMiniStyle(bool)"),b))
        #self.connect(self, QtCore.SIGNAL("SwitchMiniStyle(bool)"), lambda x='Empty': Debug.debug(x) )
        
        self.addAction(self.action_GetGetter)
        self.addAction(self.action_SwitchMiniStyle)
        self.show()
        
    def CreateTrayIcon(self):
        self.trayIcon = QtGui.QSystemTrayIcon(self.icon_main)
        
        self.trayIconMenu = QtGui.QMenu(self)
        
        self.trayIconMenu.addAction(self.action_test)
        self.trayIconMenu.addAction(self.action_SwitchMiniStyle)
        
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()
        return
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addAction(self.action_about)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
         
        
    def closeEvent(self, event): 
        c = self.chat_tabs.count()
        for x in xrange(0,c):
            self.chat_tabs.widget(x).OnClose(x)
        CONF_O.Save(); 
        qapp.quit();
        
    def WordFilterWindow(self): WordFilter_Widget().exec_()
    
    def GET_icons(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtCore.QUrl('http://py-chat.tk/favicon.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icons_conn.append(icon)
        self.setWindowIcon(icon)
        
    def changeStyle(self, styleName, Load = False):
        qapp.setStyle(QtGui.QStyleFactory.create(styleName))
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
    

if __name__ == '__main__':
    #os.system('clear')
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(script_dir)    
    if 1:
        qapp =  QtGui.QApplication(sys.argv)
        #qapp.setStyle("Plastique")
        #qapp.setPalette(QtGui.QApplication.style().standardPalette())
        CONF_O = Config()
        PLUGINH_O = PluginHandler()
        Chat_o = Chat()
    else:
        wf_o = WordFiler_DotNET()
        wf_o.load()
        print wf_o.FilterMessage('Test Ня?=^_^= test')
        sys.exit()
    sys.exit(qapp.exec_())
