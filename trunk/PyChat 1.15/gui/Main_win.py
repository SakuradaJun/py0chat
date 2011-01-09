# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\wipe\0chat\Form_UI\For_Relese_02\chat_from_2.ui'
#
# Created: Wed May 05 11:45:43 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import re

class ChatTextEdit(QtGui.QTextEdit):
    
    #re_serach_event = re.compile('event[:]insert[\,]([0-9]{1,10})')
    re_serach_event = re.compile('event\:(.*)')
    re_serach_insert_event = re.compile('insert\,(\d+)')
    
    def __init__(self,parent = None):
        super(ChatTextEdit, self).__init__(parent)
        if False:
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.connect(self,QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), lambda x: self.show_Menu(x))
        
    def show_Menu(self,point):
        self.menu = self.createStandardContextMenu(self.mapToGlobal(point))
        
        #QtCore.Qt.DefaultContextMenu
        #self.menu.addAction( QtGui.QAction("Copy:", self) )
        self.menu.exec_(self.mapToGlobal(point) ) 
        
    def mousePressEvent(self, event):
    
        if self.anchorAt(event.pos()) and event.button() == QtCore.Qt.LeftButton:
            Link_href = self.anchorAt(event.pos())
            get_link = self.re_serach_event.search(Link_href)
            # Если это event
            if get_link: 
                #Если insert,131231
                insert = self.re_serach_insert_event.search(get_link.group(1))
                if insert: 
                    self.emit(QtCore.SIGNAL("paste_link(QString)"), ">>%s " % (insert.group(1)))
            else:
                try:
                    get_link_url_img = re.compile('(http:\/\/[\S_ ]+\.(png|jpg|gif))').search(Link_href).group(1)
                except:
                    pass
                if get_link_url_img:
                    self.emit(QtCore.SIGNAL("link_Picture(QString)"), get_link_url_img)
                    get_link_url_img = False
        super(ChatTextEdit, self).mousePressEvent(event)

