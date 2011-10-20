#-*-coding: utf-8 -*-
'''
Created on 24.03.2011
@author: anon
'''

from __builtin__ import G
from PyQt4 import QtCore, QtGui, uic, QtWebKit
from class_tab import TAB

class TAB_web(TAB):
    obj_parent = object
    init_url = ''
    
    def __init__(self,url=None):
        self.obj_parent = G['chat_win'].chat_tabs
        self.init_url = url
        super(TAB_web,self).__init__(self.obj_parent)
        #self.WEB_view.setUrl(QtCore.QUrl('www.google.com'))
        #self.WEB_page.mainFrame().evaluateJavaScript()
        #self.WEB_page.mainFrame().setHtml('efefasfas')
        #self.Message_Webkit.load(QtCore.QUrl('http://www.google.com.ua/'))
        pass
    
    def init_TWO(self):
        self.SetupUI()
    
    
    def SetupUI(self):
        uic.loadUi('res/tab_web.ui',self)
        self.WEB_page = QtWebKit.QWebPage(self.Message_Webkit)
        self.Message_Webkit.setPage(self.WEB_page)
        
        
        def GoToUrl():
            url = self.lineEdit_Url.text()
            self.Message_Webkit.load(QtCore.QUrl(url))
            
        def OnCnangeUrl(url):
            #url_t = QtCore.QUrl.toString(url)
            url_t = url.toString()
            print "URL change"
            print url
            
            self.lineEdit_Url.setText(url_t)
        self.connect(self.pushButton_Go, QtCore.SIGNAL("clicked()"), GoToUrl)
        
        self.connect(self.Message_Webkit, QtCore.SIGNAL("urlChanged(const QUrl &)"), OnCnangeUrl)
        self.connect(self.Message_Webkit, QtCore.SIGNAL("titleChanged()"), OnCnangeUrl)
       
        print self.Message_Webkit.__class__
        if self.init_url:
            self.Message_Webkit.load(QtCore.QUrl(self.init_url))
        #self.connect(self.ButtonSend, QtCore.SIGNAL("clicked()"),self.SendMessage)
        #self.connect(self.Button_CaptchaOK, QtCore.SIGNAL("clicked()"), self.SendCaptcha)
        #self.connect(self.Button_Disconnect, QtCore.SIGNAL("clicked()"), self.conn_Stop)
        #self.connect(self.ButtonClear, QtCore.SIGNAL("clicked()"), self.MessagesClear)
        