# -*- coding: UTF-8 -*-

import __init__
import os, inspect, sys

class controllersLoader():

	def __init__(self, core):
		self.core = core
		self.__loadModules()

	def __loadModules(self):
		modules_folder = self.core.APP_DIR + self.core.CONTROLLERS_DIR

		self.controllers = {}
		self.modules = {}

		for item in os.listdir(modules_folder):
			if item[-2:] == 'py':
				self.modules.update({item[:-3:]:__import__(item[:-3:])})

		for module_name in self.modules:
			try:
				for name, class_name in inspect.getmembers(sys.modules[module_name]):
					if inspect.isclass(class_name):
						controller = class_name()
						if controller.pages['type'] != controller.pages['urls']:
							pass

						# Conditional methods
						if hasattr(controller, 'methods'):
							deleted_methods = []
							conditional_methods = {}

							for method_name in controller.methods:
								tmp = method_name.split('?')
								if len(tmp) > 1:
									if not tmp[0] in conditional_methods:
										conditional_methods.update({tmp[0]: {}})

									conditional_methods[tmp[0]].update({tmp[1]: controller.methods[method_name]})
									deleted_methods.append(method_name)

							controller.conditional_methods = conditional_methods

							for method_name in deleted_methods:
								del controller.methods[method_name]

						self.controllers.update({module_name: controller})

			except Exception:
				print 'WARNING:', module_name, 'module loading FAIL!'



