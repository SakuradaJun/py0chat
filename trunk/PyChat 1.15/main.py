#!/usr/bin/python
#-*-coding: utf-8 -*-
'''
Created on 03.01.2011

@author: питон-кун
'''

gloal_windowsTitle = "PyChat 1.15 (dbg)"

import re, os, sys
from class_config_man import *
from class_MainQThread import *
from PyQt4 import QtCore, QtGui #,phonon
import gui
from PostParser import *

def translate(Text_tr):

	eng_key = u"""qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?""" #qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?
	rus_key = u"""йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,""" #йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,
	i = 0
	
	while i < 66:
		current_eng = unicode(eng_key[i]).encode('utf-8')
		current_rus = unicode(rus_key[i]).encode('utf-8')
		Text_tr = Text_tr.replace(current_rus, current_eng)
		i +=1
		
	del eng_key ,rus_key
	return Text_tr
	
class MainChatForm(QtGui.QMainWindow,gui.Ui_MainWindow, gui.Radio):

	NameFagInterator = 0
	show_popup_timeout = 3000
	Input_max = 255
	msg_popup_list = {}
	popUp_count = 1
	Threads_dic = {}
	Threads_exits = []

	TextEdit_css_style = """
	.m_highlight {
		border-left: 2pt solid #FFFFA0;
		-webkit-animation-name: highlight;
		-webkit-animation-duration: 1.2s;
		-webkit-animation-iteration-count: 1;
		-webkit-animation-timing-function: linear;
	}

	body {
	background: url('images/background.png') repeat;
	}

	@-webkit-keyframes highlight 
	{
		0% {
			background-color: #FFFFA0;
		}

		33% {
			background-color: #FFFFA0;
		}	
		100% {
			background-color: white;
		}
	}
	
	.my { 
		color : red; 
	} 
	
	.reply {
		color: #ff6600;
	} 
	
	.msgNum {
		color: #3366ff;
		text-decoration: none;
		font-family: Trebuchet MS,sans; 
	}
	
	.lllla {
	color: red;
	text-decoration: none;
	}
	"""
	
	#S_TEST = "<a href='event:insert,2670133' class='msgNum'>2670133</a> <span class='post_time'>18:12:06</span><br />Тест."
	
	def __init__(self):
		super(MainChatForm, self).__init__()
		self.conf_o = conf_o
		self.show()
		self.setupUi(self)
		self.setUpMainUi()

		if False:
			self.timer = QtCore.QTimer()
			self.timer.start(4000)
			self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.de_op)
		
		# Установка CSS для TextEdit с сообщениями чата
		self.textEdit_Chat.document().setDefaultStyleSheet(self.TextEdit_css_style);
		
		self.LoadConfig()
		#'''<a href="http://2-ch.ru/b/src/1294339093360.jpg" target="_blank">http://2-ch.ru/b/src/1294339093360.jpg</a> [21:42:00] <b>&lt;<a href="event:insert,2673551"><font color="#000000">2673551</font></a></b><b>&gt;</b> Вин на вине вином погоняет.'''
		#self.S_TEST = ParsePost(u'[18:12:06] <b>&lt;<a href="event:insert,2670133"><font color="#000000">2670133</font></a></b><b>&gt;</b> Грустное кино. Так <br />')
		#utf = QtGui.QApplication.translate("MainWindow",self.S_TEST, None, QtGui.QApplication.UnicodeUTF8)
		#self.textEdit_Chat.append(utf)
		#self.textEdit_Chat.append(u'<span class="m_highlight">dsadas</span><img src="images/background.png" height="14"/>')
		#self.textEdit_Chat.toHtml()
		#self.AddText(u'[18:12:06] <b>&lt;<a href="event:insert,2670133"><2670133</span></a></b><b>&gt;</b> Грустное кино.<br />')
		return
		
		# Тест popUP
		if False:
			self.showPopupMessage(msg = u'Нарута', title=None)
			self.showPopupMessage(msg = u'Это', title=None)
			self.showPopupMessage(msg = u'Крута', title=None)
			
			self.showPopupMessage(msg = u'Тимотей', title=None)
			self.showPopupMessage(msg = u'Яой', title=None)
			self.showPopupMessage(msg = u'Коната', title=None)
		
		if conf_o.settings['autoconnect']:
			#self.Thread_Run()
			pass

	def setUpMainUi(self):
		
		self.setWindowTitle(QtGui.QApplication.translate("MainWindow", gloal_windowsTitle, None, QtGui.QApplication.UnicodeUTF8))
		self.icon = QtGui.QIcon()
		self.icon.addPixmap(QtGui.QPixmap('Images/icon_16.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		QtGui.QApplication.setWindowIcon(self.icon)
		self.setWindowIcon(self.icon)
		
		self.textEdit_Chat.setAcceptRichText(True)
		
		'''
		self.fontChat = QtGui.QFont()
		self.fontChat.setFamily("Droid Sans")
		self.fontChat.setPointSize(14)
		self.textEdit_Chat.setFont(self.fontChat)

		self.font_chat_input = QtGui.QFont()
		self.font_chat_input.setFamily("Droid Sans")
		self.font_chat_input.setPointSize(14)#9
		self.TextEdit_Input.setFont(self.font_chat_input)
		
		self.font_for_main_window = QtGui.QFont()
		self.font_for_main_window.setFamily("Droid Sans")
		self.font_for_main_window.setPointSize(9)#9
		self.setFont(self.font_for_main_window)
		'''
		
		#MainWindow.resize(902, 520)
		self.toolButton_Console.hide()
		self.label_captcha.hide()
		self.toolButton.hide() # key
		self.toolButton_2.hide()
		#self.toolButton_Options.hide()
		self.originalPalette = QtGui.QApplication.palette()
		#LinksAccessibleByMouse 
		self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
		
		# Create Tray
		self.createActions()
		self.createTrayIcon()
		self.trayIcon.show()

		# Set SIGNALS
		gui.Radio(self)
		self.connect(self.pushButton_Send, QtCore.SIGNAL("clicked()"), self.Send )
		self.connect(self.TextEdit_Input, QtCore.SIGNAL("editingFinished_Enter()"), self.Send )
		self.connect(self.TextEdit_Input, QtCore.SIGNAL("editingFinished_Enter()"), self.Send )
		
		self.connect(self.textEdit_Chat, QtCore.SIGNAL("paste_link(QString)"), self.LinkPaste)
		self.connect(self.textEdit_Chat, QtCore.SIGNAL("link_Picture(QString)"), self.ViewImage)
		self.connect(self.pushButton_Connect, QtCore.SIGNAL("clicked()"), self.Thread_Run )
		#self.connect(self.toolButton_Console, QtCore.SIGNAL("clicked()"), self.Thread_Diskonnect)
		self.connect(self.toolButton_Options, QtCore.SIGNAL("clicked()"), self.OptionWin)
		#self.connect(self.toolButton_2, QtCore.SIGNAL("clicked()"), self.translate_L)
		#self.TextEdit_Input.hide()
		#self.textEdit_Chat.hide()
		
		#self.dial = gui.dial(self)

	def translate_L(self, isUTF = False):
		msg = unicode(self.TextEdit_Input.toPlainText()).encode('utf-8')
		newText = translate(msg)
		self.TextEdit_Input.setPlainText(QtGui.QApplication.translate("MainWindow", newText, None, QtGui.QApplication.UnicodeUTF8))
		
	def SetSignals(self):
		# Ставим сигналы на все существующие треды
		for obj_i in self.Threads_exits:
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("setDownRange(int)"), self.DownRange)
			#self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("setDownVal(int)"), self.DownSetVal)
			#self.ProgressBar_buffer, 
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("setDownVal(int)"), self.progDownBar, QtCore.SLOT('setValue(int)'))
			
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("ViewCaptcha()"), self.ViewCaptchaData)
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("HideCaptcha(QString)"), self.HideCaptcha)
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("OnlineCounter(QString)"), self.label_Online.setText)
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("output_chat(QString)"), self.AddText)
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("RadioSetText(QString)"), lambda text:self.RadioText(text,'thread'))
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("DisconnectUpdateGUI()"), self.DisconnectUpdateGUI)
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("ClearChat()"), self.ClearChat)
			self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("thread_is_die()"), self.Disconnected_)
			
			
	# Выполняется при закрытии главного окна
	def closeEvent(self, event): self.SaveConfig(); app.quit();
		
	def Disconnected_(self,*arg): self.pushButton_Connect.setText('Connect')
		
	def Thread_Run(self):
		obj_i = 1
		print "Сейчас Всего %s тредов" % (len(self.Threads_exits))
		#for obj_i in self.Threads_exits:
		#hasattr(self.Threads_dic, )
		if obj_i in self.Threads_dic:
			print "Есть обьект %s , Удаляем" % (obj_i)
			if self.Threads_dic[obj_i].isRunning():
				print "Поток запущен"
				if self.Threads_dic[obj_i].StopMainWhile == True:
					#self.Threads_dic[obj_i].deleteLater()
					del self.Threads_dic[obj_i]
				else:
					self.Threads_dic[obj_i].stop()
				return
		else:
			print "Нету! Создаем обьект"
			Create_current_at = 1#len(self.Threads_dic)+1
			
			self.Threads_dic[Create_current_at] = MainQThread(conf_o = conf_o,mainWin_obj=self)
			self.Threads_dic[Create_current_at].self_id_in_dic = Create_current_at
			
			self.Threads_exits.append(Create_current_at)
			self.SetSignals()
			self.pushButton_Connect.setText('Disconnect')
			self.Threads_dic[Create_current_at].start()
		
	def Thread_Diskonnect(self):
		# Q_thread_1.exit()
		# Q_thread_1.quit()
		#Q_thread_1.Disconnect(True)
		if self.Q_thread_1.isRunning():
				self.Q_thread_1.stop()

	def DisconnectUpdateGUI(self):
		self.pushButton_Connect.setText('Connect')
		self.label_Online.setText ("<b>Online:&nbsp;</b>0")
		#print "Сейчас ссылок %s на этот обьект" % (sys.getrefcount(self.Q_thread_1))
		for ins in self.Threads_dic:
			print "%s -> %s" % (ins,self.Threads_dic[ins])
		#if 1 in self.Threads_dic: del self.Threads_dic[1]
		#print "Сейчас ссылок %s на этот обьект" % (sys.getrefcount(self.Q_thread_1))

	def Send(self):
		thread_obj = self.Threads_dic[len(self.Threads_dic)] # Тут будет обьект треда с которым будем работать
		#Input_text = self.TextEdit_Input.toPlainText()
		#if Input_text
		# Если текст есть, если сокет активин и он сам есть то отпровляем
		if self.TextEdit_Input.toPlainText() and thread_obj.SocketActive and hasattr(thread_obj, 'socket_o'):
			msg = unicode(self.TextEdit_Input.toPlainText()).encode('utf-8')
			name = unicode(self.lineEdit_Name.text()).encode('utf-8')
			
			if thread_obj.cpatcha_enter == False:
				newText = translate(msg)
				#self.TextEdit_Input.setPlainText(newText)
				msg = unicode(self.TextEdit_Input.toPlainText()).encode('utf-8')
				thread_obj.writeSocket(str(newText))
				self.TextEdit_Input.clear()
				
			
			if thread_obj.cpatcha_enter == True:   
				if self.checkBox_NameFag.isChecked() and self.lineEdit_Name.text() != '':
					name = name.replace('${iterator}', str(self.NameFagInterator))
					thread_obj.writeSocket(str(name+msg))
					self.NameFagInterator = self.NameFagInterator+1
				else:
					thread_obj.writeSocket(str(msg))
				self.TextEdit_Input.clear()

	def LinkPaste(self, text): self.TextEdit_Input.insertPlainText(text)
	
	def ViewCaptchaData(self,img_data = None):

		self.image = QtGui.QPixmap()
		self.image.loadFromData(conf_o.DATA_CAPTCHA)
		#width = self.image.width(); height = self.image.height()
		self.label_captcha.setPixmap(self.image)
		self.label_captcha.setEnabled(True)
		self.label_captcha.show()
		conf_o.DATA_CAPTCHA = None
		
	def HideCaptcha(self, *a): self.label_captcha.hide()
		
	# Добавление сообщения в чат
	def AddText(self,text):
		#text = QtCore.QString(text).fromUtf8(str, size=_1)
		#text = ParsePost( str(text) ) #.decode('utf-8')
		utf = QtGui.QApplication.translate("MainWindow", text, None, QtGui.QApplication.UnicodeUTF8)
		self.textEdit_Chat.append(utf)
		self.textEdit_Chat.toHtml()
		#self.showPopupMessage(utf)
		
	def ClearChat(self): self.textEdit_Chat.clear()

	def ViewImage(self, text): pass

	## STYLE
	def changeStyle(self, styleName, Load = False):
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(styleName))
		if Load != True:
			self.changePalette()  
	
	def changePalette(self):
		if (conf_o.settings['style_color']['originalPalette']):
			QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
		else:
			QtGui.QApplication.setPalette(self.originalPalette)

	# Load\Save CFG	
	def SaveConfig(self):
		conf_o.settings['view']['MainWindow_W'] = self.width()
		conf_o.settings['view']['MainWindow_H'] = self.height()
		conf_o.settings['style_color']['style'] = conf_o.settings['style_color']['style']
		conf_o.settings['user_nick'] = unicode(self.lineEdit_Name.text()).encode('utf-8')
		conf_o.settings['NamefagMode'] = self.checkBox_NameFag.isChecked()
		if self.RadioUrlActive: conf_o.settings['radio_current'] = self.RadioUrlActive;
		if self.RadioUrl: conf_o.settings['radio'] = {'UrlList':self.RadioUrl}
		conf_o.Save()
		
	def LoadConfig(self):
		conf_o.Load()
		
		self.fontChat = QtGui.QFont()
		self.fontChat.setFamily(conf_o.settings['style_color']['font_chat_message'][0])
		self.fontChat.setPointSize(conf_o.settings['style_color']['font_chat_message'][1])
		self.textEdit_Chat.setFont(self.fontChat)
		
		self.font_chat_input = QtGui.QFont()
		self.font_chat_input.setFamily(conf_o.settings['style_color']['font_text_input'][0])
		self.font_chat_input.setPointSize(conf_o.settings['style_color']['font_text_input'][1])
		self.TextEdit_Input.setFont(self.font_chat_input)
		
		self.font_for_main_window = QtGui.QFont()
		self.font_for_main_window.setFamily(conf_o.settings['style_color']['font_main_wondow'][0])
		self.font_for_main_window.setPointSize(conf_o.settings['style_color']['font_main_wondow'][1])#9
		self.setFont(self.font_for_main_window)
		
		self.lineEdit_Name.setText(QtGui.QApplication.translate("MainWindow", conf_o.settings['user_nick'], None, QtGui.QApplication.UnicodeUTF8))
		self.checkBox_NameFag.setChecked(conf_o.settings['NamefagMode'])
		self.resize(conf_o.settings['view']['MainWindow_W'], conf_o.settings['view'][ 'MainWindow_H']) 
		self.changeStyle(conf_o.settings['style_color']['style'], conf_o.settings['style_color']['originalPalette'])
		self.setWindowTitle(QtGui.QApplication.translate("MainWindow", gloal_windowsTitle+" - "+conf_o.settings['servers'][conf_o.settings['current_server']]['host']+":"+str(conf_o.settings['servers'][conf_o.settings['current_server']]['port']), None, QtGui.QApplication.UnicodeUTF8))
		QtGui.QApplication.setApplicationName(gloal_windowsTitle)
		
		if 'radio' in conf_o.settings: 
			if 'radio_current' in conf_o.settings: self.RadioUrlActive = conf_o.settings['radio_current']; print 'Загруженна текущая'
			if 'UrlList' in conf_o.settings['radio']: self.RadioUrl = conf_o.settings['radio']['UrlList']
		#msgBox.exec();
	## Tray
	def createActions(self):
		self.minimizeAction = QtGui.QAction("Mi&nimize", self, triggered=self.hide)
		self.maximizeAction = QtGui.QAction("Ma&ximize", self, triggered=self.showMaximized)
		self.restoreAction = QtGui.QAction("&Restore", self, triggered=self.showNormal)
		self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)  
		self.action_about = QtGui.QAction("&About Qt", self, triggered=QtGui.qApp.aboutQt)
		self.action_about = QtGui.QAction("&Show settings arr", self, triggered=self.PrintConfigArray)

	def createTrayIcon(self):
		self.trayIconMenu = QtGui.QMenu(self)
		self.trayIconMenu.addAction(self.minimizeAction)
		self.trayIconMenu.addAction(self.maximizeAction)
		self.trayIconMenu.addAction(self.restoreAction)
		self.trayIconMenu.addAction(self.action_about)
		self.trayIconMenu.addSeparator()
		self.trayIconMenu.addAction(self.quitAction)
		
		self.trayIcon = QtGui.QSystemTrayIcon(self.icon)
		self.trayIcon.setContextMenu(self.trayIconMenu)
	
	def showPopupMessage(self, msg , title = 'Message:'):
		'''
		if hasattr(self, 'msg_popup'):
			self.msg_popup.close()
			#del self.msg_popup
			#self.msg_popup.deleteLater()
		'''
		#self.connect(obj, QtCore.SIGNAL('closed()'), obj, QtCore.SLOT('deleteLater()'));
		
		#t = time.time()
		obj = gui.Popup(msg,parent=self)
		obj.my_id = self.popUp_count
		self.msg_popup_list[int(self.popUp_count)] = obj
		obj.self_num = len(self.msg_popup_list)
		
		# = len(self.msg_popup_list)
		obj._show()
		self.popUp_count =  self.popUp_count+1
		#len_o = len(self.msg_popup_list)
		#self.msg_popup_list[-1].self_num = len_o
		#self.msg_popup_list[-1].self_num = len(self.msg_popup_list)
		
	## ENd tray!
	
	def OptionWin(self):
		self.win_conf = gui.Configuration_win(win,conf_o)
		self.win_conf.show()

if __name__ == '__main__':
	os.system('clear')
	if len(sys.argv) > 1:
		if sys.argv[1] in ('help','-help'):
			print "Usage:",sys.argv[0], "-s server_name_in_settings.yaml"
			sys.exit(1)
		if len(sys.argv) < 3: 
			print "Usage:",sys.argv[0], "-s server_name_in_settings.yaml"
			sys.exit(1)
	
	#conf_o.set_def_settings() ;conf_o.Save() ;exit(1)
	import gc
	gc.enable()
	conf_o = Config()
	app = gui.app
	#TestWin_o = gui.TestWin()
	#win_i = gui.ImageWindow_d(u'http://img.0chan.ru/wp/src/12942426116674.jpg')
	#win_i.app = app
	win =  MainChatForm()
	#!win_conf = gui.Configuration_win(win)
	#!win_conf.show()
	#gui.Window_From_UI.show()
	
	app.exec_()
