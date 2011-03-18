#-*-coding: utf-8 -*-
'''
Created on 03.03.2011
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

from sys import platform
import re, os, time
from PyQt4 import QtCore,QtGui

reCompile_ImagesThumd_F = re.compile('(<a href="(http://.*(\.png|\.jpg|\.jpeg|\.gif))".*>.*</a>)')
reCompile_ImagesRGHostRe_F = re.compile('(http\:\/\/rghost\.ru\/(\d+)\.view)')
#reCompile_ImagesRGHostRe_R = re.compile('http:\/\/rghost\.ru\/\\1\.\\2')
#result = re.search(reCompile_ImagesRGHostRe_F,u'gfdgfd gfd dfg http://rghost.ru/4698495.view')
#if result:
#    print result.groups()
#sys.exit()
def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        #print '%r (%r, %r) %2.2f sec' % \
        #      (method.__name__, args, kw, te-ts)
        print '%r %2.2f sec ' % \
             (method.__name__,te-ts)
        return result

    return timed

class class_WebKitStyle():
    
    setyleDirPath = os.path.abspath('res/style/webkitstyle')+'/'
    TemplateFilePath = 'Template.html'
    '''
    font_chat_message: !!python/tuple [sans, 14]
    font_main_wondow: !!python/tuple [Droid Sans, 9]
    font_text_input: !!python/tuple [Droid Sans, 14]
    '''
    #variantPath = 'Variants/Medium.css'
    #variantPath = 'Variants/Small.css'
    #variantFilePath = 'Variants/Big.css'
    variantFilePath = 'Variants/Custom_font.css'
    
    baseStyleFilePath = 'base.css'
    mainCommon_FilePath = '../main_common.css'
    
    def getAppStyle(self,file='res/style/style/qutim.qss'):
        path_to_style = QtCore.QUrl().fromLocalFile(QtCore.QString(os.path.abspath(file))).toString()
        data_style = ReadFile(file).replace('%path%',path_to_style)
        return data_style
        
        
    def Build(self):
        templateHtml = ReadFile(self.setyleDirPath + self.TemplateFilePath)
        Data_BaseStyle = ReadFile(self.setyleDirPath + self.mainCommon_FilePath)
        Data_BaseStyle += ReadFile(self.setyleDirPath + self.baseStyleFilePath)
        
        BaseHref = self.getStyleBaseHref()
        templateHtml = templateHtml.replace('%@',BaseHref,1)
        templateHtml = templateHtml.replace('%@',Data_BaseStyle,1)
        templateHtml = templateHtml.replace('%@',self.variantFilePath,1)
        
        templateHtml = templateHtml.replace('%@','')
        #print templateHtml
        return templateHtml

    def getStyleBaseHref(self):
        return QtCore.QUrl().fromLocalFile(QtCore.QString(self.setyleDirPath + self.TemplateFilePath)).toString()
    
        
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
        text = QtCore.QString.fromUtf8(str(text))
        title = QtCore.QString.fromUtf8(str(title))
        self.setText(text)
        #self.setIcon(QtGui.QMessageBox.Information); 
        self.setIcon(type); 
        self.setWindowTitle(title)
        #self.setIcon(None)
        self.exec_()
        
def qStringToStr(s):
    try:
        if False: s = QtCore.QString()
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
    HEAD = '\033[95m'
    END = '\033[0m'
    RED = '\033[91m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'

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
        m = '# [Warring]: ' + str(s)
        if n: 
            print m
        else: 
            print m, 
            
    def info(self,s, n = True):
        m = '# [Info]: ' + str(s)
        if n: 
            print m
        else: 
            print m,
            
    def debug(self,s,color=None):
        s = '# [Debug]: %s' % (s)
        if platform == 'win32' or color == None: 
            print s
        else:
            print color+s+self.END

Debug = Debug_class()
WebKitStyle = class_WebKitStyle()
