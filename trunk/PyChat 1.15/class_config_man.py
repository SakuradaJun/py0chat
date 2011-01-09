#!/usr/bin/python
#-*-coding: utf-8 -*-
import  yaml, sys

class Config:
	
	settings = {}
	setting_file_name = 'settings.yaml'
	DATA_CAPTCHA = None # Тут будет хранится скачанная капча.
	def_settings = {
		'user_nick': '**<аноним> **', 
		'admin_pass': None,
		'current_server': 'py-chat',
		'autoconnect': True,
		'NamefagMode': False,
		'servers': {
			'0chan': {
				'token_page': 'http://0chan.ru/0chat',
				'host': '0chan.ru',
				'port': 1984
			},
			'py-chat': {
				'token_page': 'http://py-chat.tk',
				'host': 'py-chat.tk',
				'port': 1984
			}
		},
		'style_color': {
			'style':'Plastique', #  Plastique
			'originalPalette': True,
			'MsgNumColor': '#3366ff',
			'font_text_input': ('Droid Sans',14),
			'font_chat_message': ('Droid Sans',14),
			'font_main_wondow': ('Droid Sans',9)
		},
		'view' : {
			'MainWindow_W': 0,
			'MainWindow_H': 0
		},
		'debug': {
			'print_log_in_console':False
		}
	}
	def __init__(self):
		pass
		
	def Save(self):
		if self.Load_and_Return() == self.settings:
			return True
		
		file_h = file(self.setting_file_name,'w+')
		yaml.dump(self.settings, file_h, 
			default_flow_style=None,
			#default_style='\'',
			encoding='utf-8',
			allow_unicode=True,
		) # explicit_start=True, default_flow_style={None OR False}
		file_h.close()	
		
	def Load_and_Return(self):
		file_h = file(self.setting_file_name,'r')
		settings = yaml.load(file_h)
		file_h.close()
		return settings
		
			
	def Load(self):
		try:
			self.settings = self.Load_and_Return()
		except :
			print "# Error: произошла ошибка при загрузке конфига %s будут использованны настройки по умолчанию." % (self.setting_file_name)
			self.set_def_settings()
			self.Save()
			#print "Error in configuration file: "+self.setting_file_name
			#exit()
			#MSG_error_o = MSG_error()
		if len(sys.argv) == 3:
			self.settings['current_server'] = sys.argv[2]
			
	def set_def_settings(self):
		self.settings = self.def_settings

