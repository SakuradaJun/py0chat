#-*-coding: utf-8 -*-
'''
Created on 04.01.2011

@author: anon
'''
from PyQt4 import QtCore, QtGui

class Qlabel_click(QtGui.QLabel):

    def    mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            self.emit(QtCore.SIGNAL("closeMe()"))
        QtGui.QLabel.mousePressEvent(self,event)
        
        
class Popup_OLD(QtGui.QWidget):
    
    s = u'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Ubuntu'; font-size:10pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">&lt;</span><a href="event:insert,2665909"><span style=" font-weight:600; text-decoration: underline; color:#3366ff;">2665909</span></a><span style=" font-weight:600;">&gt;</span> <span style=" font-weight:600;">&lt;питон-кун&gt; </span><span style=" color:#ff6600;">&gt;&gt;2665908</span> Аххх. Нуу да... Может. Тогда и HTML там печатать можно будет.</p></body></html>'''
    close_timeout = 5000 # 3000
    Opacity = 0.9
    main_w_obj = None
    bottom_offset = 24 # Отступ от низа 26
    
    def __init__(self,text = None,parent = None, timeout=5000,show=True):
        QtGui.QWidget.__init__(self)
        self.main_w_obj = parent
        flag = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.ToolTip
        # WORK QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.ToolTip
        #!QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup
        
        
        #QtCore.Qt.Popup| QtCore.Qt.WindowStaysOnTopHint
        self.setWindowFlags(flag)#QtCore.Qt.Popup|QtCore.Qt.WindowStaysOnTopHint| QtCore.Qt.SplashScreen
        #! self.setAttribute(QtCore.Qt.WA_DeleteOnClose );
        
        if text == None: text = self.s
        self.close_timeout = timeout
        self.Label = Qlabel_click(self)
        self.Label.setText(text)
        self.Label.setWordWrap(True)
        #QtCore.Qt.FramelessWindowHint| QtCore.Qt.WindowStaysOnTopHint
        
        
        self.setGeometry(QtCore.QRect(0,0,400,40))
        self.Label.setGeometry(QtCore.QRect(0,0,400,40))
        self.SetUpSignal()
        self.setWindowOpacity(self.Opacity)

        #self.timer = QtCore.QTimer()
        #self.timer.start(100)
        #self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.de_op)
        

            
    def _show(self):
        res = self.GetMovePoint()
        #print "Move %s %s" % res
        self.move(res[0],res[1])
        #1010 1280
        #self.move(1280,988)# Вправо-в лево, вверх в низ
            
        
        self.show()
            
        if self.close_timeout != 0:
            self.Timer = QtCore.QTimer()
            #self.Timer.start(self.close_timeout)
            #self.Timer.singleShot(self.close_timeout, self.close_optan );
            #Timer.singleShot(self.close_timeout, self, QtCore.SLOT('close()') );
            #self.connect(Timer, QtCore.SIGNAL("timeout()"), self.close_optan)
            self.Timer.singleShot(self.close_timeout, self.close_optan );
            
    def __del__(self):
        #print "~Del popup"
        #QtGui.QWidget.destroy()
        pass
        
    def GetMovePoint(self):
        desktop = QtGui.QApplication.desktop() #.availableGeometry().
        height = desktop.height()
        width = desktop.width()
        #print "Desktop Height: %s Width: %s" % (height,width)
        
        s_height = self.height()
        s_width = self.width()
        #print "Self size: %s %s" % (s_height,s_width)
        #1680 - 400
        #Desktop Height: 1050 Width: 1680
        #Self size: 40 400
        #self.parent()
        #14,6
        if self.self_num >= 1:
            #print "Всплывающих окон %s" % (self.self_num)
            height = height - ((self.height() + 5 )*self.self_num)
        return ((width - s_width) ,height-s_height- self.bottom_offset)
       
        if len(self.main_w_obj.msg_popup_list) > 1:
            print "Всплывающих окон %s" % (self.main_w_obj.msg_popup_list)
            height = height- (40*len(self.main_w_obj.msg_popup_list))

        
        #        0,0,1680, 1002)
        #return m
    
    def SetUpSignal(self):
        #self.connect(self.Label, QtCore.SIGNAL("closeMe()"), self.close_optan)
        pass
        
    def close_optan(self):
        #print "Close() %s " % (self.self_num)
        #self.Timer.stop()
        #del self.Timer
        del self.main_w_obj.msg_popup_list[self.my_id]
        
        self.close()
        #self.deleteLater()
        #self.destroy()
        #del self
        import sys
        
        #print "Сейчас ссылок %s на этот обьект" % (sys.getrefcount(self))
        return
        i_float = 1.0
        for trans in xrange(99):
            #i_float = i_float-0.1
            self.de_op()
            #self.setWindowOpacity(i_float)
            time.sleep(0.01)
        #self.close()
