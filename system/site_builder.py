# -*- coding: utf-8 -*-

import __init__
import cherrypy
import __main__

from jinja2 import Environment, FileSystemLoader, exceptions

class builder():

	env = Environment(
		auto_reload=True,
		loader=FileSystemLoader(__main__.core.APP_DIR+'templates/')
	)

	def __init__(self, core = None):

		if not core:
			core = __main__.core

		self.core_settings = core
		self.base_fields = self.core_settings.base_fields

	def throwWebError(self, error_code = 404, params = {}):

		error = 'Unknown error'
		if error_code == 404:
			error = 'Page Not Found'

		fields = {'error': error, 'code':error_code }

		return self.loadTemplate('error.jinja2', fields)

	def throwFrameworkError(self, name, context = {}):
		data = {'fields': {
			'error_name': name,
		    'context': context
		}}
		return self.loadTemplate(self.core_settings.SERVICE_TEMPLATES['framework_error']+'.jinja2', data)

	def httpRedirect(self, url):
		raise cherrypy.HTTPRedirect(url)

	def loadTemplate(self, filename = '', data = {'fields': {} }):

		if not 'current_page' in data['fields']:
			data['fields'].update({
				'current_page': filename,
				'version': self.core_settings.__version__,
				'address': cherrypy.request.path_info[1:],
				'build': self.core_settings.__revision__,
				'conf_name': self.core_settings.loaded_data['conf_name']
			})

		data['fields'].update(self.base_fields)

		try:
			template = self.env.get_template(filename)
		except exceptions.TemplateNotFound, e:
			return self.throwFrameworkError('template not found', {'template name': str(e)})

		text = template.render(data['fields'])

		print data
		if self.core_settings.DEBUG:
			template = self.env.get_template(self.core_settings.SERVICE_TEMPLATES['debug']+'.jinja2')
			text += template.render(data)

		return text