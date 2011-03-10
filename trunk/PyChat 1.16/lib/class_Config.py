#-*-coding: utf-8 -*-
'''
Created on 04.03.2011

@author: anon
'''
try:
    import sys
    import os
    import yaml
    from lib.utilits import *
except Exception,err:
    print err
    sys.exit()

class Config():
    
    settings = {} # Словарь текущих настроек
    setting_file_name = 'settings.yaml'
    DATA_CAPTCHA = None # Тут будет хранится скачанная капча.

    def_settings = {
        'image_thumb_size':(150,150),
        'admin_pass': None,
        'open_server_tabs': (2,3),
        'autoconnect': True,
        'servers':(
                {
                    'name':'Test',
                   'token_page': 'http://site.ru/',
                    'host': 'site.ru',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/icon.png'
                },
                
                {
                    'name':'0chan.ru',
                    'token_page': 'http://0chan.ru/0chat',
                    'host': '0chan.ru',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/py-chat.tk.ico'
                },
                
                {
                    'name': 'py-chat.tk',
                    'token_page': 'http://py-chat.tk',
                    'host': 'py-chat.tk',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/0chan.ru.ico'
                }
            ),
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

    def __init__(self):
        pass
        
    def Save(self,force_settings = None):
        if force_settings:
            settings = force_settings
        else:
            settings = self.settings
            if self.Load_and_Return() == self.settings: return True
        #if 'current_server' in self.set_by_argv:
        #    self.settings['current_server'] = self.set_on_load['current_server']
            
        

        
        file_h = file(self.setting_file_name,'w+')
        yaml.dump(settings, file_h, 
            default_flow_style=None,
            #default_style='\'',
            encoding='utf-8',
            allow_unicode=True,
        ) # explicit_start=True, default_flow_style={None OR False}
        file_h.close()    
        
    def Load_and_Return(self):
        try:
            if not os.path.exists(os.path.abspath(self.paths['config_dir']+'/'+self.setting_file_name)):
                Debug.warr("Произошла ошибка при загрузке конфига %s будут использованны настройки по умолчанию." % (os.path.abspath(self.paths['config_dir']+'/'+self.setting_file_name)))
                self.Save(self.def_settings)
                self.settings = self.def_settings.copy()
                return self.settings
            Debug.info('Read config: \'%s\'' % (os.path.abspath(self.paths['config_dir']+'/'+self.setting_file_name)))
            file_h = file(os.path.abspath(self.setting_file_name),'r')
            settings = yaml.load(file_h)
            file_h.close()
            return settings
        except Exception,err:
            MessageBox(err,'Fatal error',type=QtGui.QMessageBox.Warning)
            sys.exit()

    def Load(self):
        #TODO: Если значение параметра нет в загруженном конфиге то брать дефолтное
        self.settings = self.Load_and_Return()
        for def_s in self.def_settings:
            if not def_s in self.settings:
                self.settings[def_s] = self.def_settings[def_s].copy()
                self.Save()
        return

        if len(sys.argv) == 3:
            self.settings['current_server'] = sys.argv[2]
            self.set_by_argv.append('current_server')
            
    def set_def_settings(self): self.settings = self.def_settings


        
