# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Jan  7 19:36:12 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(536, 302)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout = QtGui.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName("gridLayout")
		self.splitter = QtGui.QSplitter(self.centralwidget)
		self.splitter.setOrientation(QtCore.Qt.Vertical)
		self.splitter.setObjectName("splitter")
		self.Messages = QtGui.QTextEdit(self.splitter)
		self.Messages.setObjectName("Messages")
		self.Input = QtGui.QTextEdit(self.splitter)
		self.Input.setObjectName("Input")
		self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

