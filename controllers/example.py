# -*- coding: utf-8 -*-

# This is example controller 
# basic_controller must be included 
#
import basic_controller

# Name of controller is not important for system
# but must be unique across the project 
#
class exampleController(basic_controller.defaultController):

	# Directory for all controllers templates (within /templates dir)
	# If not defined - controller will use /templates
	DIR = './'

	# This dict describes controller's routes
	# 'type' - url prefix dir (note: 'index' = '')
	# 'urls' - paths
	#
	# example:
	#  - http://site/ 			-> self.printDefault(self, data) - default behavior
	# 	- http://site/example 	-> self.printExample(self, data)
	#  - http://site/normal		-> self.printNormal(self, data)
	#
	# All page methods are executing with (self, data) parameters
	# - data dict = {
	#     "fields" - template variables
	#     "levels" - controllers urls (paths) 
	#     "params" - query parameters
	# } 
	#
	
	pages = {
		'type': ['index'],
		'urls': {
			'example': 'printExample',
			'normal': 'printNormal',
		}
	}

	# This dict describes controller's methods
	# all methods are executing with (self, params) parameters
	
	methods = {
		# if there is "time" parameter in query
		# we will execute "getTime" method
		'time': 'getTime',
		
		# if there is "say" parameter in query
		# and it's value == "yes" or "no"
		# we will execute one of these methods
	   'say' : {
			'yes': 'testSayYes',
	      'no' : 'testSayNo'
		},
		
		# if path == normal and there is "test" parameter
		# we will execute "getTestField" method  
		'normal?test': 'getTestField'
	}


	# Methods
	# --------------------------------------------------------------------------------------------------
	# There are controller's methods definition
	# in the section below
	# 
	# Methods can return dict values
	# This values will be append to data['fields'] dict
	# and can be used in page controllers methods and templates
	#

	# Returns current time in 'current_time' field
	# to demonstrate how methods are working 
	def getTime(self, params):
		return {'current_time': time()}

	# Print string to console 
	def testSayYes(self, params):
		print {'said': 'yarrr!'}

	# Print string to console
	def testSayNo(self, params):
		print {'said': 'noooo!'}

	# Redirect user to main page
	def getRedirect(self, params):
		self.redirect('/index')

	# Returns test_field with 'test' value
	def getTestField(self, params):
		return {'test_field': 'test'}

	# Print pages
	# --------------------------------------------------------------------------------------------------

   # This method will be called by default 
   # if controller's route path not exists
   # 
	def printDefault(self, data):  
		
		# Define example variable 'page_name' 
		data['fields'].update({'page_name': 'u -> default'})
		
		# Print template
		return self.printTemplate('test', data)

	# Example
	def printNormal(self, data):
	
		# Raise error with framework error template
		raise NameError
		
		return self.printTemplate('normal', data)

	# Example
	def printExample(self, data):
		return self.printTemplate('example', data)
