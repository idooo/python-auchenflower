# -*- coding: UTF-8 -*-

import __init__
import inspect
import settings

core = settings.core()

import cherrypy
import site_builder
from sets import Set
from controllers_loader import controllersLoader

class WebApp():

	exposed = True

	controller = controllersLoader()
	pages = Set()

	def __init__(self):
		self.page_runners = {}

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

		for thing in self.page_runners:
			print thing, self.page_runners[thing]

	def __load(self, page, args, params = {}):

		for variant in self.page_runners[page]:

			if len(args):
				page_name = args.pop(0)
			else:
				page_name = '__default__'

			return self.controller.controllers[variant['name']].printPage(page_name, args, params)

		return builder.throwWebError(params=params)

	def index(self, *args, **kwargs):
		return self.__load('index', {})

	def default(self, page, *args, **kwargs):
		args = list(args)
		if not page in self.page_runners:
			args.insert(0, page)
			page = 'index'

		return self.__load(page, args, {})

	index.exposed = True
	default.exposed = True

if __name__ == '__main__':

	print '# ------------------------------------------------------------- #'
	print '#  ', core.__appname__,'version:', core.__version__, 'revision:', core.__revision__
	print '# ------------------------------------------------------------- #'

	builder = site_builder.builder(core)
	cherrypy.quickstart(WebApp(), config=core.conf_name)