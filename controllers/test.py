# -*- coding: utf-8 -*-

import basic

class miscController(basic.defaultController):

	pages = {
		'type': ['u', 'u2'],
		'urls': {
			'error_1': '_/_', # method not defined
			'error_2': 'printTestError2', # template not found
		    # 'error_3: '--' # page rule not found
		    'normal': 'printNormal'
		}
	}

	# --------------------------------------------------------------------------------------------------
	# Print pages

	def printTestError2(self, data):
		return basic.defaultController.printTemplate(self, '______', data)

	def printDefault(self, data):
		data['fields'].update({'page_name': 'u -> default'})
		return basic.defaultController.printTemplate(self, 'test', data)

	def printNormal(self, data):

		for item_name in data:
			print item_name,' > ', data[item_name]

		data['fields'].update({'page_name': 'u -> normal'})
		return basic.defaultController.printTemplate(self, 'test', data)
