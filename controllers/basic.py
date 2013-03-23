# -*- coding: utf-8 -*-

import __init__
import settings
import site_builder
import re
import cherrypy
import __main__

class defaultClass:

	def __init__(self):
		pass

	def loadSettings(self):
		try:
			self.core
		except:
			self.core = __main__.core

class defaultController(defaultClass):

	DIR = './'
	title = 'page_title_name'

	def __init__(self, preload = True):
		defaultClass.__init__(self)
		self.sbuilder = site_builder.builder()

		if preload:
			self.__initialize()

	def __initialize(self):
		defaultClass.loadSettings(self)

	def __checkParam(self, params, name, criteria = {}):

		def convert(item):
			try:
				return int(item)
			except Exception:
				return False

		status = True
		errors = []

		if not name in params:
			status = False
			errors.append({'name': name, 'desc': 'null'})

		else:
			errors_count = len(errors)

			if 'min_length' in criteria and criteria['min_length']>len(params[name]):
				errors.append({'name': name, 'desc': 'min_length_fail'})

			if 'max_length' in criteria and criteria['max_length']<len(params[name]):
				errors.append({'name': name, 'desc': 'max_length_fail'})

			# x > param
			if 'gt' in criteria and convert(params[name]) and criteria['gt'] >= int(params[name]):
				errors.append({'name': name, 'desc': 'not_greater'})

			# x < param
			if 'lt' in criteria and convert(params[name]) and criteria['lt'] <= int(params[name]):
				errors.append({'name': name, 'desc': 'not_lower'})

			# x => param
			if 'gte' in criteria and convert(params[name]) and criteria['gte'] > int(params[name]):
				errors.append({'name': name, 'desc': 'not_greater_or_equal'})

			# x <= param
			if 'lte' in criteria and convert(params[name]) and criteria['lte'] < int(params[name]):
				errors.append({'name': name, 'desc': 'not_lower_or_equal'})

			if 'not_null' in criteria and params[name] == '':
				errors.append({'name': name, 'desc': 'null'})

			if 'exist' in criteria and not name in params:
				errors.append({'name': name, 'desc': 'not_exist'})

			if 'int' in criteria:
				try:
					int(params[name])
				except Exception:
					errors.append({'name': name, 'desc': 'not_int'})

			if 'in' in criteria and convert(params[name]) and not criteria['in'] in params[name]:
				errors.append({'name': name, 'desc': 'not in allowed values'})

			if 'match' in criteria:
				if re.match(criteria['match'], params[name]) == None:
					errors.append({'name': name, 'desc': 'not_match'})

			if 'not_dublicate' in criteria:
				collection_name = criteria['not_dublicate'].keys()[0]
				field = criteria['not_dublicate'].values()[0]
				if self.model.misc.isDuplicate(collection_name, {field: re.compile('^'+params[name].strip()+'$', re.I+re.U)}):
					errors.append({'name': name, 'desc': 'dublicate'})

			# итоговое состояние — если нашли хоть одну ошибку, то статус = False
			if errors_count != len(errors):
				status = False

		return {'status': status, 'errors': errors}

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

	def printPage(self, page, methods, params = {}):

		def runRule(urls, name):

			if name in urls:
				rule = urls[name]
			elif name == '__default__':
				rule = 'printDefault'
			else:
				return 'error! page rule not found'

			if isinstance(rule, dict):
				params.update(rule['params'])
				if rule['method']:
					return rule['method']({'fields': fields, 'params': params})
				else:
					methods(params)
			else:
				return getattr(self, rule)({'fields': fields, 'params': params})


		fields = {}


		params.update({'__page__': page, '__query__': cherrypy.request.query_string})

		#res = methods(params)
		res = False

		if res and self.isAjax():
			return res

		if isinstance(res, dict) and 'critical_error' in res:
			fields.update({'critical_error': res['critical_error']})

		if 'errors' in params:
			fields.update({'errors': params['errors']})

		if res and 'ok' in res:
			fields.update({'success': True})

		fields.update(self.__paramsConvert(params))

		# если метод обработчика возвращает страницу, тогда выведем ее
		# не дожидаясь выполнения print page
		if isinstance(res, unicode) or isinstance(res, str):
			return res

		# print page
		return runRule(self.pages['urls'], page)

	def printDefault(self, data):
		return self.printTemplate(self.core.SERVICE_TEMPLATES['default'], data)

	def isAjax(self):
		return 'X-Requested-With' in cherrypy.request.headers and cherrypy.request.headers['X-Requested-With'] == 'XMLHttpRequest'

	def checkParams(self, params, rules):

		status = {'status': True, 'errors': []}

		for key in rules:
			buff = self.__checkParam(params, key, rules[key])
			if not buff['status']:
				for error in buff['errors']:
					status['errors'].append(error)

				status['status'] = False

		return status

	def pageMethods(self, rules, params):
		for param_name in rules:
			if param_name in params:
				if isinstance(rules[param_name], dict):
					actions = rules[param_name]
					for key in actions:
						if params[param_name] == key:
							return actions[key](params)
				else:
					return rules[param_name](params)

	def httpRedirect(self, params, additional = ''):
		if 'backlink' in params:
			params['__page__'] = params['backlink']

		self.sbuilder.httpRedirect(params['__page__']+additional)

	def printTemplate(self, tmp, data):
		return self.sbuilder.loadTemplate(self.DIR+tmp+'.jinja2', data)