#!/usr/bin/python
#-*-coding: utf-8 -*-

from PyQt4 import QtCore
from urllib2 import urlopen
import socket, re #, os, sys
import time
from struct import unpack
import  yaml
from PostParser import *
#import captcha_breaker

'''
	HEADER = '\033[95m' 
	OKBLUE = '\033[94m' 
	OKGREEN = '\033[92m' 
	WARNING = '\033[93m' 
	FAIL = '\033[91m' 
	ENDC = '\033[0m' 
'''
cmd_description = {
	'\x01':'Сообщение',
	'\x02':'Онлайн',
	'\x03':'Ошибка',
	'\x04':'Радио',
	'\x05':'Капча',
	'\x07':'Успешная авторизация'
}
AOUTOR_ERROR = 7

class CacheToken:
	'''
	Смотреть текущий ИП
	Смотреть Базу Данных На предмет нахождение в ней текущего ИП
	Если ИП найдет то возвращать токен по ключу, если нет то False
	'''
	bd = {None:None}
	bd_file_name = 'cache_of_token.yaml'
	
	def __init__(self):
		self.Load()
		
	def get(self):
		if self.bd == None:
			return False
		if self.SetIP() == False: return False
		self.Load()
		for ip in self.bd:
			if ip == self.ip_current:
				return self.bd[ip]
		return False
	
	def Save(self):
		file_h = file(self.bd_file_name,'w+')
		yaml.dump(self.bd, file_h, 
				default_flow_style=None,
				encoding='utf-8',
				allow_unicode=True)
		file_h.close()
		
	def Load(self):
		try:
			file_h = file(self.bd_file_name,'r+')
			self.bd = yaml.load(file_h)
		except Exception,err:
			print '# %s' % (str(err))
			self.bd = {None:None}
			self.Save()
			return True
		if self.bd is None:
			self.bd = {'def':'None'}
		file_h.close()
		
	def SetIP(self):
		try:
			s_o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s_o.connect(('8.8.8.8',53))
			self.ip_current = s_o.getsockname()[0]
			s_o.close()
		except Exception,err:
			print str(err)
			return False
		
	def AddToken(self,Token):
		if Token == None:
			return False
		if self.SetIP() == False: return False
		self.Load()
		if self.bd:
			for ip in self.bd:
				if ip == self.ip_current:
					if self.bd[self.ip_current] == Token:
						self.bd['IP %s Имеет два токена ID:%s' % (self.ip_current,time.time())] = Token
						self.Save()
						return False
		#print "%s %s" % (self.ip_current,Token)
		self.bd[str(self.ip_current)] = str(Token)
		self.Save()
		return True

