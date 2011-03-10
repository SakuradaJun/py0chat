#-*-coding: utf-8 -*-
'''
Created on 09.03.2011

@author: anon
'''
from lib.utilits import *
from lib.utilits_parser import *
from PyQt4 import QtCore, QtGui, uic

class WordFilter_Widget(QtGui.QDialog):

    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self)
        uic.loadUi('res/word_filter_add.ui',self)
        self.show()
        