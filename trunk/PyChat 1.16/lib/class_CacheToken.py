# -*- encoding: utf-8 -*-
'''
Created on 05.03.2011

@author: anon
'''
from lib.utilits import *
import socket, yaml, os, time

class CacheToken:
    '''
    Смотреть текущий ИП
    Смотреть словарь На предмет нахождение в ней текущего ИП
    Если ИП найдет то возвращать токен по ключу, если нет то False
    '''
    bd = {}
    bd_file_name = 'cache_of_token.yaml'
    chat_host = ''
    
    def __init__(self, chat_host):
        self.chat_host = chat_host;
        self.Load()
        
    def get(self):
        
        if not self.Load(): return False
        if not self.SetIP(): return False
        if not (self.chat_host in self.bd): return False
        
        for ip in self.bd[self.chat_host]:
            if ip == self.ip_current:
                return self.bd[self.chat_host][ip]
        return False
    
    def Save(self):
        try:
            file_h = file(self.bd_file_name,'w+')
            yaml.dump(self.bd, file_h, 
                    default_flow_style=None,
                    encoding='utf-8',
                    allow_unicode=True,)
            file_h.close()
            return True
        except Exception, err:
            Debug.err(err)
            return False
        
    def Load(self):
            
        if not os.path.exists('./'+self.bd_file_name):
            self.bd[self.chat_host] = {}
            self.Save()
            Debug.warr('File: %s not found. But it will be created' % (self.bd_file_name))
            return False
        
        try:
            file_h = file(self.bd_file_name,'r')
            self.bd = yaml.load(file_h)
        except Exception,err:
            Debug.err(err)
            file_h.close()
            return False
        
        if self.bd is None: 
            Debug.warr('File %s is empty!' % (self.bd_file_name))
            self.bd[self.chat_host] = {}
            file_h.close()
            self.Save()
            return False
        
        if not (self.chat_host in self.bd):
            self.bd[self.chat_host] = {}
            file_h.close()
            self.Save()
            return False
        return True
        
    def SetIP(self):
        try:
            s_o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_o.connect(('8.8.8.8',53))
            self.ip_current = s_o.getsockname()[0]
            s_o.close()
            return True
        except Exception,err:
            Debug.err(err)
            return False
        
    def AddToken(self,Token):
    
        if Token == None: return False
        if not self.SetIP(): return False
        if not self.Load(): return False
        print "Add: %s:%s" % (self.ip_current,Token)
        
        if self.chat_host in self.bd:
            if self.ip_current in self.bd[self.chat_host]:
                self.bd[self.chat_host][self.ip_current+str(time.time())] = Token
                Debug.warr('IP %s have more tokens (%s)'  % ( self.ip_current,Token ))
            else:
                self.bd[self.chat_host][self.ip_current] = Token
                print "OK"
        self.Save()    
        return True