class MainQThread(QtCore.QThread):

	printConsoleLog = True
	UseCacheToken = True
	UseCaptchaBreaker = False
	NameFagInterator = 0
	
	def __init__(self, mainWin_obj, parent = None, conf_o = None):
		QtCore.QThread.__init__(self, parent)
		self.mainWin_obj = mainWin_obj
		self.conf_o = conf_o
		global cmd_description
		self.cmd_description = cmd_description

	# Установка настроек
	def Set_Vars(self):
		self.admin_key = self.conf_o.settings['admin_pass']
		self.chat_port = self.conf_o.settings['servers'][self.conf_o.settings['current_server']]['port']
		self.chat_host = self.conf_o.settings['servers'][self.conf_o.settings['current_server']]['host']
		self.chat_token_page = self.conf_o.settings['servers'][self.conf_o.settings['current_server']]['token_page']

		# Thread settings
		self.cpatcha_enter = False
		self.my_message_list = ['']
		self.last_masg = ''
		self.CurentToken = None
		self.SocketActive = False
		self.StopMainWhile = None
		self.PacketCounterMSG = 0
		
	

	def __del__(self):
		print "\033[91mMainQThread __DEL__\033[0m"
		#self.CurentToken = False
		#if hasattr(self, 'socket_o'): self.socket_o.close()
		#self.wait()
		#if hasattr(self, 'socket_o'): 
		#	self.socket_o.close()
		#	del self.socket_o
		#self.terminate()
		
		#self.emit(QtCore.SIGNAL("thread_is_die()"))
	
	def run(self):

		while self.start_conn(): pass
		self.printLog("STOP THREAD, quit main while. %s" % (self.self_id_in_dic))
		self.offSocket()
		self.sendDisconnectSignal()
		self.terminate()
		#del self.mainWin_obj.Threads_dic[self.self_id_in_dic]
		
		#self.wait()

		#self.stop()
	
	def start_conn(self):
		try:
			self.printLog('')
			self.printLog("\033[94m# Run Thread %s\033[0m" % (self.self_id_in_dic))
			self.Set_Vars()
			if self.GetToken() == False: self.stop() ;return False
			if self.SetUpSocket() == False: self.stop() ;return False
			if self.Handshaked() == False: self.stop() ;return False
			#self.SetUpSocket(),self.Handshaked()):
				
			while not self.StopMainWhile:
					# Если возврощает True значит все Ок и продолжаем иначе если False то произошла ошибка
					result = self.MainWhile()
					if result:
						if result == AOUTOR_ERROR: return True
						continue
					else:
						break
			#self.quit()
		except KeyboardInterrupt:
			print "Exit by Keyboard Interrupt"
			exit()
		return False
	
	def stop(self):
		print "Stop в %s" % (self.self_id_in_dic)
		
		self.StopMainWhile = True
		#self.wait()
		return
		#self.terminate()
		#del self.mainWin_obj.Threads_dic[self.self_id_in_dic]
		
	def sendDisconnectSignal(self):
		self.emit(QtCore.SIGNAL("DisconnectUpdateGUI()"))
		self.emit(QtCore.SIGNAL("HideCaptcha(QString)"), '')
		self.emit(QtCore.SIGNAL("output_chat(QString)"), '<font color="#800000">Disconnected</font>')
		
	def offSocket(self):
		if hasattr(self, 'socket_o'): 
			try:
				self.socket_o.shutdown(0)
				self.socket_o.shutdown(1)
				self.socket_o.shutdown(2)
				self.socket_o.close()
				del self.socket_o
			except:
				pass
			
	def GetToken(self):
		if self.UseCacheToken:
			tok_c = CacheToken().get()
			if tok_c:
				self.PrintGui('<font color="#0000ff">Токен найден в кеше.</font>')
				self.CurentToken = tok_c
				return True
			else:
				del tok_c
		
		self.printLog('# Get token from: %s' % (self.chat_token_page))
		self.PrintGui('<font color="#0000ff">Get token...</font>')
		try:
			self.CurentToken = re.compile('token=([a-zA-Z0-9]{32})').search(urlopen(self.chat_token_page).read()).group(1)
		except Exception, err:
			#self.PrintGui('<font color="#800000">Get token error (Возможно сервер выпилен в данный момент или у вас отсутствует подключение к интернетам.)</font>')
			self.PrintGui('<font color="#800000">Get token error.</font>')
			#print dir(err) #@UndefinedVariable
			#print str(err.message)
			self.stop()
			return False
		if self.UseCacheToken: CacheToken().AddToken(self.CurentToken)
	
	# Handshaked
	def Handshaked(self):
		# Connecting
		self.PrintGui('<font color="#0000ff">Connecting...</font>')
		self.printLog('# Connecting... ')
		try:
			self.socket_o.connect( (self.chat_host, self.chat_port) )
			self.SocketActive = True
		except Exception, err_msg:
			#self.printLog("Error: Can\'t connect to server.")
			self.printLog("Error: %s" % (str(err_msg)))
			self.PrintGui('<font color="#800000">Error: %s</font>' % (str(err_msg)))
			self.stop()
			
		# Handshaked
		self.printLog("# Handshaked... ")
		try:
			self.writeSocket('<handshake version=4 token=%s/>' % (self.CurentToken))
		except:
			self.printLog("Socket error send")
			self.PrintGui('<font color="#800000">Socket error send</font>')
			self.stop()
			
	# Create socket 
	def SetUpSocket(self):
		
		try:
			self.socket_o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, err_msg:
			self.printLog("Create socket error.")
			self.PrintGui('<font color="#800000">Create socket error: %s</font>' % (err_msg))
			self.stop()
		
	def MainWhile(self):
		# Комманды: 1 - сообщение чата, 2 - число онлайн, 3 - ошибка, 4 - заголовок с радио, 5 - верификация 
		# Первыеее 2 байта это размер, а последующий 1 байт тип комманды
		cmd = ''
		data_size = 0
		data = ''
		
		try:
			recv_tmp =  self.socket_o.recv(3)
			if recv_tmp is None:
				self.PrintGui('<font color="#800000">Ошибка: переменная recv_tmp равна none type.</font>')
				return False
			
			if len(recv_tmp) == 3:
				data_size = unpack(">H", recv_tmp[:2])[0] # Это почему то список
				cmd = recv_tmp[2:3] # Тут будет тип сообщения (тип комманды)
			else:
				self.PrintGui('<font color="#800000">Ошибка: при приеме данных. Неверная капча?</font>')
				return AOUTOR_ERROR
				#print "recv_tmp: %s" % (recv_tmp.encode("hex"))
				self.PrintGui('<font color="#800000">Ошибка: recv_tmp содержит мение 3 байт!</font>')
				#self.printLog("# Ошибка: Произошла ошибка при приеме данных.")
				#self.PrintGui('<font color="#800000">Ошибка: Произошла ошибка при приеме данных.</font>')
				return False

			if data_size:
				self.emit(QtCore.SIGNAL("setDownRange(int)"), int(data_size))
			while len(data) < data_size:
					#data = self.socket_o.recv(data_size)
					add_size = data_size-len(data)
					data += self.socket_o.recv(1)
					#data += self.socket_o.recv(add_size)
					self.emit(QtCore.SIGNAL("setDownVal(int)"), len(data))
			self.emit(QtCore.SIGNAL("setDownVal(int)"), len(data))
				
		except Exception, err:
			'''
			if err.errno == 11:
				return True
			else:
				return False
			'''
			str_error = str(err)
			print "# Error: %s" % (str_error)
			self.PrintGui('<font color="#800000">Error: %s</font>' % (str_error) )
			self.SocketActive = False
			return False
		
		if cmd:
			#! self.printLog("# Recv cmd: %s (Тип: %s): Size: %s" % (cmd.encode("hex"), self.cmd_description[cmd], data_size) )
			
			# 1 - сообщение чата
			if cmd == "\x01":
				self.PacketCounterMSG +=1
				#f = open('msg_dumb.dat','ab+');f.write(data);f.close()
				#print "\033[95m%s\033[0m" % (data)
				#data = ParsePost(data)
				data = self.StringParser(data)
				self.PrintGui(data)
				return True
			
			# 2 - число онлайн
			if cmd == "\x02":
				self.emit(QtCore.SIGNAL("OnlineCounter(QString)"), "<b>Online:&nbsp;</b> %s" % (data))
				return True
			
			# 3 Ошибка
			if cmd == "\x03":
				self.printLog("# Server err msg: %s" % (data))
				self.PrintGui(data)
				return False
				
			
			# 4 - Радио
			if cmd == "\x04":
				self.emit(QtCore.SIGNAL("RadioSetText(QString)"), data)
				return True
				
			# 5 - верификация (КАПЧА)  
			if cmd == "\x05":
				try:
					self.conf_o.DATA_CAPTCHA = urlopen(data).read()
				except:
					print "Error load captcha from %s" % (data)
					self.PrintGui("Error loading captcha from: %s" % (data))
				self.emit(QtCore.SIGNAL("ViewCaptcha()"))
				if self.UseCaptchaBreaker:
					break_o = captcha_breaker.Capthca_crack(None,im=self.conf_o.DATA_CAPTCHA)
					break_o.run()
					print "Капча: "+str(break_o.strout)
					time.sleep(10)
					self.writeSocket(break_o.strout)
				return True
			
			# 7 - Успешный ввод капчи	
			if cmd == "\x07":
				self.cpatcha_enter = True
				self.printLog("\033[92m# Успешно авторизован.\033[0m")
				self.emit(QtCore.SIGNAL("HideCaptcha(QString)"), data)
				self.emit(QtCore.SIGNAL("ClearChat()"))  
				return True
			return True
		
	def writeSocket(self,data):
		#!print '# Отправка: %s' % (data)
		try:
			self.socket_o.send(data)
		except socket.error, err:
			print str(err)
			
	def StringParser(self,Text):
		#[18:12:06] <b>&lt;<a href="event:insert,2670133"><font color="#000000">2670133</font></a></b><b>&gt;</b> Грустное кино.<br />
		#Text = Text.replace('<font color="red">', '<font color="#ff0000">')
		#Text = Text.replace('то что ищем', 'то на что заменяем')
		Text = re.sub("<font color=\"#000000\">(\d{1,})</font>", "<span class=\"msgNum\">\\1</span>", Text)
		#Text = Text.replace('<font color="#000000">', '<font color="'+self.conf_o.settings['style_color']['MsgNumColor']+'">')
		#Text = Text.replace('<span class="reply">', '<span style="color:#ff6600;">')
		Text = Text.replace('<span class="reply_for_me">', '<span class="reply_for_me" style="color:#FF3333;">')
		return Text
		
	def PrintGui(self,text):
		self.emit(QtCore.SIGNAL("output_chat(QString)"), text)
		
	def printLog(self,str,print_n = False):
		if self.conf_o.settings['debug']['print_log_in_console']:
			if print_n == False:
				print str
			else:
				print str,
