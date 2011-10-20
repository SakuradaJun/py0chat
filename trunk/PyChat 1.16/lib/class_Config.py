#-*-coding: utf-8 -*-
'''
Created on 04.03.2011
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

try:
    import sys
    import os
    import yaml
    from lib.utilits import *
except Exception, err:
    print (err)
    sys.exit()

class Config():
    
    settings = {} # Словарь текущих настроек
    setting_file_name = 'settings.yaml'
    paths = {}
    DATA_CAPTCHA = None # Тут будет хранится скачанная капча.

    def_settings = {
        'image_thumb_size':(150,150),
        'admin_pass': None,
        'open_server_tabs': (2,3),
        'autoconnect': True,
        'showpopupmsg': 1,
        'servers':{
                0:{
                    'protocol_type': '0chat',
                    'name':'Test',
                   'token_page': 'http://site.ru/',
                    'host': 'site.ru',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/icon.png'
                },
                
                1:{
                    'protocol_type': '0chat',
                    'name':'0chan.ru',
                    'token_page': 'http://0chan.ru/0chat',
                    'host': '0chan.ru',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/py-chat.tk.ico'
                },
                
                2:{
                    'protocol_type': '0chat',
                    'name': 'py-chat.tk',
                    'token_page': 'http://py-chat.tk',
                    'host': 'py-chat.tk',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/0chan.ru.ico'
                },
                
                3:{
                    'protocol_type': '1chat',
                    'name': '1chan.ru',
                    'token_page': 'http://py-chat.tk',
                    'host': 'py-chat.tk',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/0chan.ru.ico'   
                }
            },
        'style_color': {
            'originalPalette': True,
            'MsgNumColor': '#3366ff',
        },
        'view' : {
            'style':'Plastique',#  Plastique
            'font_text_input': ('Droid Sans',14),
            'font_chat_message': ('Droid Sans',14),
            'font_main_wondow': ('Droid Sans',9),
            'MainWindow_W': 0,
            'MainWindow_H': 0
        },
        'debug': {
            'print_log_in_console':False,
        }
    }
        
    def Save(self,settings = None):
        if not settings:
            settings = self.settings
        if os.path.exists(G['script_dir']+'/'+self.setting_file_name):    
            if self.Load_and_Return() == self.settings: return True
            
        Debug.info('Write config: \'%s\'' % (G['script_dir']+'/'+self.setting_file_name))
        
            
        file_h = open(self.setting_file_name,'w+')
        #file_h = file(self.setting_file_name,'w+')
        yaml.dump(settings, file_h, 
            default_flow_style=None,
            #default_style='\'',
            encoding='utf-8',
            allow_unicode=True,
        ) # explicit_start=True, default_flow_style={None OR False}
        file_h.close()    
        
    def Load_and_Return(self):
        try:
            if not os.path.exists( G['script_dir']+'/'+self.setting_file_name):
                Debug.warr("Произошла ошибка при загрузке конфига %s будут использованны настройки по умолчанию." % (os.path.abspath(os.path.dirname(__file__)+'/'+self.setting_file_name)))
                #self.Save(self.def_settings)
                settings = self.def_settings.copy()
                self.Save(settings)
                return settings
            Debug.info('Read config: \'%s\'' % (os.path.abspath(G['script_dir']+'/'+self.setting_file_name)))
            file_h = open(os.path.abspath(self.setting_file_name),'r')
            #file_h = file(os.path.abspath(self.setting_file_name),'r')
            settings = yaml.load(file_h)
            file_h.close()
            return settings
        except Exception, err:
            Debug.err(err)
            MessageBox(str(err),'Fatal error',type=QtGui.QMessageBox.Warning)
            sys.exit()

    def Load(self):
        #TODO: Если значение параметра нет в загруженном конфиге то брать дефолтное
        self.settings = self.Load_and_Return()
        for def_s in self.def_settings:
            if not def_s in self.settings:
                self.settings[def_s] = self.def_settings[def_s].copy()
                self.Save()


        
