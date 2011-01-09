#!/usr/bin/python
#-*-coding: utf-8 -*-
'''
Created on 07.01.2011
@author: anon
'''

import re

def ParsePost(post_message):
    #re.I|re.U 
    post_message = post_message.strip()
    #f = open('msg_dumb.dat','ab+');f.write(data);f.close()
    parent = '.*\[(?P<time>[\d:]*)\] <b>&lt;<a href="event:insert,(?P<post_num>\d+)"><font color="#000000">\d+</font></a></b><b>&gt;</b>(?P<message>.*)(<br />|.*)'
    #'[22:02:11] <b>&lt;<a href="event:insert,2677309"><font color="#000000">2677309</font></a></b><b>&gt;</b> &lt;<i><b>Angrybot</b></i>&gt; От нас ушла одна няша — помашем вслед платочком!'
    result = re.match(parent,post_message)#re.U 
    if result:
            print result.groups()
            #print u"[%s] <%s> %s\n" % (result.group('time'),result.group('post_num'),result.group('message'))
            dic = {
                u'time':result.group(u'time'),
                u'post_num':result.group(u'post_num'),
                u'message':result.group(u'message')
            }
            time = result.group(u'time')
            post_num = result.group(u'post_num')
            message = result.group('message')
            try:
                t = '<a href="event:insert,%s" class="msgNum">%s</a>&nbsp;<span class="post_time">%s</span><br /> %s<br />\n' % (post_num,post_num,time,message)
            except Exception,err:
               print "# %s" % (str(err))
               return post_message
            return t
    else:
        #print u"Not Found: %s\n" % (post_message)
        print post_message
        #[21:36:00] <b>&lt;<a href="event:insert,2677196"><span class="msgNum">2677196</span></a></b><b>&gt;</b> d
        return post_message
