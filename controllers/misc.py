# -*- coding: utf-8 -*-

import basic

class miscController(basic.defaultController):

	pages = {
				'type': ['index'],
				'urls': {
					'index': 'printIndex',
					'test1': 'printTest1',
				}
			}


	# --------------------------------------------------------------------------------------------------
	# Print pages

	def printDefault(self, data):
		data['fields'].update({'test': 1})
		return basic.defaultController.printTemplate(self, 'index', data)

	def printTest1(self, data):
		data['fields'].update({'test': 2})
		return basic.defaultController.printTemplate(self, 'test1', data)
