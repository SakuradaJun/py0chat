#-*-coding: utf-8 -*-
'''
Created on 05.03.2011

@author: anon
'''

import os
import sys
from lib.utilits import *
# Экземпляры загруженных плагинов
Plugins = []

# Базовый класс плагина
class Plugin(object):
	Name = 'undefined'
	Version = '1.0'
	Window_Main = None
	
	# Методы обратной связи
	def OnLoad(self,Window_Main,P):
		pass

	def OnCommand(self, cmd, args):
		pass

class PluginHandler(object):
	events = {}
	def __init__(self):
		ev = {'test':[self.Event]}
	
	def AddEventHandler(self, EventName, EventFunction):
		#Debug.info(' Add Event Hendler: %s - call %s ' % (EventName, EventFunction))
		if EventName in self.events:
			self.events[EventName].append(EventFunction)
		else:
			self.events[EventName] = [EventFunction,]
		
	def Event(self, event, argv, *args):
		if event in self.events:
			#print 'Event: %s **args: %s ' % (event,args)
			for func in self.events[event]:
				#print 'Call: %s' % (func)
				func(argv)
		else:
			#Debug.err('Нет события для %s' % (event))
			pass

	def LoadPlugins(self,Window_Main):
		from lib.plugin_kernel import KernelPlugin
		plugins_dir = './plugins'
		try:
			ss = os.listdir(plugins_dir) # Получаем список плагинов в /plugins
			sys.path.insert( 0, plugins_dir) # Добавляем папку плагинов в $PATH, чтобы __import__ мог их загрузить
		except Exception,err:
			Debug.err(err)
			Debug.info('Create dir "%s"' % (plugins_dir))
			os.mkdir(plugins_dir)
	
		
		for s in ss:
			if s[-3:] != '.py': continue
			Debug.info('Found plugin: %s' % (s))
			__import__(os.path.splitext(s)[ 0], None, None, ['']) # Импортируем исходник плагина
			
		#p = KernelPlugin()
		#print Plugin.__subclasses__()
		for plugin in Plugin.__subclasses__(): # так как Plugin произведен от object, мы используем __subclasses__, чтобы найти все плагины, произведенные от этого класса
			p = plugin() # Создаем экземпляр
			Plugins.append(p)
			Debug.info('Load Plugin: %s v%s' % (p.Name, p.Version))
			p.OnLoad(Window_Main,self) # Вызываем событие загруки этого плагина
	
		return

def Plugin_CMD(argv):
		for p in Plugins:
			p.OnCommand(argv)
