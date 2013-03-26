#!/usr/bin/python
# -*- coding: utf-8 -*-

import __init__
import __main__
import os, inspect, sys

class DataModel():

	@staticmethod
	def loadGlobalModel(core):

		MODELS_DIR = '/models'

		models_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])+'/..'+MODELS_DIR

		modules = {}
		for item in os.listdir(models_folder):
			if item[-2:] == 'py':
				modules.update({item[:-3:]:__import__(item[:-3:])})

		global_model = {}

		for module_name in modules:
			clear_module_name = module_name.replace('model_', '')

			for name, class_name in inspect.getmembers(sys.modules[module_name]):
				if inspect.isclass(class_name):
					if not clear_module_name in global_model:
						global_model.update({clear_module_name: {}})

					global_model[clear_module_name].update({name: class_name(core)})

		return global_model



