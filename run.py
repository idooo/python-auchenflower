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
		pages = []
		for item in self.controller.alias:
			for type_of_method in item['type']:
				if not type_of_method in self.page_runners:
					self.page_runners.update({type_of_method:[item]})
				else:
					self.page_runners[type_of_method].append(item)

		for runner in self.page_runners:
			if 'default' in self.page_runners[runner][0]['type']:
				pages += self.page_runners[runner][0]['urls']
			else:
				pages += self.page_runners[runner][0]['type']

		for item in pages:
			self.pages.add(item)

	def __load(self, func_name, page, params):
		for variant in self.page_runners[func_name]:
			if page in variant['urls']:
				return self.controller.controllers[variant['name']].printPage(page, {}, params)

		return builder.throwWebError(params=params)

	def index(self, **params):
		return self.__load(inspect.stack()[0][3],'index', params)

	def default(self, page, **params):
		if page in self.pages:
			return self.__load(inspect.stack()[0][3], page, params)

	index.exposed = True
	default.exposed = True

root = WebApp()

if __name__ == '__main__':

	print '# ----------------------------------------- #'
	print '#  Site version:', core.__version__, 'build:', core.__build__
	print '# ----------------------------------------- #'

	builder = site_builder.builder(core)
	cherrypy.quickstart(WebApp(), config=core.conf_name)