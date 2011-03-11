#-*-coding: utf-8 -*-
'''
Created on 07.03.2011

@author: anon
'''
from PyQt4 import QtCore, QtGui, uic, QtWebKit
from class_tab import TAB
from lib.class_ChatConnection import ChatConnection
from lib.utilits import *
from lib.utilits_parser import *
#from __main__ import CONF_O,GLOBAL_VARS,P

class TAB_Connection(TAB):
    
    obj_mainWin = None
    obj_conn = None
    obj_parent = None
        
    chat_host = None
    chat_port = None
    chat_tokenpage = None
    chat_connName = ''
    
    def __init__(self): 
        #QtGui.QWidget.__init__(self,self.obj_parent)
        super(TAB_Connection,self).__init__(self.obj_parent)
    
    def init_TWO(self,connIndex=None,conn_par=None, mainWin=None, IsAutoConn=False):
        if False: 
            self.obj_parent = QtGui.QTabWidget()
            self.Message_Webkit = QtWebKit.QWebView()
            self.lineEdit_Captcha = QtGui.QLineEdit()
       
        self.obj_parent = mainWin.chat_tabs
        self.obj_mainWin = mainWin
        self.CONF_O = self.obj_mainWin.CONF_O
        self.connIndex = connIndex
        self.P = self.obj_mainWin.P
        #self.setWindowTitle('dasda [*]')
        #self.setWindowModified(True)
        self.SetupUI()
        
        if connIndex: self.Settings_Load(connIndex)
            
        if conn_par and False:
            if IsAutoConn:
                self.chat_host, self.chat_port, self.chat_token_page = conn_par
            else:
                self.lineEdit_Host.setText(str(conn_par[0]))
                self.lineEdit_Port.setText(str(conn_par[1]))
                self.lineEdit_Token.setText(str(conn_par[2]))
        
        #self.tab_SetIcon_Modifed()
        if False:
            Test_text = u'[20:39:39] <b>&lt;<a href="event:insert,28793"><font color="#000000">28793</font></a></b><b>&gt;</b> '
            self.AddText(u'[20:39:39] <b>&lt;<a href="event:insert,28792"><font color="#000000">28792</font></a></b><b>&gt;</b>  искра, и ты покроешь собой город <a href="http://2ip.ru">http://2ip.ru</a> AND http://rghost.ru/4698495.view')
            self.AddText(u'[20:39:39] <b>&lt;<a href="event:insert,28793"><font color="#000000">28793</font></a></b><b>&gt;</b>  <span class="reply">&gt;&gt;28792</span> искра, и ты покроешь собой город <a href="http://py-chat.tk">http://py-chat.tk</a>')
        
            self.AddText(Test_text+u' Text \\s <a href="http://rghost.ru/4698495.png">http://rghost.ru/4698495.png</a> Text')
            #self.WEB_view.setUrl(QtCore.QUrl('www.google.com'))
        #self.WEB_page.mainFrame().evaluateJavaScript()
        #self.WEB_page.mainFrame().setHtml('efefasfas')
        #self.Message_Webkit.load(QtCore.QUrl('http://www.google.com.ua/'))
        if IsAutoConn: self.conn_Start()
        
    def Settings_Load(self,index):
        sett = self.obj_mainWin.CONF_O.settings
        current_index = sett['servers'][self.connIndex]
        self.lineEdit_Name.setText(QtGui.QApplication.translate("MainWindow",current_index['user_nick'], None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_Name.setChecked(bool(current_index['NamefagMode']))
        self.lineEdit_Host.setText(current_index['host'])
        self.lineEdit_Port.setText(str(current_index['port']))
        self.lineEdit_Token.setText(current_index['token_page'])
        self.tab_SetName(current_index['name'])
            
    def Settings_Save(self,index):
        sett = self.obj_mainWin.CONF_O.settings
        current_index = sett['servers'][index]
        current_index['user_nick'] = unicode(self.lineEdit_Name.text()).encode('utf-8')
        
        #current_index['user_nick'] = str(QtCore.QString().fromUtf8(self.lineEdit_Name.text()))
        current_index['NamefagMode'] = bool(self.checkBox_Name.isChecked())
        self.obj_mainWin.CONF_O.Save()
        
    def SetupUI(self):
        uic.loadUi('res/tab.ui',self)
        self.WEB_page = QtWebKit.QWebPage(self.Message_Webkit)
        self.Message_Webkit.setPage(self.WEB_page)
        self.WEB_page.connect(self.WEB_page, QtCore.SIGNAL("linkClicked(QUrl)"), self.WEB_LinkClicked )
        
        self.WEB_page.setLinkDelegationPolicy(self.WEB_page.DelegateAllLinks)
        #self.WEB_page.contentsChanged()[sig]
        self.Message_Webkit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.Message_Webkit, QtCore.SIGNAL('customContextMenuRequested ( const QPoint & )'), lambda p: self.Message_Webkit_MenuRequested(p,self.Message_Webkit))
        #self.connect(self.WEB_page, QtCore.SIGNAL('linkHovered(QString,QString,QString)'), lambda *a: Debug.info(a))
        ##self.connect(self.WEB_page, QtCore.SIGNAL('customContextMenuRequested ( const QPoint & )'), self.Message_Webkit_MenuRequested)
        #self.Message_Webkit.contextMenuEvent_OLD = self.Message_Webkit.contextMenuEvent
        #self.Message_Webkit.contextMenuEvent = self.Message_Webkit_MenuRequested
        #self.Message_Webkit.cus
        
        self.WEB_page.mainFrame().setHtml(WebKitStyle.Build())
        self.groupBox_OnConnected.hide()
        self.groupBox_captcha.hide()
        self.connect(self.Button_Connect, QtCore.SIGNAL("clicked()"), self.conn_Start_parr )
 
        self.connect(self.ButtonSend, QtCore.SIGNAL("clicked()"),self.SendMessage)
        self.connect(self.Button_CaptchaOK, QtCore.SIGNAL("clicked()"), self.SendCaptcha)
        self.connect(self.Button_Disconnect, QtCore.SIGNAL("clicked()"), self.conn_Stop)
        
        self.lineEdit_Captcha.installEventFilter(self)
        self.Input.installEventFilter(self)
        self.installEventFilter(self)  
        #self.WEB_page.installEventFilter(self)
        #self.Message_Webkit.installEventFilter(self)
         
    def Messages_mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton and self.Messages.anchorAt(event.pos()):
            #self.Messages.emit(QtCore.SIGNAL("anchorClicked(QString)"), self.Messages.anchorAt(event.pos()))
            anchort_text = str(self.Messages.anchorAt(event.pos()))
            if anchort_text[:5] == 'event':
                event_split = anchort_text.split(",")#['event:insert', '28031']
                if event_split[0] == 'event:insert':
                    self.Input.insertPlainText('>>'+event_split[1]+' ')
                if  event_split[0] == 'event:block_user':
                    print 'Block %s' % (event_split[1])
        self.Messages.mousePressEvent_OLD(event)
        
    def Message_Webkit_MenuRequested(self,point,obj=None):
        #print  point,obj
        
        Menu = QtGui.QMenu(self)
        Menu.addAction(QtGui.QAction("New tab", self, triggered = lambda x=None: self.obj_mainWin.CreateTab(1)))
        DefaultMenu = self.WEB_page.createStandardContextMenu()
        DefActionsQList = DefaultMenu.actions()
        #del DefaultMenu
       
        #DefaultMenu.setTitle('Default actions')
        #Menu.addAction(QtGui.QAction("Test", self))
        #QtCore.QString().fromUtf8
        q_text = self.WEB_page.selectedText()
        if q_text:
            #text = unicode(q_text).encode('utf-8')
            text = qStringToStr(q_text)
            #text = str(q_text)
            text = '*>'+text+'* '
            Menu.addAction(QtGui.QAction('>>: '+text[:15]+'...', self,triggered = lambda x=0: self.Input.insertPlainText(QtCore.QString().fromUtf8(text))))
        
        for def_action in DefActionsQList:
            Menu.addAction(def_action)
        
        self.AddMainMenuActions(Menu)
        #Menu.removeAction()
        #print (dir(Menu))
        #self.WEB_page.linkClicked()
        
        Menu.exec_(self.Message_Webkit.mapToGlobal(point) )
        #self.Message_Webkit.contextMenuEvent_OLD(MenuEvent)
        
    def AddMainMenuActions(self,Menu):
        #Menu.addAction(QtGui.QAction("New tab", self, triggered = lambda x=None: self.obj_mainWin.CreateTab(1)))
        ##Menu_WordFilter = QtGui.QMenu(Menu)
        ##Menu_WordFilter.setTitle("Word filter")
        ##Menu_WordFilter.addAction(QtGui.QAction("Edit...", self,
        ##                             triggered = self.obj_mainWin.WordFilterWindow))
        ##Menu.addMenu(Menu_WordFilter)
        #Menu.addAction(QtGui.QAction("Exit", self,
        #                             triggered = self.obj_mainWin.close))
        Menu_View = QtGui.QMenu(Menu)
        Menu_View.setTitle("View")
        
        Menu_Style = QtGui.QMenu(Menu)
        Menu_Style.setTitle("Style")
        style_current = str(QtGui.QApplication.style().objectName())
        for style in QtGui.QStyleFactory.keys():
                #QtGui.QApplication.sty
                style = str(style)
                set_style = lambda x,s = style: self.obj_mainWin.changeStyle( s )
                style_action = QtGui.QAction(style, self, triggered = set_style )
                if style_current.upper() == style.upper():
                    style_action.setCheckable(True)
                    style_action.setChecked(True)
                    
                
                Menu_Style.addAction(style_action)
                del set_style
        
        Menu_View.addMenu(Menu_Style)
        Menu.addMenu(Menu_View)
        
        Menu.addSeparator()

    def OnConnected(self):
        #self.Messages.clear()
        self.groupBox_captcha.hide()
        self.groupBox_Connect.hide()
        self.groupBox_OnConnected.show()
        self.groupBox_Connect.setDisabled(False)
        self.Input.setFocus()
        
    def eventFilter(self,Qobj, event):
        '''If you delete the receiver object in this function, be sure to return true. Otherwise, 
        Qt will forward the event to the deleted object and the program might crash.'''
        #if 0: event = QtCore.QEvent()
                   
        if event.type() == QtCore.QEvent.KeyPress:
            if Qobj == self.lineEdit_Captcha and event.key() in (QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter):
                self.SendCaptcha()
                return True
            if Qobj == self.Input and event.key() in (QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter):
                self.SendMessage()
                return True
        if Qobj == self and event.type() == 26: self.tab_OnActive()
            
        if Qobj == self.Message_Webkit and event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                print event,event.type(),Qobj
                point =  event.pos()
                Menu = self.WEB_page.createStandardContextMenu()
                if Menu:
                    Menu.exec_(self.Message_Webkit.mapToGlobal(point) )
                else:
                    #del Menu
                    #Menu =
                    pass 
                #return True
        return False
        
    def conn_Start_parr(self):
        self.chat_host, self.chat_port, self.chat_tokenpage = (self.lineEdit_Host.text(),self.lineEdit_Port.text(),self.lineEdit_Token.text())
        self.conn_Start()
        
    def conn_Start(self):
        self.obj_conn = ChatConnection(self.obj_mainWin, self)
        self.SetSignalFor(self.obj_conn)
        self.obj_conn.chat_port = int(self.chat_port)
        self.obj_conn.chat_host = str(self.chat_host)
        self.obj_conn.chat_token_page = str(self.chat_tokenpage)
        self.groupBox_Connect.setDisabled(True)
        self.obj_conn.start()
            
    def conn_Stop(self): 
        if self.obj_conn:
            #self.Button_Disconnect.setDisabled(True)
            self.obj_conn.stop()
            
    def conn_Del(self):
        Debug.debug("Thread send del SIGNAL",Debug.RED)
        self.groupBox_captcha.hide()
        self.groupBox_OnConnected.hide()
        self.groupBox_Connect.show()
        self.groupBox_Connect.setDisabled(False)
        self.Button_Disconnect.setDisabled(False)
        self.Button_Connect.setDisabled(False)

    def SetSignalFor(self,obj):
        #print 'Set signal %s' % (obj)
        #self.connect(obj, QtCore.SIGNAL("output_chat(QString)"), self.AddText)
        self.obj_mainWin.connect(obj, QtCore.SIGNAL("conn_msg_chat(QString)"),self.SIGNAL_msg_chat)
        self.obj_mainWin.connect(obj, QtCore.SIGNAL("conn_msg_sys(QString)"), self.SIGNAL_msg_sys)
        self.obj_mainWin.connect(obj, QtCore.SIGNAL("conn_msg_chat_err(QString)"), self.SIGNAL_msg_chat)
        self.obj_mainWin.connect(obj, QtCore.SIGNAL("conn_captcha_show()"), self.Captcha_View)
        self.obj_mainWin.connect(obj, QtCore.SIGNAL("conn_authorization_success()"), self.OnConnected)
        self.obj_mainWin.connect(obj, QtCore.SIGNAL("conn_del()"), self.conn_Del)
        self.obj_mainWin.connect(obj, QtCore.SIGNAL("conn_online_users(int)"), lambda i: self.label_Online.setText('<b>Online:&nbsp;</b> %s' % (i)) )
        return
        self.connect(obj, QtCore.SIGNAL("setDownRange(int)"), self.DownRange)
        #self.connect(self.Threads_dic[obj_i], QtCore.SIGNAL("setDownVal(int)"), self.DownSetVal)
        #self.ProgressBar_buffer, 
        self.connect(obj, QtCore.SIGNAL("setDownVal(int)"), self.progDownBar, QtCore.SLOT('setValue(int)'))
        self.connect(obj, QtCore.SIGNAL("OnlineCounter(QString)"), self.label_Online.setText)
        self.connect(obj, QtCore.SIGNAL("RadioSetText(QString)"), lambda text:self.RadioText(text,'thread'))
        self.connect(obj, QtCore.SIGNAL("DisconnectUpdateGUI()"), self.DisconnectUpdateGUI)
        self.connect(obj, QtCore.SIGNAL("ClearChat()"), self.ClearChat)
        self.connect(obj, QtCore.SIGNAL("thread_is_die()"), self.Disconnected_)
        self.connect(obj, QtCore.SIGNAL("HideCaptcha(QString)"), self.HideCaptcha)
        self.connect(obj, QtCore.SIGNAL("msg_in()"), lambda: self.PlaySound_Event('msg_in'))
        
    def SIGNAL_msg_chat(self,s):
        s = qStringToStr(s)
        self.AddText(s)
        #self.tab_SetIcon_Modifed()
        self.P.Event('chat_message', s) 
        
    def SIGNAL_msg_sys(self,s):
        s = qStringToStr(s)
        self.AddText(s,False)
        #self.tab_SetIcon_Modifed()
        self.P.Event('chat_message_sys', s)
        
    def WEB_LinkClicked(self,qUrl):
        anchort_text= qUrl.toString()
        #print anchort_text
        if len(anchort_text) >= 5 and anchort_text[:5] == 'event':
                event_split = anchort_text.split(",")#['event:insert', '28031']
                if event_split[0] == 'event:insert':
                    self.Input.insertPlainText('>>'+event_split[1]+' ')
                if  event_split[0] == 'event:block_user':
                    print 'Block %s' % (event_split[1])
        else:
            pass

    def AddText(self,Text,parse=True):
        
        if False: result = ()
        if parse:
            result = ParsePost(Text)
            if len(result) == 3:
                time = result[0]
                num = result[1]
                msg = Parser_IN(result[2])
                #Debug.debug(msg)
                #Text = """<br />%s [%s]<br />%s""" % (num,time,msg)
                
                msg = msg.replace('\\', '&#92;')
                Text = """<div class="replico">
                    <span class="inContact">%s</span>
                    <span class="inContentTime">&nbsp;[%s]</span>
                    <br>
                    <div class="m_highlight"><div class="m_received">%s</div></div>
                    <div id="insert"></div>
                </div>""".replace('\n', '') % ('<a href="event:insert,%s" class="msgNum" name="p_%s">%s<a/>' % (num,num,num),time,msg)
                Text = AddImagesThumb(Text,self.obj_mainWin.CONF_O.settings['image_thumb_size'])
                self.WEB_page.mainFrame().evaluateJavaScript((QtCore.QString("appendMessage('%s')" % (Text))))
                #print 'Add: %s' % (msg)
                return
                
            else:
                #print 'NONE: %s' % (Text)
                Text = Text.replace('\n','<br />')
                Text = Text.replace('\r','<br />')
                
        self.WEB_page.mainFrame().evaluateJavaScript((QtCore.QString("appendMessage('%s')" % (Text+'<br />'))))
        #self.WEB_page.mainFrame().evaluateJavaScript((QtCore.QString("replaceLastMessage('%s')" % (Text+'<br />'))))
        #self.WEB_page.mainFrame().evaluateJavaScript((QtCore.QString("appendNextMessageNoScroll('%s')" % (Text+'<br />'))))
        #self.WEB_page.mainFrame().evaluateJavaScript((QtCore.QString("appendNextMessage('%s')" % (Text+'<br />'))))
    
    def SendMessage(self):
        msg = unicode(self.Input.toPlainText()).encode('utf-8')
        if not msg: return
        if self.checkBox_Name.isChecked():
            name = unicode(self.lineEdit_Name.text()).encode('utf-8')
            msg = name+msg
        
        if self.obj_conn.writeSocket(msg):
            self.Input.clear()
        
    def SendCaptcha(self): self.obj_conn.writeSocket(unicode(self.lineEdit_Captcha.text()).encode('utf-8'))
    
    def Captcha_View(self,img_data = None):
        image = QtGui.QPixmap()
        image.loadFromData(self.obj_mainWin.CONF_O.DATA_CAPTCHA)
        #width = image.width()height = image.height()
        self.lineEdit_Captcha.clear()
        self.label_Captcha.setPixmap(image)
        #self.label_Captcha.setEnabled(True)
        self.groupBox_captcha.show()
        self.lineEdit_Captcha.setFocus()
        self.obj_mainWin.CONF_O.DATA_CAPTCHA = None
    
    def OnClose(self,i):
        #print "Close tab %s - %s" % (i,self.tab_GetName())
        self.Settings_Save(self.connIndex)
        self.conn_Stop()
        self.deleteLater()
        
    def tab_OnActive(self):
        self.tab_SetIcon_None()
        
    def __del__(self):
        Debug.debug("~TAB",Debug.RED)
        #print 'DEL %s ' % (self.tab_GetName())
