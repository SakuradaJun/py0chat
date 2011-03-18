#-*-coding: utf-8 -*-
'''
Created on 05.03.2011
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

from PyQt4 import QtCore
from PyQt4.QtCore import QString

from urllib2 import urlopen
import socket, re, yaml, os, time
from struct import unpack
from lib.utilits import *
from lib.class_CacheToken import CacheToken

#from tabnanny import Debug.errrint
#from PostParser import *
#import captcha_breaker
AOUTOR_ERROR = 7
cmd_description = {
    '\x01':'Сообщение',
    '\x02':'Онлайн',
    '\x03':'Ошибка',
    '\x04':'Радио',
    '\x05':'Капча',
    '\x07':'Успешная авторизация'
}
RE_SEARCH_POST_NUM = re.compile('<a href=\"event\:insert\,(\d+)\">')

class ChatConnection(QtCore.QThread):
    obj_mainwin = None
    obj_tab = None
    conf_o = None
    printConsoleLog = True
    UseCacheToken = True
    UseCaptchaBreaker = False
    NameFagInterator = 0
    
    cpatcha_enter = False
    my_message_list = ['']
    last_masg = ''
    CurentToken = None
    SocketActive = False
    StopMainWhile = False
    PacketCounterMSG = 0
    GET_GETTER = [12345,'**【питон-кун】　{get_post_id} Гет! ._.**']
    
    def __init__(self,obj_mainwin,obj_tab):
        print 'Create object ChatConnection %s' % (self)
        QtCore.QThread.__init__(self, obj_tab)
        if False: self.socket_o = socket.socket()
        self.obj_mainwin = obj_mainwin
        self.conf_o = self.obj_mainwin.CONF_O
        self.obj_tab = obj_tab
        self.cmd_description = cmd_description

    # Установка настроек
    def Set_Vars(self):
        self.admin_key = self.conf_o.settings['admin_pass']
        #self.chat_port = self.conf_o.settings['servers'][self.conf_o.settings['current_server']]['port']
        #self.chat_host = self.conf_o.settings['servers'][self.conf_o.settings['current_server']]['host']
        #self.chat_token_page = self.conf_o.settings['servers'][self.conf_o.settings['current_server']]['token_page']

        # Thread settings
        self.cpatcha_enter = False
        self.my_message_list = ['']
        self.last_masg = ''
        self.CurentToken = None
        self.SocketActive = False
        self.StopMainWhile = False
        self.PacketCounterMSG = 0
        
    

    def __del__(self):
        Debug.info('\033[91mMainQThread __DEL__\033[0m')
        #self.emit(QtCore.SIGNAL("thread_is_die()"))
    
    def run(self):

        while self.StopMainWhile == False and self.start_conn() : pass
        Debug.info("STOP THREAD, quit main while.")
        self.emit(QtCore.SIGNAL('conn_del()'))
        self.deleteLater()
        del self.obj_tab.obj_conn
    
    def start_conn(self):
        try:
            Debug.debug(Debug.OKBLUE+"Run Thread"+Debug.END)
            self.Set_Vars()
            if self.GetToken() == False: return False
            #self.stop()
            if self.SetUpSocket() == False: return False
            if self.Handshaked() == False: return False
            
            while self.StopMainWhile == False:
                    # Если возврощает True значит все Ок и продолжаем иначе если False то произошла ошибка
                    result = self.MainWhile()
                    if result:
                        if result == AOUTOR_ERROR: return True
                        continue
                    else:
                        self.socket_o.close()
                        break
            #self.quit()
        except KeyboardInterrupt:
            Debug.info("Exit by Keyboard Interrupt")
            exit()
        return False
    
    def stop(self):
        self.StopMainWhile = True
        if hasattr(self, 'socket_o'): 
            self.socket_o.shutdown(socket.SHUT_RD)
            self.socket_o.close()
                    
    def GetToken(self):
        if self.UseCacheToken:
            tok_c = CacheToken(self.chat_host).get()
            if tok_c:
                self.PrintGui('<font color="#0000ff">Токен найден в кеше.</font>')
                self.CurentToken = tok_c
                return True
            else:
                del tok_c
        
        Debug.info('Get token from: %s' % (self.chat_token_page))
        self.PrintGui('<font color="#0000ff">Get token...</font>')
        try:
            self.CurentToken = re.compile('token=([a-zA-Z0-9]{32})').search(urlopen(self.chat_token_page).read()).group(1)
        except Exception, err:
            self.PrintGui('<font color="#800000">Get token error.</font>')
            Debug.err('Get token error, '+str(err))
            return False
        if self.UseCacheToken: 
            c = CacheToken(self.chat_host)
            c.AddToken(self.CurentToken)
    
    # Handshaked
    def Handshaked(self):
        # Connecting
        self.PrintGui('<font color="#0000ff">Connecting...</font>')
        Debug.info('Connecting...')
        try:
            self.socket_o.connect( (self.chat_host, self.chat_port) )
            self.SocketActive = True
        except Exception, err_msg:
            #self.printLog("Error: Can\'t connect to server.")
            self.printLog("Error: %s" % (str(err_msg)))
            self.PrintGui('<font color="#800000">Error: %s</font>' % (str(err_msg)))
            return False
        self.PrintGui('<font color="#0000ff">Connected.</font>')
        Debug.info('Connected.')
        # Handshaked
        Debug.info("Handshaked...")
        self.PrintGui('<font color="#0000ff">Handshaked...</font>')
        try:
            self.writeSocket('<handshake version=4 token=%s/>' % (self.CurentToken))
        except:
            Debug.err("Socket error send")
            self.PrintGui('<font color="#800000">Socket error send</font>')
            return False
            
    # Create socket 
    def SetUpSocket(self):
        
        try:
            self.socket_o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, err_msg:
            Debug.err("Create socket error.")
            self.PrintGui('<font color="#800000">Create socket error: %s</font>' % (err_msg))
            self.stop()
        
    def MainWhile(self):
        # Комманды: 1 - сообщение чата, 2 - число онлайн, 3 - ошибка, 4 - заголовок с радио, 5 - верификация 
        # Первыеее 2 байта это размер, а последующий 1 байт тип комманды
        cmd = ''
        data_size = 0
        data = ''
        
        try:
            #TODO: Проверка соединения с чятом. (Для линукс систем больше это скорее всего)
            recv_tmp =  self.socket_o.recv(3)
            if self.StopMainWhile: return False
            if recv_tmp is None:
                self.PrintGui('<font color="#800000">Ошибка: переменная recv_tmp равна none type.</font>')
                return False
            
            if len(recv_tmp) == 3:
                data_size = unpack(">H", recv_tmp[:2])[0] # Это почему то список
                cmd = recv_tmp[2:3] # Тут будет тип сообщения (тип комманды)
            else:
                return AOUTOR_ERROR
                self.PrintGui('<font color="#800000">Ошибка: recv_tmp содержит мение 3 байт!</font>')
                return False

            if data_size:
                pass
            while len(data) < data_size:
                    add_size = data_size-len(data)
                    data += self.socket_o.recv(add_size)
                
        except Exception, err:
            str_error = str(err)
            Debug.err("%s" % (str_error))
            self.PrintGui('<font color="#800000">Error: %s</font>' % (str_error) )
            self.SocketActive = False
            return False
        
        if cmd:
            #! self.printLog("# Recv cmd: %s (Тип: %s): Size: %s" % (cmd.encode("hex"), self.cmd_description[cmd], data_size) )
            
            # 1 - сообщение чата
            if cmd == "\x01":
                self.PacketCounterMSG +=1
                self.GetGetter(data)
                        
                #Debug.debug('Принято: %s' % (data),Debug.OKBLUE)
                self.emit(QtCore.SIGNAL("conn_msg_chat(QString)"),QString.fromUtf8(data))
                return True
            
            # 2 - число онлайн
            if cmd == "\x02":
                self.emit(QtCore.SIGNAL("conn_online_users(int)"), (int(data)))
                return True
            
            # 3 Ошибка
            if cmd == "\x03":
                Debug.err(" Server err msg: %s" % (data))
                self.emit(QtCore.SIGNAL("conn_msg_chat_err(QString)"), QString.fromUtf8(data))
                self.stop()
                return False
                
            
            # 4 - Радио
            if cmd == "\x04":
                self.emit(QtCore.SIGNAL("conn_radio_stat(QString)"), QString.fromUtf8(data))
                return True
                
            # 5 - верификация (КАПЧА)  
            if cmd == "\x05":
                try:
                    self.PrintGui("Downloading captcha...")
                    self.conf_o.DATA_CAPTCHA = urlopen(data).read()
                    self.PrintGui("Done.")
                except:
                    Debug.err("Error load captcha from %s" % (data))
                    self.PrintGui("Error loading captcha from: %s" % (data))
                self.emit(QtCore.SIGNAL("conn_captcha_show()"))
                
                if self.UseCaptchaBreaker:
                    break_o = captcha_breaker.Capthca_crack(None,im=self.conf_o.DATA_CAPTCHA)
                    break_o.run()
                    Debug.info("Капча: "+str(break_o.strout))
                    time.sleep(10)
                    self.writeSocket(break_o.strout)
                return True
            
            # 7 - Успешный ввод капчи    
            if cmd == "\x07":
                self.cpatcha_enter = True
                Debug.debug(Debug.OKGREEN+"Успешно авторизован"+Debug.END)
                self.emit(QtCore.SIGNAL("conn_authorization_success()"))  
                return True
            return True
        
    def writeSocket(self,data):
        if not hasattr(self, 'socket_o'): return  False
        Debug.debug('Отправка[len: %s]: %s' % (len(data),data))
        data_sended = 0
        
        try:
            data_sended += self.socket_o.send(data)
            if data_sended != len(data):
                self.PrintGui( 'Ошибка отправки: отправленно %s байт из %s байт' %  (data_sended,len(data)) )

                return False
            #while data_sended <= len(data):
            #    #add_size = data_size-len(data)
            #    data_sended += self.socket_o.send(data)
            #    print 'sended %s size %s' % (data_sended, len(data))
        except socket.error, err:
            print str(err)
            self.PrintGui(str(err))
            return False
        return True
    def GetGetter(self,data):
        re_result = RE_SEARCH_POST_NUM.search(data)
        if re_result:
            try:
                id = int(re_result.groups(1)[0])
                
                if id == (self.GET_GETTER[0]-1):
                    self.writeSocket(self.GET_GETTER[1].replace('{get_post_id}',str(self.GET_GETTER[0])))
                    
            except Exception,err:
                print str(err)

    def PrintGui(self,text):
        self.emit(QtCore.SIGNAL("conn_msg_sys(QString)"), QString.fromUtf8(text))
        return text

    def printLog(self,str,print_n = False):
        if True:
            if print_n == False:
                Debug.info(str)
            else:
                Debug.info(str,0)

