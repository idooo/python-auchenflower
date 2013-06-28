# -*- coding: UTF-8 -*-

"""
	Server runner class
"""

import __init__
import settings

# We need to get and init core settings
# before we start import other modules
core = settings.core()

import cherrypy
import site_builder
from controllers_loader import controllersLoader

class WebApp():

	exposed = True

	# Load all controllers from ./controllers/
	controller = controllersLoader(core)
	pages = set()

	# Set CherryPy static dir root = working dir
	cherrypy.config.update({
		'tools.staticdir.root': core.APP_DIR,
		'tools.encode.encoding': 'utf8'
	})

	@staticmethod
	def welcomeString():
		""" Display pretty formatted loader welcome message """

		welcome_string = '#  ' + core.__appname__ + ', version: ' + str(core.__version__)
		if core.__revision__:
			welcome_string += ', revision: '+ str(core.__revision__)

		delimeter = '# '+('-')*(len(welcome_string)-1)+' #\n'

		if core.DEBUG_MODE:
			welcome_string += '\n#  <<< DEBUG MODE >>>'

		return '\n'+delimeter+welcome_string+'\n'+delimeter

	def __init__(self):
		self.page_runners = {}

		# Create dict() from the list of controllers to make routes search faster
		for module_name in self.controller.controllers:
			for type_name in self.controller.controllers[module_name].pages['type']:
				new_runner = {
					'class': self.controller.controllers[module_name],
				    'urls': self.controller.controllers[module_name].pages['urls'],
				    'name': module_name
				}

				if type_name in self.page_runners:
					self.append = self.page_runners[type_name].append(new_runner)
				else:
					self.page_runners.update({type_name: [new_runner]})

	def __load(self, page, args, params = {}):
		"""
			Searches for controller that can open @page route
			printPage method of this controller will be executed
			with @args and @params
		"""
		for variant in self.page_runners[page]:

			if len(args):
				page_name = args.pop(0)
			else:
				page_name = '__default__'

			return self.controller.controllers[variant['name']].printPage(page_name, args, params)

		# If we didn't find controller for this route
		# we will throw web error
		return builder.throwWebError(params=params)

	def index(self, *args, **kwargs):
		"""
			This method executing by load empty address (route)
			and always bind to 'index' page type
		"""
		return self.__load('index', list(args), kwargs)

	def default(self, page, *args, **kwargs):
		"""
			This is handler for all addresses (routes)
			After execution we will run __load to find
			which of controllers we will use for this page
		"""
		args = list(args)
		if not page in self.page_runners:
			args.insert(0, page)
			page = 'index'

		return self.__load(page, args, kwargs)

	index.exposed = True
	default.exposed = True

if __name__ == '__main__':

	print WebApp.welcomeString()

	builder = site_builder.builder(core)
	cherrypy.quickstart(WebApp(), config=core.conf_name)