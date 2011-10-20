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

from __builtin__ import G
from PyQt4 import QtCore
#from PyQt4.QtCore import QString

import urllib2
import socket, re, yaml, os, time
from struct import unpack
from lib.utilits import *
from lib.class_CacheToken import CacheToken
import binascii
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
    UseCacheToken = False
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
        QtCore.QThread.__init__(self, obj_tab)
        if False: self.socket_o = socket.socket()
        self.obj_tab = obj_tab
        self.cmd_description = cmd_description

    # Установка настроек
    def Set_Vars(self):
        if self.chat_host == 'py-chat.tk':
            self.UseCacheToken = False
        self.admin_key = G['config'].settings['admin_pass']
        #self.chat_port = G['config'].settings['servers'][G['config'].settings['current_server']]['port']
        #self.chat_host = G['config'].settings['servers'][G['config'].settings['current_server']]['host']
        #self.chat_token_page = G['config'].settings['servers'][G['config'].settings['current_server']]['token_page']

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
        self.PrintGui('<font color="#800000">Disconnected.</font>')
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
            if self.chat_host == 'py-chat.tk':
                return True
            #self.quit()
        except KeyboardInterrupt:
            Debug.info("Exit by Keyboard Interrupt")
            exit()
        return False
    
    def stop(self):
        self.StopMainWhile = True
        if hasattr(self, 'socket_o'): 
            try:
                self.socket_o.shutdown(socket.SHUT_RD)
                self.socket_o.close()
            except Exception , e:
                Debug.warr(e)
                self.PrintGui('<font color="#800000">%s</font>' % (e))
                return False
                    
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
            #data = urllib.request.urlopen(self.chat_token_page).read()
            data = urllib2.urlopen(self.chat_token_page).read()
            self.CurentToken = re.compile('token=([a-zA-Z0-9]{32})').search(data).group(1)
        except Exception , err:
            self.PrintGui('<font color="#800000">Get token error: %s</font>' % (err))
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
        except Exception , err:
            #self.printLog("Error: Can\'t connect to server.")
            self.printLog("Error: %s" % err)
            self.PrintGui('<font color="#800000">Error: %s</font>' % err)
            return False
        self.PrintGui('<font color="#0000ff">Connected.</font>')
        Debug.info('Connected.')
        # Handshaked
        Debug.info("Handshaked...")
        self.PrintGui('<font color="#0000ff">Handshaked...</font>')
        
        if not self.writeSocket('<handshake version=4 token=%s/>' % self.CurentToken):
            return False
        else:
            return True
        '''
        except Exception , err:
            Debug.err("Socket write error: %s" % err)
            self.PrintGui('<font color="#800000">Socket write error: %s</font>' % err)
            return False
        '''
            
    # Create socket 
    def SetUpSocket(self):
        
        try:
            self.socket_o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error ,  err:
            Debug.err("Create socket error.")
            self.PrintGui('<font color="#800000">Create socket error: %s</font>' % (err))
            self.stop()
        
    def MainWhile(self):
        # Комманды: 1 - сообщение чата, 2 - число онлайн, 3 - ошибка, 4 - заголовок с радио, 5 - верификация 
        # Первыеее 2 байта это размер, а последующий 1 байт тип комманды
        cmd = b''
        data_size = 0
        data = b''
        
        try:
            #TODO: Проверка соединения с чятом. (Для линукс систем больше это скорее всего)
            recv_tmp =  self.socket_o.recv(3)
            if len(recv_tmp) < 1: return False
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
                
        except Exception , err:
            str_error = str(err)
            Debug.err("%s" % (str_error))
            self.PrintGui('<font color="#800000">Error: %s</font>' % (str_error) )
            self.SocketActive = False
            return False
        #bytes(data,'UTF-8')
        #s_tmp = recv_tmp
        #s_tmp += data
        #Debug.info(binascii.hexlify(s_tmp))
        try:
            data = data #.encode('utf8')
        except Exception , e:
            data = ''
            self.PrintGui('<font color="#800000">Decode data to string error[cmd %s]: %s</font>' % (cmd,e))
        
        
        
        if cmd:
            #! self.printLog("# Recv cmd: %s (Тип: %s): Size: %s" % (cmd.encode("hex"), self.cmd_description[cmd], data_size) )
            
            # 1 - сообщение чата
            if cmd == b"\x01":
                self.PacketCounterMSG +=1
                self.GetGetter(data)
                        
                #Debug.debug('Принято: %s' % (data),Debug.OKBLUE)
                self.emit(QtCore.SIGNAL("conn_msg_chat(QString)"),QtCore.QString.fromUtf8(data))#
                return True
            
            # 2 - число онлайн
            if cmd == b"\x02":
                self.emit(QtCore.SIGNAL("conn_online_users(int)"), (int(data)))
                return True
            
            # 3 Ошибка
            if cmd == b"\x03":
                Debug.err(" Server err msg: %s" % (data))
                #self.emit(QtCore.SIGNAL("conn_msg_chat_err(QString)"), data)#
                self.emit(QtCore.SIGNAL("conn_msg_chat_err(QString)"), 
                          QtCore.QString.fromUtf8(data))
                self.stop()
                return False
                
            
            # 4 - Радио
            if cmd == b"\x04":
                self.emit(QtCore.SIGNAL("conn_radio_stat(QString)"), 
                                        QtCore.QString.fromUtf8(data))#
                return True
                
            # 5 - верификация (КАПЧА)  
            if cmd == b"\x05":
                try:
                    self.PrintGui("Downloading captcha...")
                    #G['config'].DATA_CAPTCHA = urllib.request.urlopen(data).read()
                    Debug.info('Get captcha: %s' % data)
                    #cap_data = urllib.request.urlopen(data).read()
                    cap_data = urllib2.urlopen(data).read()
                    cap_data = QtCore.QByteArray(cap_data)
                    self.PrintGui("Done.")
                except Exception , err:
                    Debug.err("Error load captcha from %s. %s" % (data,err))
                    self.PrintGui("Error loading captcha from: %s . %s" % (data,err))
                self.emit(QtCore.SIGNAL("conn_captcha_show(QByteArray)"),cap_data)
                del cap_data
                return True
            
            # 7 - Успешный ввод капчи    
            if cmd == b"\x07":
                self.cpatcha_enter = True
                Debug.debug(Debug.OKGREEN+"Успешно авторизован"+Debug.END)
                self.emit(QtCore.SIGNAL("conn_authorization_success()"))  
                return True
            return True
        
    def writeSocket(self,data):
        if not hasattr(self, 'socket_o'): return  False
        data = data.replace('\r\n',' ')
        data = data.replace('\n',' ')
        Debug.debug('Отправка[len: %s]: %s' % (len(data),data))
        data_sended = 0
        #data = bytes(data,'utf8')
        
        try:
            data_sended += self.socket_o.send(data)
            if data_sended != len(data):
                self.PrintGui( 'Ошибка отправки: отправленно %s байт из %s байт' %  (data_sended,len(data)) )

                return False
            

            #while data_sended <= len(data):
            #    #add_size = data_size-len(data)
            #    data_sended += self.socket_o.send(data)
            #    print 'sended %s size %s' % (data_sended, len(data))
        except socket.error ,  err:
            print (err)
            self.PrintGui(err)
            return False
        return True
        
    def GetGetter(self,data):
        re_result = RE_SEARCH_POST_NUM.search(data)
        if re_result:
            try:
                id = int(re_result.groups(1)[0])
                
                if id == (self.GET_GETTER[0]-1):
                    self.writeSocket(self.GET_GETTER[1].replace('{get_post_id}',str(self.GET_GETTER[0])))
                    
            except Exception , err:
                print (err)

    def PrintGui(self,text):
        text = QtCore.QString.fromUtf8(text)
        self.emit(QtCore.SIGNAL("conn_msg_sys(QString)"), text)#
        return text

    def printLog(self,s,print_n = False):
        if True:
            if print_n == False:
                Debug.info(s)
            else:
                Debug.info(s,)

