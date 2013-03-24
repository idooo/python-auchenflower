# -*- coding: utf-8 -*-

import basic

class miscController(basic.defaultController):

	pages = {
				'type': ['index'],
				'urls': {
					'test1': 'printTest1',
				}
			}

	# --------------------------------------------------------------------------------------------------
	# Print pages

	def printDefault(self, data):
		data['fields'].update({'page_name': 'index'})
		return basic.defaultController.printTemplate(self, 'test', data)

	def printTest1(self, data):
		data['fields'].update({'page_name': 'misc -> test1'})
		return basic.defaultController.printTemplate(self, 'test1', data)
