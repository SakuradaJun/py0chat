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


import __builtin__
__builtin__.G = {}
G = __builtin__.G

G['QAPP'] = None
G['version'] = ['1.16','Alpha',True]
G['plugin_o'] = object
G['script_dir'] = './'
G['config'] = object
G['chat_win'] = object
G['version'] = ['1.16','Alpha',True]
G['msg_counter'] = [0,0]

import gc
gc.enable()
#gc.set_debug(gc.DEBUG_STATS)
import sys
import os
#import thread
from PyQt4 import QtCore, QtGui, uic
from lib.utilits import *
from lib.class_Config import Config
from lib.class_plugin_core import PluginHandler
from lib.class_ChatConnection import ChatConnection
from lib.gui.class_tab_connection import TAB_Connection
from lib.gui.class_tab_web import TAB_web
from lib.gui.class_tray import Tray
from lib.gui import *
import res_

#Create pyrc: pyrcc4 -o resources.py resources.qrc
# TODO: блокирование через контенстное меню, правая кнопка на постид -> меню-блоикровать
#TODO: Проверка новых версий svn на гугле файл
'''
Подсветка сових постов.
Реконнект py-chat.tk

 >>32056 Вордфильтр, удобный, с возможностью выделить слово и внести его туда. 
 Блок одним кликом, функция обрезания постов больше n длинны. 
 Возможность игнора всех символов кроме латиницы и кириллицы.
 Всплывающие окна, оповещение о смене онлайна.
 Ах да, ещё хоткеи.
 Игнор капса.
 
 Сохранить буфер сообщений чята в файл
ПРИ СБОРКЕ ПОД ВЕНДУ ЧЕРЕЗ PY2EXE заменить в ui файлах <header>QtWebKit/QWebView</header> на
<header>PyQt4.QtWebKit</header>
'''

