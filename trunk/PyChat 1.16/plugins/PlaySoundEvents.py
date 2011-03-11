#-*-coding: utf-8 -*-
'''
Created on 24.02.2011

@author: anon
'''
from PyQt4 import QtCore, QtGui
from PyQt4 import phonon
from lib.class_plugin_core import Plugin

class PLugin_PlaySound(Plugin):

    sound_media = None
    Name = 'Play sound events'
    obj_mainWin = None
    
    def init_gui(self):
        self.obj_mainWin.Button_SoundSwitch = QtGui.QToolButton(self.obj_mainWin.centralwidget)
        
        #self.obj_mainWin.Button_SoundSwitch.move
        
        Icon_SoundSwitch = QtGui.QIcon()
        Icon_SoundSwitch.addPixmap(QtGui.QPixmap("res/Images/sound_on_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.obj_mainWin.Button_SoundSwitch.setIcon(Icon_SoundSwitch)
        self.obj_mainWin.Button_SoundSwitch.setAutoRaise(True)
        self.obj_mainWin.Button_SoundSwitch.setCheckable(True)
        self.obj_mainWin.Button_SoundSwitch.setChecked(False)
        self.obj_mainWin.Button_SoundSwitch.setObjectName("ToolButton_SoundSwitch")
        self.obj_mainWin.Layout_Top.addWidget(self.obj_mainWin.Button_SoundSwitch)
        self.obj_mainWin.Button_SoundSwitch.show()
        
    
    def init_sound(self,parent = None):
        self.p("sound init")
        if not self.sound_media:
                self.p("create media")
                self.sound_media = phonon.Phonon.MediaObject(parent)
                self.sound_audioOutput = phonon.Phonon.AudioOutput(phonon.Phonon.MusicCategory, parent)
                phonon.Phonon.createPath(self.sound_media, self.sound_audioOutput)
        self.PlaySound_Test()
        
    def p(self,s):
        print '# %s: %s' % (self.Name,s)
        
    # замещаем нужные методы
    def OnLoad(self,parent,P):
        self.obj_mainWin = parent
        self.init_gui()
        self.init_sound(self.obj_mainWin)
        P.AddEventHandler('chat_message', self.PlaySound_Event)
    
    def PlaySound_Event(self,event = None):
        #print "PlaySound_Event: %s" % (event)
        if self.obj_mainWin.Button_SoundSwitch.isChecked():
            self.PlaySound_Test()
    
    def PlaySound_Test(self):
        self.sound_media.setCurrentSource(phonon.Phonon.MediaSource('res/sound/msg_in.wav'))
        self.sound_media.play()
