# -*- coding: utf-8 -*-

import basic_controller
from time import time

class miscController(basic_controller.defaultController):

	pages = {
		'type': ['u', 'u2'],
		'urls': {
			'error_1': '_/_', # method not defined
			'error_2': 'printTestError2', # template not found
		    'normal': 'printNormal',
		    'model': 'printModelData',
		    'items': 'printDatabase',
		}
	}

	methods = {
		'time': 'getTime',
		'bzz': 'bzzz',
	    'redirect': 'getRedirect',
		'string' : {
			'ya': 'getTestString1',
	        'no': 'getTestString2'
		},

	    'normal?define': 'getDefine',
	    'not_normal?papa': 'appapap',
	    'normal?define2': {
		    'ye': 'yeeeee',
	        'no': 'nope'
	    },
	    'normal?define3': 'getDefine3'

	}


	# --------------------------------------------------------------------------------------------------
	# Methods

	def getTime(self, params):
		return {'current_time': time()}

	def getDefine(self, params):
		return {'test_string': 'da da da'}

	def getTestString1(self, params):
		print {'test_string': 'yaaaarrr!'}

	def getTestString2(self, params):
		print {'test_string': 'nooooorr!'}

	def getRedirect(self, params):
		self.redirect('/index')

	# --------------------------------------------------------------------------------------------------
	# Print pages

	def printTestError2(self, data):
		return self.printTemplate('______', data)

	def printRedirect(self, data):
		return self.printTemplate('______', data)

	def printDefault(self, data):
		data['fields'].update({'page_name': 'u -> default'})
		return self.printTemplate('test', data)

	def printNormal(self, data):
		data['fields'].update({'page_name': 'u -> normal'})
		return self.printTemplate('test', data)

	def printModelData(self, data):
		data['fields'].update({'page_name': self.core.model['test']['People'].getPeople()})
		return self.printTemplate('test', data)

	def printDatabase(self, data):
		data['fields'].update({'page_name': self.core.model['test']['Items'].getItems()})
		return self.printTemplate('test', data)