#-*-coding: utf-8 -*-
'''
Created on 04.03.2011

@author: anon
'''
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from lib.class_plugin_core import Plugin

class KernelPlugin(Plugin): # производим наш плагин от родительского класса
    Name = 'KernelPlugin'
 
    # замещаем нужные методы
    def OnLoad(self,parent,P):
        pass
        
    def OnCommand(self, cmd_args):
        print cmd_args
        return