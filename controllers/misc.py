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
		return self.printTemplate('test', data)

	def printTest1(self, data):
		data['fields'].update({'page_name': 'misc -> test1'})
		return self.printTemplate('test1', data)
