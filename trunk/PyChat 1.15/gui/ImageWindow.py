#-*-coding: utf-8 -*-
from PyQt4 import QtCore, QtGui,QtNetwork

class ImageWindow_d(QtGui.QWidget):

    def __init__(self,Url):
        super(QtGui.QWidget, self).__init__(None)
        self.setWindowTitle(Url)
        self.setObjectName("MainWindow")
        self.resize(902, 520)
        self.Url = Url
       
        self.label_captcha = QtGui.QLabel(self)
        self.label_captcha.setText('Loading...')
        self.label_captcha.resize(200 , 300 )
        self.Progress = QtGui.QProgressBar(self)
        self.Progress.show()
        self.setWindowIconText('TEST!&')
        self.show() 
        self.Conn()
    
    def Conn(self):
        #print "Connect %s" % (self.Url)
        self.http = QtNetwork.QHttp(self)
        self.SetSocketSIGNALS()
        url = QtCore.QUrl(self.Url)
        fileInfo = QtCore.QFileInfo(url.path())
        #print fileInfo.fileName()
        
        self.http.setHost(url.host(), QtNetwork.QHttp.ConnectionModeHttp, 0)
        if url.userName():
            self.http.setUser(url.userName(), url.password())
            
        self.httpRequestAborted = False
        self.outFile = QtCore.QFile(fileInfo.fileName())
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, "HTTP",
                    "Unable to save the file %s: %s." % (fileInfo.fileName(), self.outFile.errorString()))
            self.outFile = None
            return
        path = str(QtCore.QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/"))
        self.Buffer = QtCore.QBuffer()
        self.Buffer.open(QtCore.QIODevice.ReadWrite)
        self.DATA = self.http.get(path, to=self.Buffer)#self.outFile

    ### SIGNALS
    def SetSocketSIGNALS(self):
        self.http.requestFinished.connect(self.httpRequestFinished)
        self.http.dataReadProgress.connect(self.updateDataReadProgress)
        self.http.responseHeaderReceived.connect(self.readResponseHeader)
        self.http.authenticationRequired.connect(self.slotAuthenticationRequired)
        
    def httpRequestFinished(self,*a):
        if self.Buffer.size() < 1: return 
        print self.Buffer.size()
        #self.QBuffer.size())
        #f = open('img.jpg','ab+');f.write(str(String));f.close()
        
        #from urllib2 import urlopen
        #self.image.loadFromData(urlopen(self.Url).read())
        self.image = QtGui.QPixmap()
        self.image.loadFromData(self.Buffer.data())
        self.label_captcha.setPixmap(self.image)
        
        
        self.label_captcha.resize(self.image.width(), self.image.height())
        self.resize(self.image.width()+20, self.image.height()+20)    
        
    def updateDataReadProgress(self, bytesRead, totalBytes):
        #print "Read: %s %s" % (bytesRead, totalBytes)
        self.Progress.setMaximum(totalBytes)
        self.Progress.setValue(bytesRead)
        
    def readResponseHeader(self, responseHeader):
        print 'statusCode: %s' % (responseHeader.statusCode())
        return
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            QtGui.QMessageBox.information(self, "HTTP",
                    "Download failed: %s." % responseHeader.reasonPhrase())
            self.httpRequestAborted = True
            self.progressDialog.hide()
            self.http.abort()
        
    def slotAuthenticationRequired(self, *a):

        print a
        
    def closeEvent(self,event):
        self.app.quit()
        