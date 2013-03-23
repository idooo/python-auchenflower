# -*- coding: utf-8 -*-

import basic

class miscController(basic.defaultController):

	pages = {
		'index':    'printIndex',
		'':         'printIndex'
	}


	# --------------------------------------------------------------------------------------------------
	# Print pages

	def printIndex(self, data):
		data['fields'].update({'test': 1})
		return basic.defaultController.printTemplate(self, 'index', data)


data = {
	'class': miscController,
    'type': ['index', 'default'],
	'urls': ['', 'index']
}
