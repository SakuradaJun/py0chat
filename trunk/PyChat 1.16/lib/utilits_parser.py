#-*-coding: utf-8 -*-
'''
Created on 07.03.2011
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


import re
from lib.utilits import *

def Parser_IN(Text):  
    #[18:12:06] <b>&lt;<a href="event:insert,2670133"><font color="#000000">2670133</font></a></b><b>&gt;</b> Грустное кино.<br />
    #Text = Text.replace('<font color="red">', '<font color="#ff0000">')
    #Text = Text.replace('то что ищем', 'то на что заменяем')
    #<a href="#" onClick="javascript:goToMark(28792); return false;">28792</a>
    Text = re.sub("<font color=\"#000000\">(\d{1,})</font>", 
                  "<a href=\"event:block_user,\\1\">B</a>  <span class=\"msgNum\">\\1</span>", Text)
    #Text = re.sub("<font color=\"#000000\">(\d{1,})</font>", "<a href=\"event:block_user,\\1\">B</a>  <span class=\"msgNum\">\\1</span>", Text)
    
    
    #Text = Text.replace('<font color="#000000">', '<font color="'+self.conf_o.settings['style_color']['MsgNumColor']+'">')
    #Text = Text.replace('<span class="reply">', '<span style="color:#ff6600;">')
    Text = Text.replace('<span class="reply_for_me">', '<span class="reply_for_me" style="color:#FF3333;">')
    Text = re.sub('<span class="reply">&gt;&gt;(\d{1,})</span>','<a class="reply" href="" onClick="javascript:goToMark(\\1); return false;">&gt;&gt;\\1</a>',Text)
    return Text

def ParsePost(post_message):
    #[20:39:39] <b>&lt;<a href="event:insert,28792"><font color="#000000">28792</font></a></b><b>&gt;</b> TEst
    #re.I|re.U 
    try:
        post_message = post_message.strip()
    except Exception,err:
        Debug.err('Parse err: '+str(err))
        return post_message
    #f = open('msg_dumb.dat','ab+');f.write(data);f.close()
    #parent = '.*\[(?P<time>[\d:]*)\] <b>&lt;<a href="event:insert,(?P<post_num>\d+)"><font color="#000000">\d+</font></a></b><b>&gt;</b>(?P<message>.*)(\n|\r\n|<br/>|<br />|)'
    post_message_s = post_message.split('<br />')
    if type(post_message_s) == list and len(post_message_s) > 1:
        return post_message
    del post_message_s
    
    parent = '.*\[(?P<time>[\d:]*)\] <b>&lt;<a href="event:insert,(?P<post_num>\d+)"><font color="#[a-f0-9]+">\d+</font></a></b><b>&gt;</b>(?P<message>.*)(<br />|.*)'
    #parent = '.*\[(?P<time>[\d:]*)\] <b>&lt;<a href="event:insert,(?P<post_num>\d+)"><font color="#000000">\d+</font></a></b><b>&gt;</b>(?P<message>.*)(<br />|\r\n|\n|.*)'
    #'[22:02:11] <b>&lt;<a href="event:insert,2677309"><font color="#000000">2677309</font></a></b><b>&gt;</b> &lt;<i><b>Angrybot</b></i>&gt; От нас ушла одна няша — помашем вслед платочком!'
    result = re.match(parent,post_message)#re.U 
    if result:
            #print result.groups()
            #print u"[%s] <%s> %s\n" % (result.group('time'),result.group('post_num'),result.group('message'))
            dic = {
                u'time':result.group(u'time'),
                u'post_num':result.group(u'post_num'),
                u'message':result.group(u'message')
            }
            time = result.group(u'time')
            post_num = result.group(u'post_num')
            message = result.group('message')
            return (time,post_num,message)
            try:
                t = '<a href="event:insert,%s" class="msgNum">%s</a>&nbsp;<span class="post_time">%s</span><br /> %s<br />\n' % (post_num,post_num,time,message)
            except Exception,err:
                Debug.err("# %s" % (str(err)))
                return post_message
            return t
    else:
        #print u"Not Found: %s\n" % (post_message)
        Debug.debug('Parser: not found',Debug.RED)
        return post_message
        #print post_message
        #[21:36:00] <b>&lt;<a href="event:insert,2677196"><span class="msgNum">2677196</span></a></b><b>&gt;</b> d
        post_message.replace('\r\n','<br />')
        post_message.replace('\n','<br />')
        
        post_message = post_message.strip("<br />")
        return post_message
