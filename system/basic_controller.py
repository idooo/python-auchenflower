# -*- coding: utf-8 -*-

import __init__
import __main__
import site_builder
from simplejson import dumps as toJSON
import cherrypy

class defaultClass:

	def __init__(self):
		pass

	def loadSettings(self):
		try:
			self.core
		except:
			self.core = __main__.core

		self.model = self.core.model

class defaultController(defaultClass):

	DIR = './'
	title = 'page_title_name'

	pages = {}
	methods = {}
	conditional_methods = {}

	def __init__(self, preload = True):
		defaultClass.__init__(self)
		self.sbuilder = site_builder.builder()

		if preload:
			self.__initialize()

	def __initialize(self):
		defaultClass.loadSettings(self)

	def __paramsConvert(self, params):
		result = {}
		for param_name in params:
			if param_name[0] != '_':
				result.update({'param_'+param_name: params[param_name]})
			else:
				result.update({param_name: params[param_name]})

		if 'errors' in params:
			error_fields = []
			for error in params['errors']:
				error_fields.append(error['name'])

			result.update({'error_fields': error_fields})

		return result

	def __isAjax(self):
		return 'X-Requested-With' in cherrypy.request.headers and cherrypy.request.headers['X-Requested-With'] == 'XMLHttpRequest'

	def printPage(self, page, paths, params = {}):

		def runMethod(params):

			methods = self.methods.copy()
			if page in self.conditional_methods:
				methods.update(self.conditional_methods[page])

			if not methods:
				return False

			for param_name in params:
				if param_name in methods:
					if isinstance(methods[param_name], dict):
						if params[param_name] in methods[param_name]:
							method_name = methods[param_name][params[param_name]]
						else:
							method_name = methods[param_name]
					else:
						method_name = methods[param_name]

					if isinstance(method_name, str) and hasattr(self, method_name):
						return getattr(self, method_name)(params)
					else:
						return self.sbuilder.throwFrameworkError(
							name='method not defined',
							context={
								'class': str(self.__class__),
								'method name': method_name
							}
						)

		def runRule(urls, name):

			if name in urls:
				rule = urls[name]
			elif name == '__default__':
				rule = 'printDefault'
			else:
				return self.sbuilder.throwFrameworkError(
					name='page rule not found',
					context={
						'page rule': name,
						'allowed': urls.keys()
					}
				)

			data = {
				'levels': paths,
				'fields': fields,
				'params': params
			}

			if hasattr(self, rule):
				return getattr(self, rule)(data)
			else:
				return self.sbuilder.throwFrameworkError(
					name='response page not defined',
					context={
						'class': str(self.__class__),
						'method name': rule
					}
				)

		fields = {}
		res = runMethod(params)

		params.update({'__page__': page, '__query__': cherrypy.request.query_string})

		if res:
			if not isinstance(res, dict):
				return res

			if self.__isAjax() or '__ajax__' in params:
				return toJSON(res)

			else:
				fields.update({'__method__': res})


		fields.update(self.__paramsConvert(params))

		return runRule(self.pages['urls'], page)

	def redirect(self, url_or_params, additional = ''):

		if isinstance(url_or_params, dict):
			if 'backlink' in url_or_params:
				url_or_params['__page__'] = url_or_params['backlink']

			self.sbuilder.httpRedirect(url_or_params['__page__']+additional)
		else:
			self.sbuilder.httpRedirect(url_or_params+additional)

	def printDefault(self, data):
		return self.printTemplate(self.core.SERVICE_TEMPLATES['default'], data)

	def printTemplate(self, tmp, data):
		return self.sbuilder.loadTemplate(self.DIR+tmp+'.jinja2', data)