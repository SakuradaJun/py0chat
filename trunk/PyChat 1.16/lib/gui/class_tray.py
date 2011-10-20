'''
Created on 06.09.2011

@author: anon
'''
from PyQt4 import QtCore
from PyQt4 import QtGui

class Tray:

    def __init__(self,params):
        self.trayIcon = QtGui.QSystemTrayIcon(self.icon_main)
        self.trayIcon.showMessage("sdf","df")
        self.trayIcon.setToolTip("sdf")
        self.trayIconMenu = QtGui.QMenu(self)
        
        #self.trayIconMenu.addAction(self.action_test)
        #self.trayIconMenu.addAction(self.action_SwitchMiniStyle)
        
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()
        