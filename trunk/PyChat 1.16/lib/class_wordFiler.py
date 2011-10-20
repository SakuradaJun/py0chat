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


from lib.utilits import *

class WordFiler_DotNET:
    file_wordfiler = 'blacklist_neko.txt'
    filter_in = []
    filter_in_markcolor = '#DF4AA9'
    
    '''
     public struct Blacklist
    {
        public string Blackword;
        public bool IgnorePost;
        public bool ReplaceBlackword;
        public string ReplaceWord;
    }
    Что ищем: ##ADMIN## 
    Блокировать?: False
    Заменять?: True
    На: няша
    '''
    def __init__(self):
        self.load()
    
    @timeit
    def load(self):
        file_h = open(self.file_wordfiler,'r')
        bl_size = int(file_h.readline())
        Debug.debug('WordFiler: count %s' % (bl_size))
        def ToBool(s):
            if s == 'False':
                return False
            if s == 'True':
                return True
            return s
        
        for i in range(0,bl_size):
            element = []
            
            Blackword = file_h.readline().replace('\r\n','').replace('\n','')
            IgnorePost = file_h.readline().replace('\r\n','')
            ReplaceBlackword = file_h.readline().replace('\r\n','')
            ReplaceWord = file_h.readline().replace('\r\n','').replace('\n','')
            if not Blackword.replace('\t','').replace('\n',''): continue
            #print 'Find: %s isBlock %s isReplace %s in: %s\n' % (Blackword, IgnorePost, ReplaceBlackword, ReplaceWord )

            element.append(Blackword)
            element.append(ToBool(IgnorePost))
            element.append(ToBool(ReplaceBlackword))
            element.append(ReplaceWord)
            self.filter_in.append(element)
        Debug.debug('WordFiler: loaded %s words' % (self.filter_in.__len__()))
        file_h.close()
        return
        for item in self.filter_in:
            print (item)
            #['\xd0\x8e', True, False, '']

    @timeit  
    def FilterMessage(self,src,filter_dic=None):
        if filter_dic == None: filter_dic = self.filter_in
        
        src_lower = src.encode('utf-8').lower()
        #src_lower = unicode(src, 'utf-8').lower().encode('utf-8')
        
        for item in filter_dic:
            Blackword = item[0]
            Blackword_lower = Blackword.encode('utf-8').lower()
            #Blackword_lower = unicode(Blackword, 'utf-8').lower().encode('utf-8')
            IgnorePost = item[1]
            ReplaceBlackword = item[2]
            ReplaceWord =  item[3]
            #print Blackword_lower, src_lower
            ggg = 'ху %s' % (Blackword_lower)
            ggg = 'ху %s' % (src_lower)
            
            if src_lower.count(Blackword_lower):
                if IgnorePost and ReplaceBlackword:
                        return ReplaceWord
                else:
                    if IgnorePost:
                        return ''
                    else:
                        print ('Find: %s Replace: %s' % (item[0],item[3]))
                        #print "REPLACE"
                        #par_find = re.compile(Blackword, re.I|re.U)
                        #print 're.sub(\'%s\',\'%s\',\'%s\')' % (Blackword, ReplaceWord ,src)
                        #src = re.sub('('+Blackword+')', ReplaceWord ,src,re.I|re.U)
                        if self.filter_in_markcolor:
                            ReplaceWord = '<font color="%s">%s</font>' % (self.filter_in_markcolor,ReplaceWord)
                            
                        src = re.sub(Blackword.replace('?','\?')
                                     .replace('^','\^')
                                     .replace('*','\*')
                                     .replace('.','\.')
                                     .replace('(','\(')
                                     .replace(')','\)')
                                     .replace('$','\$')
                                     .replace('+','\+'),
                                     ReplaceWord,
                                     src,
                                     re.I|re.U
                                     )
                         
                        '''
                        src = Regex.Replace(src, 
                                bl[i].Blackword.Replace(@"\", @"\\")
                                .Replace(".", @"\.")
                                .Replace("^", @"\^")
                                .Replace("?",@"\?")
                                .Replace("*",@"\*")
                                .Replace("$",@"\$")
                                .Replace("+",@"\+")
                                .Replace("(",@"\(")
                                .Replace(")",@"\)"), 
                                bl[i].ReplaceWord, RegexOptions.IgnoreCase);
                        '''
                        return src
        return src
                    
        
WordFilter = WordFiler_DotNET()