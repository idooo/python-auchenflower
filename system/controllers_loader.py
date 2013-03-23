# -*- coding: UTF-8 -*-

import __init__
import os, inspect, sys

class controllersLoader():

	def __init__(self):
		self.__loadModules()
		self.__getAlias()

	def __loadModules(self):
		modules_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])+'/../controllers'

		self.modules = {}
		for item in os.listdir(modules_folder):
			if item[-2:] == 'py' and item[:-3:] != 'basic':
				self.modules.update({item[:-3:]:__import__(item[:-3:])})

	def __getAlias(self):
		self.controllers = {}

		for item in self.modules:
			try:
				for name, class_name in inspect.getmembers(sys.modules[item]):
					if inspect.isclass(class_name):
						controller = class_name()
						if controller.pages['type'] != controller.pages['urls']:
							pass

						self.controllers.update({item: controller})

			except Exception:
				print 'WARNING:', item, 'module loading FAIL!'