"""       
    def SetSizes(self):
        position = 0
        geometry= QtGui.QApplication.desktop().availableGeometry();
        moveToPointX = 0
        moveToPointY = 0
        
        #0
        moveToPointX = geometry.left();
        moveToPointY = geometry.top() + (1 - 1) * self.height();
        self.move(moveToPointX, moveToPointY);
        #PyQt4.QtCore.QRect(0, 24, 1680, 1002)
        return 'N'

        
    def tim(self):
        print "timer!"
        
    def de_op(self):
        #print "timer!"
        if self.windowOpacity() >= 1.1 or self.windowOpacity() <= 0.0:
            self.setWindowOpacity(1.0)
        self.setWindowOpacity(self.windowOpacity()-0.1)
        #print 'Set %s' % (self.windowOpacity())
        
"""

class Popup(QtGui.QWidget):
    
    s = u'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Ubuntu'; font-size:10pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">&lt;</span><a href="event:insert,2665909"><span style=" font-weight:600; text-decoration: underline; color:#3366ff;">2665909</span></a><span style=" font-weight:600;">&gt;</span> <span style=" font-weight:600;">&lt;питон-кун&gt; </span><span style=" color:#ff6600;">&gt;&gt;2665908</span> Аххх. Нуу да... Может. Тогда и HTML там печатать можно будет.</p></body></html>'''
    close_timeout = 5000 # 3000
    Opacity = 0.7
    main_w_obj = None
    bottom_offset = 28 # Отступ от низа 26
    
    popUp_width = 400
    popUp_height = 40
    popUp_def_position = (1280, 982)#942-8
    popUp_margin = 8
    
    def __init__(self,text = None,parent = None, timeout=5000,show=True):
        QtGui.QWidget.__init__(self)
        self.main_w_obj = parent
        flag = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.ToolTip
        # WORK QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.ToolTip
        #!QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup
        
        
        #QtCore.Qt.Popup| QtCore.Qt.WindowStaysOnTopHint
        self.setWindowFlags(flag)#QtCore.Qt.Popup|QtCore.Qt.WindowStaysOnTopHint| QtCore.Qt.SplashScreen
        #! self.setAttribute(QtCore.Qt.WA_DeleteOnClose );
        
        if text == None: text = self.s
        self.close_timeout = timeout
        self.Label = Qlabel_click(self)
        self.Label.setText(text)
        self.Label.setWordWrap(True)
        #QtCore.Qt.FramelessWindowHint| QtCore.Qt.WindowStaysOnTopHint
        
        startWidthPos = QtGui.QApplication.desktop().width()-self.popUp_width# Ширина
        startHeightPos =  QtGui.QApplication.desktop().height()-self.popUp_height-self.bottom_offset # Высота
        #PyQt4.QtCore.QRect(1280, 974, 400, 40) Для выдвижения
        #print "Start Pos PyQt4.QtCore.QRect(%s, %s, 400, 40)" % ( startWidthPos, startHeightPos)
        x = startWidthPos# Лево, Право ШИРИНА 1280
        y = startHeightPos# вверх, Вниз! ВЫСОТА 974
        self.setGeometry(QtCore.QRect(x, y, self.popUp_width,self.popUp_height))
        self.Label.setGeometry(QtCore.QRect(0,0, self.popUp_width,self.popUp_height))
        self.SetUpSignal()
        self.setWindowOpacity(self.Opacity)
        
        '''
        self.timer_two = QtCore.QTimer()
        self.timer_two.start(4000)
        self.connect(self.timer_two, QtCore.SIGNAL("timeout()"), self._show)
        '''
        

            
    def _show(self):
        self.show()
        if self.close_timeout != 0:
            self.Timer = QtCore.QTimer()
            self.Timer.singleShot(self.close_timeout, self.close_optan );
        style = 0 # 1 2

        res = self.GetMovePoint()

        #print "Move %s %s" % res
        #self.slideHorizontallyRight(res)
        
        self.move(res[0],res[1])
        #1010 1280
        #self.move(1280,988)# Вправо-в лево, вверх в низ
        
            
    def __del__(self):
        #print "~popup"
        #QtGui.QWidget.destroy()
        pass
        
    def GetMovePoint(self):
        print "\033[91mthis: %s\033[0m" % (self.my_id)
        for one in self.main_w_obj.msg_popup_list:
            print '%s -> %s' % (one,self.main_w_obj.msg_popup_list[one])
        
        
        if self.my_id >= 2:
            if not self.my_id-1 in self.main_w_obj.msg_popup_list:
                return self.popUp_def_position
            print "Try %s" % (self.my_id-1)
            obj = self.main_w_obj.msg_popup_list[self.my_id-1]
            old_y = str(obj.y())
            old_x = str(obj.x())
            print "OLD %s %s" % (old_y,old_x)
            
            obj.tmp_h = obj.y()
            too_y = (obj.tmp_h -  obj.height()  * self.main_w_obj.popUp_count-1)- self.popUp_margin
            too_x = obj.x()
            
            print "%s Move %s to: x: %s x: %s   " % (self.my_id,self.my_id-1,too_x,too_y)
            obj.move(too_x,too_y)
            obj.show()
            #del obj
        return self.popUp_def_position
        desktop = QtGui.QApplication.desktop() #.availableGeometry().
        height = desktop.height()
        width = desktop.width()
        #print "Desktop Height: %s Width: %s" % (height,width)
        #Desktop Height: 1050 Width: 1680
        
        s_height = self.height()
        s_width = self.width()
        #print "Self size: %s %s" % (s_height,s_width)
        #1680 - 400
        #Self size: 40 400
        #self.parent()
        #14,6

        if self.self_num != 1:
            height = height - ((self.height() + self.popUp_margin) * (self.self_num-1))
        #PyQt4.QtCore.QRect(1273, 975, 400, 40) лучшая позиция, начальная
        # PyQt4.QtCore.QRect(1280, 974, 400, 40) Для выдвижения
        return ((width - s_width) ,height-s_height- self.bottom_offset)
    
    def slideHorizontallyRight(self,EndPoint):
        pass
    
    def SetUpSignal(self):
        self.connect(self.Label, QtCore.SIGNAL("closeMe()"), self.close_optan)
        pass
        
    def close_optan(self):
        del self.main_w_obj.msg_popup_list[self.my_id]
        self.close()
        
class Move_Widget(QtGui.QWidget):
    
    def moveEvent(self,event):
        #print "Move! %s" % (event)
        #self.move(0,0)
        #return
        self.emit(QtCore.SIGNAL("move_event()"))
        QtGui.QWidget.moveEvent(self, event)
        
        
class TestWin(Move_Widget):
    w_flag =  QtCore.Qt.FramelessWindowHint
    # QtCore.Qt.FramelessWindowHint| QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.ToolTip
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowFlags(self.w_flag)
        self.Label = QtGui.QLabel(self)
        #self.Label.setText('TEST!')
        self.Label.setWordWrap(True)
        self.connect(self, QtCore.SIGNAL('move_event()'),self.env_move)
        self.setWindowTitle('Test')
        self.setGeometry(QtCore.QRect(0,0,400,40))
        self.show()
        
    def env_move(self):
        g = self.geometry() 
        #print "Margins: %s" + self.getContentsMargins()
        print g
        #self.Label.setText(g)
        