class ChatPlainTextEdit(QtGui.QPlainTextEdit):
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return: # or QtCore.Qt.Key_Enter
            self.emit(QtCore.SIGNAL("editingFinished_Enter()"))
        else:
            QtGui.QPlainTextEdit.keyPressEvent(self, event)

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(902, 520)
        '''
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/Icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        '''
 
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.pushButton_Connect = QtGui.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/wink.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Connect.setIcon(icon1)
        self.pushButton_Connect.setObjectName("pushButton_Connect")
        self.horizontalLayout.addWidget(self.pushButton_Connect)
        self.AddRadio(MainWindow)
        spacerItem = QtGui.QSpacerItem(4, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMouseTracking(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(49, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_captcha = QtGui.QLabel(self.centralwidget)
        self.label_captcha.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_captcha.sizePolicy().hasHeightForWidth())
        self.label_captcha.setSizePolicy(sizePolicy)
        self.label_captcha.setMinimumSize(QtCore.QSize(120, 40))
        self.label_captcha.setAlignment(QtCore.Qt.AlignCenter)
        self.label_captcha.setObjectName("label_captcha")
        self.horizontalLayout.addWidget(self.label_captcha)
        self.lineEdit_Name = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_Name.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Name.sizePolicy().hasHeightForWidth())
        self.lineEdit_Name.setSizePolicy(sizePolicy)
        self.lineEdit_Name.setObjectName("lineEdit_Name")
        self.horizontalLayout.addWidget(self.lineEdit_Name)
        self.checkBox_NameFag = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_NameFag.setObjectName("checkBox_NameFag")
        self.horizontalLayout.addWidget(self.checkBox_NameFag)
        self.label_Online = QtGui.QLabel(self.centralwidget)
        self.label_Online.setObjectName("label_Online")
        self.horizontalLayout.addWidget(self.label_Online)
        spacerItem2 = QtGui.QSpacerItem(12, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(5)
        self.splitter.setObjectName("splitter")
        self.textEdit_Chat = ChatTextEdit(self.splitter)#QtGui.QTextEdit ChatTextEdit
        
        #font = QtGui.QFont() #font.setFamily("Droid Sans")font.setFamily("Verdana") font.setPointSize(12) self.textEdit_Chat.setFont(font)
        #! self.textEdit_Chat.setMouseTracking(False)
        #! self.textEdit_Chat.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.textEdit_Chat.setAcceptDrops(True) # False
        #! self.textEdit_Chat.setAutoFillBackground(True)
        self.textEdit_Chat.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_Chat.setReadOnly(True)
        self.textEdit_Chat.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.textEdit_Chat.setObjectName("textEdit_Chat")
        self.TextEdit_Input = ChatPlainTextEdit(self.splitter) #QtGui.QPlainTextEdit
        self.TextEdit_Input.setMinimumSize(QtCore.QSize(0, 25))
        self.TextEdit_Input.setBaseSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        self.TextEdit_Input.setFont(font)
        self.TextEdit_Input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.TextEdit_Input.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.TextEdit_Input.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.TextEdit_Input.setMaximumBlockCount(255)
        self.TextEdit_Input.setObjectName("TextEdit_Input")
        self.gridLayout.addWidget(self.splitter, 2, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.toolButton_Clear = QtGui.QToolButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Images/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_Clear.setIcon(icon2)
        self.toolButton_Clear.setAutoRaise(True)
        self.toolButton_Clear.setObjectName("toolButton_Clear")
        self.horizontalLayout_3.addWidget(self.toolButton_Clear)
        spacerItem3 = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.toolButton_2 = QtGui.QToolButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Images/translate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_2.setIcon(icon3)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_3.addWidget(self.toolButton_2)
        self.toolButton = QtGui.QToolButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Images/key_enter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon4)
        self.toolButton.setCheckable(True)
        self.toolButton.setChecked(True)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_3.addWidget(self.toolButton)
        self.toolButton_Console = QtGui.QToolButton(self.centralwidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Images/command.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_Console.setIcon(icon5)
        self.toolButton_Console.setAutoRaise(True)
        self.toolButton_Console.setObjectName("toolButton_Console")
        self.horizontalLayout_3.addWidget(self.toolButton_Console)
        self.toolButton_Options = QtGui.QToolButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Images/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_Options.setIcon(icon6)
        self.toolButton_Options.setAutoRaise(True)
        self.toolButton_Options.setObjectName("toolButton_Options")
        self.horizontalLayout_3.addWidget(self.toolButton_Options)
        
        self.CreateProgressDownBar()
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.pushButton_Send = QtGui.QPushButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("Images/message.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Send.setIcon(icon7)
        self.pushButton_Send.setObjectName("pushButton_Send")
        self.horizontalLayout_3.addWidget(self.pushButton_Send)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.toolButton_Clear, QtCore.SIGNAL("clicked(bool)"), self.textEdit_Chat.clear)
        QtCore.QObject.connect(self.checkBox_NameFag, QtCore.SIGNAL("toggled(bool)"), self.lineEdit_Name.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def AddRadio(self, MainWindow):
        self.PushButton_Play = QtGui.QPushButton(self.centralwidget)
        self.PushButton_Play.setText('Play')
        self.PushButton_Play.setCheckable(True)
        
        #self.PushButton_Play.setMinimumSize(QtCore.QSize(51, 27))
        self.PushButton_Play.setMaximumSize(52, 27)
        #self.PushButton_Play.setBaseSize(QtCore.QSize(51, 27))
        
        #self.PushButton_Play.setGeometry(10, 10,75,23)
        self.horizontalLayout.addWidget(self.PushButton_Play)
        self.connect(self.PushButton_Play, QtCore.SIGNAL("clicked(bool)"), MainWindow.RadionPlay)
        
        self.ProgressBar_buffer = QtGui.QProgressBar(self.centralwidget)
        self.ProgressBar_buffer.setRange(0, 100)
        self.ProgressBar_buffer.hide()
        self.horizontalLayout.addWidget(self.ProgressBar_buffer)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "PyChat", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Connect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        
        self.label_captcha.setText(QtGui.QApplication.translate("MainWindow", "captcha", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_NameFag.setText(QtGui.QApplication.translate("MainWindow", "Namefag", None, QtGui.QApplication.UnicodeUTF8))
        #self.label_Online.setText(QtGui.QApplication.translate("MainWindow", "Online:</span>", None, QtGui.QApplication.UnicodeUTF8))

        self.toolButton_Clear.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("MainWindow", "Translete", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("MainWindow", "Send_toEnter", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_Console.setText(QtGui.QApplication.translate("MainWindow", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_Options.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Send.setText(QtGui.QApplication.translate("MainWindow", "Send", None, QtGui.QApplication.UnicodeUTF8))
    
    def CreateMainMenu(self):
        pass

    def CreateProgressDownBar(self):
        self.progDownBar = QtGui.QProgressBar(self.centralwidget)
        self.horizontalLayout_3.addWidget(self.progDownBar)

    def DownRange(self,d):
        self.progDownBar.setRange(0, d)
        
    def DownSetVal(self,value):
        #print value
        self.progDownBar.setValue(value)
