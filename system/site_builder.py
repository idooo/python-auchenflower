# -*- coding: utf-8 -*-

import __init__
import __main__
import cherrypy

from jinja2 import Environment, FileSystemLoader, exceptions

class builder():

	env = Environment(
		auto_reload=True,
		loader=FileSystemLoader(__main__.core.APP_DIR+'templates/')
	)

	def __init__(self, core = None):
		try:
			self.core
		except:
			self.core = __main__.core

	def throwWebError(self, error_code = 404, params = {}):

		error = 'Unknown error'
		if error_code == 404:
			error = 'Page Not Found'

		fields = {'error': error, 'code':error_code }

		return self.loadTemplate('error.jinja2', fields)

	def throwFrameworkError(self, name, context = {}):
		data = {
			'fields': {
				'error_name': name,
			    'context': context
			}
		}

		if not self.core.conf['debug']['framework_errors']:
			raise Exception

		return self.loadTemplate(self.core.SERVICE_TEMPLATES['framework_error']+'.jinja2', data)

	def httpRedirect(self, url):
		raise cherrypy.HTTPRedirect(url)

	def loadTemplate(self, filename = '', data = {'fields': {} }):

		if not 'current_page' in data['fields']:
			data['fields'].update({
				'__base__': {
					'current_page': filename,
				    'app_name': self.core.__appname__,
				    'framework': self.core.__framework__['name']+', version: '+self.core.__framework__['version'],
					'version': self.core.__version__,
					'address': cherrypy.request.path_info[1:],
					'revision': self.core.__revision__,
					'conf_name': self.core.conf['conf_name']
				}
			})

		data['fields']['__base__'].update(self.core.base_fields)

		try:
			template = self.env.get_template(filename)
		except exceptions.TemplateNotFound, e:
			return self.throwFrameworkError('template not found', {'template name': str(e)})

		text = template.render(data['fields'])

		if self.core.conf['debug']['web_debug']:
			template = self.env.get_template(self.core.SERVICE_TEMPLATES['debug']+'.jinja2')
			text += template.render(data)

		if self.core.conf['debug']['model_debug']:
			template = self.env.get_template(self.core.SERVICE_TEMPLATES['debug_model']+'.jinja2')
			text += template.render({'__debug_model': self.core.model})

		return text