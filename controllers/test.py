# -*- coding: utf-8 -*-

import basic

class miscController(basic.defaultController):

	pages = {
		'type': ['u'],
		'urls': {
			'test2': 'printTest1'
		}
	}

	# --------------------------------------------------------------------------------------------------
	# Print pages

	def printTest1(self, data):
		data['fields'].update({'test': 2})
		return basic.defaultController.printTemplate(self, 'test2', data)

	def printDefault(self, data):
		data['fields'].update({'test': 3})
		return basic.defaultController.printTemplate(self, 'test2_def', data)
