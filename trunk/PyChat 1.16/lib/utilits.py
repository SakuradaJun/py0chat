# -*- encoding: utf-8 -*-
'''
Created on 03.03.2011

@author: anon
'''
from PyQt4.QtCore import QString
from sys import platform
from PyQt4 import QtGui
import re
reCompile_ImagesThumd_F = re.compile('(<a href="(http://.*(\.png|\.jpg|\.jpeg|\.gif))".*>.*</a>)')
reCompile_ImagesRGHostRe_F = re.compile('(http\:\/\/rghost\.ru\/(\d+)\.view)')
#reCompile_ImagesRGHostRe_R = re.compile('http:\/\/rghost\.ru\/\\1\.\\2')
#result = re.search(reCompile_ImagesRGHostRe_F,u'gfdgfd gfd dfg http://rghost.ru/4698495.view')
#if result:
#    print result.groups()
#sys.exit()

def AddImagesThumb(Text,size=(150,150)):
    #TODO: При клике на изображение разворачивать полную версию.
    Text = re.sub(reCompile_ImagesRGHostRe_F,'http://rghost.ru/\\2.png', Text)
    
    Text = re.sub(reCompile_ImagesThumd_F, 
                  '<p>Thumb: <a href="\\2" title="\\2" alt="\\2" class="image_thumb_re">\\2<br /><img src="http://imageflyresize.appspot.com/?q=\\2&width='+str(size[0])+'&height='+str(size[1])+'"/></a></p>', 
                  Text)
    return Text

class MessageBox(QtGui.QMessageBox):
    
    def __init__(self,text = "Message Here",title = u'Сообщение:',type = QtGui.QMessageBox.NoIcon):
        super(QtGui.QMessageBox, self).__init__(None)
        text = QString.fromUtf8(str(text))
        title = QString.fromUtf8(str(title))
        self.setText(text)
        #self.setIcon(QtGui.QMessageBox.Information); 
        self.setIcon(type); 
        self.setWindowTitle(title)
        #self.setIcon(None)
        self.exec_()
        
def qStringToStr(s):
    try:
        if False: s = QString()
        #s = unicode(s) #.encode('utf-8')
        #s = str(s.toUtf8()).decode('utf-8')
        s = str(s.toUtf8()).decode('utf-8')
    except Exception,err:
        Debug.err('Decode: '+str(err))
        
    #s = str(QApplication.translate("MainWindow", s, None, QApplication.UnicodeUTF8))
    
    return s
    
def ReadFile(file):
    f = open(file)
    data = f.read()
    f.close()
    return data
        
class Debug_class():
    
    '''
    HEADER = '\033[95m' 
    OKBLUE = '\033[94m' 
    OKGREEN = '\033[92m' 
    WARNING = '\033[93m' 
    FAIL = '\033[91m' 
    ENDC = '\033[0m' 
    '''  

    def err(self,s, n = True):
        if platform != 'win32':
            m = '\033[91m# [Error]: %s\033[0m' % (str(s)) 
        else:
            m = '# [Error]: %s' % (str(s)) 
        if n: 
            print m 
        else: 
                print m,    
            
    def warr(self,s, n = True): 
        m = '# [Warring]: %s' % (str(s))
        if n: 
            print m
        else: 
            print m, 
            
    def info(self,s, n = True):
        m = '# [Info]: %s' % (str(s))
        if n: 
            print m
        else: 
            print m,
Debug = Debug_class()
