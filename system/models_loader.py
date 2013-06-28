#!/usr/bin/python
# -*- coding: utf-8 -*-

import __init__
import __main__
import os, inspect, sys

class ModelObject(dict):

	def __getattr__(self, name):
		try:
			return self[name]
		except KeyError as e:
			raise AttributeError(e)

	def __setattr__(self, name, value):
		self[name] = value


class DataModel():

	@staticmethod
	def loadGlobalModel(core):

		models_folder = core.APP_DIR + core.MODELS_DIR

		modules = {}
		for item in os.listdir(models_folder):
			if item[-2:] == 'py':
				modules.update({item[:-3:]:__import__(item[:-3:])})

		global_model = ModelObject()

		for module_name in modules:
			clear_module_name = module_name.replace('model_', '').capitalize()

			for name, class_name in inspect.getmembers(sys.modules[module_name]):
				if inspect.isclass(class_name):
					if not clear_module_name in global_model:
						setattr(global_model, clear_module_name, ModelObject())

					setattr(getattr(global_model, clear_module_name), name, class_name(core))

		return global_model