class Chat(QtGui.QMainWindow):
    
    tabs = []
    icon_new_message = QtGui.QIcon()
    icon_main = QtGui.QIcon()
    icons_conn = []
    defTitle = None
    
    def init_vars(self):        
        if G['version'][2]:
            self.defTitle = 'PyChat %s %s DEBUG' % (G['version'][0],G['version'][1])
        else:
            self.defTitle = 'PyChat %s %s DEBUG' % (G['version'][0],G['version'][1])
        self.originalPalette = QtGui.QApplication.palette()
        
    def __init__(self):
        if False:
            self.chat_tabs = QtGui.QTabBar
        G['chat_win'] = self
        super(Chat,self).__init__()        
        self.init_vars()    
        self.SetupUI()
        
        G['config'].Load()
        self.changeStyle(G['config'].settings['view']['style'])
        self.action_ShowPopup.setChecked(bool(G['config'].settings['showpopupmsg']))
        self.show()
        G['plugin_o'].LoadPlugins(self)
        
        
        self.titleUpdater = QtCore.QTimer()
        self.titleUpdater.setInterval(1000)
        QtCore.QObject.connect(self.titleUpdater, QtCore.SIGNAL("timeout()"), self.titleUpdate)
        self.titleUpdater.start()
        
        G['QAPP'].installEventFilter(self)
        self.CreateTab(1)
    
    
    def titleUpdate(self):
        
        
        title = self.defTitle
        tabTitle = self.chat_tabs.tabText(self.chat_tabs.currentIndex())
        title += ' - ' + tabTitle
        
        if G['msg_counter'][0] != 0:
            title = 'MSG: '+str(G['msg_counter'][0]) + ' ' + title

            
        self.setWindowTitle(title)
    
    def eventFilter(self, ob, ev):
        if False: 
            ev = QtCore.QEvent()
            
        t = ev.type()
        if t > 100 and t < 200:
            if t in (121,):
                G['msg_counter'][0] = 0
                self.titleUpdate()

        return False  
      
    def SetupUI(self):
        uic.loadUi('res/main.ui',self)
        self.setToolTip("")
        
        self.menubar.hide()
        self.icon_new_message.addPixmap(QtGui.QPixmap('res/Images/mail-unread-new.png'), QtGui.QIcon.Normal, 
                                        QtGui.QIcon.Off)
        self.icon_main.addPixmap(QtGui.QPixmap('res/Images/icon_16.png'), QtGui.QIcon.Normal, 
                                 QtGui.QIcon.Off)

        self.setWindowIcon(self.icon_main)
        G['QAPP'].setWindowIcon(self.icon_main)

        
        self.CreateTrayIcon()
        QtGui.QApplication.setApplicationName(self.defTitle)
        self.titleUpdate()
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

        
        self.action_SwitchMiniStyle.triggered.connect(lambda b: self.emit(QtCore.SIGNAL("SwitchMiniStyle(bool)"),b))

        self.action_App_quit.triggered.connect(self.close)

        
        self.addAction(self.action_App_quit)
        self.addAction(self.action_GetGetter)
        self.addAction(self.action_SwitchMiniStyle)
        
        
        
        self.beznogo_check = QtGui.QAction(u'БE3HOГNM',self)
        self.beznogo_check.setCheckable(True)
        self.beznogo_check.toggle()
        self.beznogo_check.setChecked(False)
        
        self.action_ShowPopup.setCheckable(True)
        def update_showpopupmsg(b):
            G['config'].settings['showpopupmsg'] = b
        self.action_ShowPopup.triggered.connect(update_showpopupmsg)
        self.addAction(self.action_ShowPopup)
        
        # Add to tray
        self.trayIconMenu.addAction(self.action_SwitchMiniStyle)
        self.trayIconMenu.addAction(self.action_ShowPopup)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.action_App_quit)
        
        
    def CreateTrayIcon(self):
        self.trayIcon = QtGui.QSystemTrayIcon(self.icon_main)
        self.trayIcon.showMessage("sdf","df")
        self.trayIcon.setToolTip("sdf")
        self.trayIconMenu = QtGui.QMenu(self)
        
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
        for x in range(0,c):
            self.chat_tabs.widget(x).OnClose(x)
        G['config'].Save();
        self.trayIcon.hide()
        G['QAPP'].quit();
        
    def WordFilterWindow(self): 
        pass
    
    def GET_icons(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtCore.QUrl('http://py-chat.tk/favicon.ico')), 
                       QtGui.QIcon.Normal, 
                       QtGui.QIcon.Off)
        self.icons_conn.append(icon)
        self.setWindowIcon(icon)
        
    def changeStyle(self, styleName):
        G['QAPP'].setStyle(QtGui.QStyleFactory.create(styleName))
        G['config'].settings['view']['style'] = styleName
        QtGui.QApplication.setPalette(self.originalPalette)
    
    def changePalette(self):
        QtGui.QApplication.setPalette(self.originalPalette)
        
                
    def setWindowTitle(self,title):
        QtGui.QMainWindow.setWindowTitle(self,title+' [*]')
        
    def SetUpSignals(self): 
        self.connect(self.Button_NewTab, QtCore.SIGNAL("clicked()"), 
                     lambda: self.CreateTab() )
        self.connect(self.chat_tabs, QtCore.SIGNAL("currentChanged(int)"), self.titleUpdate )
        self.connect(self.chat_tabs, QtCore.SIGNAL("tabCloseRequested(int)"), self.CloseTAB )

    def CloseTAB(self,i):
        self.chat_tabs.widget(i).OnClose(i)
        self.chat_tabs.removeTab(i)
        
    def OpenTAB(self,tabType,argv):
        if tabType == TABT_WEB:
            tab = TAB_web('http://google.ru')
            self.chat_tabs.addTab(tab, 'web')
            tab.init_TWO()
        if tabType == TABT_1984_CHAT:
            self.CreateTab(argv)
            
    def CreateTab(self,connIndex=None,TabName='',conn_par=None,IsAutoConn=False):
        
        print ('#open tab index %s' % (connIndex))
        tab = TAB_Connection()
        self.chat_tabs.addTab(tab, TabName)
        tab.init_TWO(connIndex,conn_par, IsAutoConn)
        return tab
    
    def AddCustomTab(self,tabwidget,name=''):
        self.chat_tabs.addTab(tabwidget, name)
        tabwidget.init_TWO(self)
    

if __name__ == '__main__':
    #os.system('clear')
    #G['script_dir'] = os.path.dirname(__file__) # __file__ не работает в скомпилированном exe
    G['script_dir'] = os.path.abspath(os.path.dirname(sys.argv[0]))
    Debug.info("Change working directory to: "+G['script_dir'])
    os.chdir(G['script_dir'])
    
    G['QAPP'] =  QtGui.QApplication(sys.argv)
    G['config'] = Config()
    G['plugin_o'] = PluginHandler()
    G['chat_win'] = Chat()

    sys.exit(G['QAPP'].exec_())
