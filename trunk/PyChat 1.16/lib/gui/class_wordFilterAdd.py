#-*-coding: utf-8 -*-
'''
Created on 09.03.2011
@author: anon

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
from lib.utilits import *
from lib.utilits_parser import *
from PyQt4 import QtCore, QtGui, uic

class WordFilterAdd_Widget(QtGui.QDialog):

    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self)
        uic.loadUi('res/word_filter_add.ui',self)
        self.show()
        