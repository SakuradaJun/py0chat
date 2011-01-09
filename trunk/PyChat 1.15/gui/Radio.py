#-*-coding: utf-8 -*-
'''
Created on 06.01.2011

@author: anon
'''
import gui
from PyQt4 import QtCore, QtGui
from PyQt4 import phonon
conf_o = None


class M_Obj(phonon.Phonon.MediaObject):
    
    def bufferStatus(self,*a):
        
        print "bufferStatus!!! %s" % (a)
        phonon.Phonon.MediaObject.bufferStatus(*a)

class Radio(object):

    m_media = None
    Radiotitles_hist = {}
    RadioUrl_ = {
                u'Radioanon':'http://radioanon.ru:8000/radio',
                u'Эхо москвы':'http://w04-cn03.akadostream.ru:8000/moscowecho48.mp3',
                u'Какое то там...':'http://stream1.radiostyle.ru:8001/luu25-mm'
    }
    RadioUrl = {}
    RadioUrlActive = {}
    IsPlay = False
    
    def __init__(self,parent = None):
        self = parent
        global conf_o 
        conf_o = self.conf_o
        #gui.MessageBox()
        self.label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.label, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), 
                      lambda point,child_obj = self.label: self.RadionRequestMenu(point,child_obj))
        
        self.PushButton_Play.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.PushButton_Play, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     lambda point,child_obj = self.PushButton_Play: self.RadionRequestMenu(point,child_obj))
        
        self.ProgressBar_buffer.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.ProgressBar_buffer, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), 
                     lambda point,child_obj = self.ProgressBar_buffer: self.RadionRequestMenu(point,child_obj)) 
        
    def ClearRadiotitles_hist(self): self.Radiotitles_hist = {}
    
    def RadionRequestMenu(self, point,child_obj = None):
        RadionLabelMenu = QtGui.QMenu(self) # self
        RadionSubMenuRadioSelect = QtGui.QMenu(self)
        RadionSubMenuRadioSelect.setTitle(u'Слушать радио')
        if self.RadioUrl:
            for radio in self.RadioUrl:
                dic_d = {radio : self.RadioUrl[radio]}
                lamb_f = lambda x,t_dic = dic_d: ( self.RadioSetCurrent(t_dic))
                action_sub = action_sub = QtGui.QAction(u"%s - %s" % (radio,self.RadioUrl[radio]), self, triggered = lamb_f) 
                del lamb_f
                #self.RadioSetCurrent(dic_d) and 
                #print "Create action form %s Url: %s" % (radio,self.RadioUrl[radio])
               
                if self.RadioUrlActive:
                    if self.RadioUrlActive == {radio:self.RadioUrl[radio]}:
                        action_sub.setCheckable(True)
                        action_sub.setChecked(True)
                RadionSubMenuRadioSelect.addAction(action_sub)
                del action_sub
        RadionSubMenuRadioSelect.addSeparator()
        RadionSubMenuRadioSelect.addAction(QtGui.QAction(u"Добавить!" , self, triggered = self.AddRadioUrl) )
        
        #self.RadionSubMenuRadioSelect.
        RadionLabelMenu.addMenu(RadionSubMenuRadioSelect)
        #!RadionLabelMenu.addSeparator()
        if self.Radiotitles_hist:
            all = ''
            for title in self.Radiotitles_hist:
                title = self.Radiotitles_hist[title]
                #copy_f = lambda text = title: QtGui.QApplication.clipboard().setText(text)
                action_o = QtGui.QAction("Copy: %s" % (title), self, 
                                         triggered = lambda x,s = title: QtGui.QApplication.clipboard().setText(s) )
                RadionLabelMenu.addAction(action_o)
                all = all + title + '\r\n'
            RadionLabelMenu.addSeparator()
            RadionLabelMenu.addAction(QtGui.QAction("Clear", self ,
                                                    triggered = self.ClearRadiotitles_hist))
            RadionLabelMenu.addAction(QtGui.QAction("Copy all", self ,
                                                    triggered = lambda x,text=all: QtGui.QApplication.clipboard().setText(text)))
        else:
            #! RadionLabelMenu.addAction(QtGui.QAction("None", self,triggered=QtGui.qApp.aboutQt))
            #RadionLabelMenu.addAction(QtGui.QAction("Copys", self,triggered = self.de_op))
            #RadionLabelMenu.addAction(QtGui.QAction("Copys", self,triggered = self.de_op))
            #RadionLabelMenu.addAction(QtGui.QAction("Copys", self,triggered = self.de_op))
            #RadionLabelMenu.addAction(self.maximizeAction)
            #RadionLabelMenu.addAction(self.restoreAction)
            #RadionLabelMenu.addAction(self.action_about)
            pass
        if child_obj:
            RadionLabelMenu.exec_(child_obj.mapToGlobal(point) )
            return
        RadionLabelMenu.exec_(self.label.mapToGlobal(point) )
    
    def PrintConfigArray(self):
        self.DialogConfigArray = QtGui.QPlainTextEdit()
        d = {}
        
        #for i in conf_o.settings:
        #    self.DialogConfigArray.appendPlainText(i.values())
        for i in conf_o.settings:
            self.DialogConfigArray.appendPlainText(i)
        self.DialogConfigArray.show()
        
    def RadioText(self,text,sendler=None):
        if self.IsPlay and sendler == 'thread':
            return
            #print '%s %s' % (text,sendler)
        self.label.setText(u'<b>Radio:&nbsp;</b> ' + QtCore.QString.fromUtf8(text))      
        self.Radiotitles_hist[len(self.Radiotitles_hist)] = QtCore.QString.fromUtf8(text)    
        
    def RadioSetCurrent(self,radioName): self.RadioUrlActive = radioName

    def RadioSetSIGNAL(self):
        self.connect(self.m_media, QtCore.SIGNAL("bufferStatus(int)"), self.ProgressBar_buffer, QtCore.SLOT('setValue(int)'))
        #self.connect(self.m_media, QtCore.SIGNAL("bufferStatus(int)"), self.Buf)
        
        #self.connect(self.m_media, QtCore.SIGNAL("bufferStatus(int)"), self.bufferStatus_m)
        #! self.connect(self.m_media, QtCore.SIGNAL("finished()"), self.RadionFinish)
        #!self.connect(self.m_media, QtCore.SIGNAL("metaDataChanged()"), self.RadionFinish)
        #! self.connect(self.m_media, QtCore.SIGNAL("stateChanged()"), self.RadionFinish)
        
    def Chaneds(self,*a):
        #print "Change!"
        ArtistMetaData = self.m_media.metaData(phonon.Phonon.ArtistMetaData)
        TitleMetaData = self.m_media.metaData(phonon.Phonon.TitleMetaData)
        try:
            Artist = u''
            Title = u''
            for f in ArtistMetaData:
                #print str(f).decode('utf8')
                Artist += str(f).decode('utf8')
            for f in TitleMetaData:
                #print str(f).decode('utf8')
                Title += str(f).decode('utf8')
                #.decode('utf8').encode('cp1255')
            #Artist =  (str(f) )
            #Artist =  u''.join((str(f) for f in ArtistMetaData))
            #print Artist
            #if title == 'Streaming Data': return
            #title = title+' - '
            #Title = u''.join((str(f) for f in TitleMetaData))
            title = '%s - %s' % (Artist,Title)
        except Exception, err:
            print str(err)
            return 
        #!print ''.join((str(f) for f in self.m_media.metaData(phonon.Phonon.AlbumMetaData)))
        
        #title =  ''.join((str(f) for f in self.m_media.metaData(phonon.Phonon.DateMetaData)))
        
        if str(self.label.text()) != title:
            self.RadioText(title)
        
        
    def delayedInit(self):
        if not self.m_media:            
            #self.m_media = phonon.Phonon.MediaObject(self)
            self.m_media = M_Obj()
            self.connect(self.m_media, QtCore.SIGNAL("bufferStatus( int )"), self.Buf)
            self.connect(self.m_media, QtCore.SIGNAL("metaDataChanged()"), self.Chaneds)
            self.RadioSetSIGNAL()
            #self.slider = phonon.Phonon.SeekSlider()
            
            
            #self.slider.setMediaObject(self.m_media)
            #self.slider.show()
            #slider = new Phonon::SeekSlider(this);
            #slider->setMediaObject(&m_MediaObject);
            #volume = new Phonon::VolumeSlider(&m_AudioOutput);
     
            
            #! self.m_media.disconnectNotify()
            audioOutput = phonon.Phonon.AudioOutput(phonon.Phonon.MusicCategory, self)
            #self.volumeSlider = phonon.Phonon.VolumeSlider(audioOutput)
            #self.volumeSlider.show()
            phonon.Phonon.createPath(self.m_media, audioOutput)
            
    def Buf(self,buf): print 'buf: %' % (buf)
        
    def RadionFinish(self, *a): pass
        
    def RadionPlay(self,bool):
        if bool:
            if not self.RadioUrl:
                self.PushButton_Play.setChecked(False)
                gui.MessageBox(u'Url список для радио пуст.\n Добавте url для того что бы играть.',type=QtGui.QMessageBox.Critical, title = u'Ошибка')
                return
            self.delayedInit()
            if self.RadioUrlActive: # Если не пуст
                url = self.RadioUrlActive[self.RadioUrlActive.keys()[0]]
            else:
                url = self.RadioUrl[self.RadioUrl.keys()[0]]
                self.RadioUrlActive = {self.RadioUrl.keys()[0]:url}
                
            #self.ProgressBar_buffer.show()
            self.m_media.setCurrentSource(phonon.Phonon.MediaSource(QtCore.QUrl(url)))
            self.IsPlay = True
            self.m_media.play()
            
            self.PushButton_Play.setText('Stop')
        else:
            if not self.m_media: return
            self.ProgressBar_buffer.hide()
            self.IsPlay = False
            self.m_media.stop()
            
            self.m_media.clear()
            self.m_media.clearQueue()
            self.m_media = None
            self.PushButton_Play.setText('Play')
            '''
            @copy_to_clipboard
            def de_op(self,*a):
                print "Copy: %s" % (a)
            '''
    def AddRadioUrl(self):
        from PyQt4 import uic
        
        win =  self.op_servers = uic.loadUi('gui/Radio_add_dialog.ui')
        win.setWindowTitle(u'Добавить ридио Url')
        if win.exec_():
            print "Save!"
            print win.lineEdit_Url.text() 
            print win.lineEdit_Name.text() 
        #win = QtGui.QDialog(self)
        #win.exec_()
        pass
