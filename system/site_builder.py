# -*- coding: utf-8 -*-

import __init__
import cherrypy
import __main__

from jinja2 import Environment, FileSystemLoader

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

	def httpRedirect(self, url):
		raise cherrypy.HTTPRedirect(url)

	def loadTemplate(self, filename = '', data = {'fields': {} }):

		if not 'current_page' in data['fields']:
			data['fields'].update({
				'current_page': filename,
				'version': self.core_settings.__version__,
				'address': cherrypy.request.path_info[1:],
				'build': self.core_settings.__build__,
				'conf_name': self.core_settings.loaded_data['conf_name']
			})

		data['fields'].update(self.base_fields)

		template = self.env.get_template(filename)

		text = template.render(data['fields'])

		return text