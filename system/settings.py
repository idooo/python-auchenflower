# -*- coding: utf-8 -*-

# Core settings
# author: Alex Shteinikov

import __main__
import sys, os, inspect
import ConfigParser
import sass_builder
from models_loader import DataModel

class CoreConfigParser():

	params = [
		{
			'scope': 'global',
	        'params_bool': ['request.show_tracebacks']
		},
		{
			'scope': 'database',
			'params_int': ['port'],
			'params_str': ['address', 'user', 'pass', 'database', 'connector'],
		},
		{
			'scope': 'debug',
			'params_bool': ['web_debug', 'model_debug', 'framework_errors']
		},
		{
			'scope': 'misc',
		    'params_bool': ['git_revision']
		},
		{
			'scope': 'sass',
		    'params_bool': ['enabled'],
		    'params_str': ['src_dir', 'output_dir']
		}
	]

	def __init__(self):

		try:
			print '\n> Loading', sys.argv[1], 'config'
		except Exception:
			print '\n> Loading default config'
			try:
				sys.argv[1] = 'default'
			except Exception:
				sys.argv.append('default')

		self.conf_str_name = sys.argv[1]

		self.conf_name = os.path.join(os.path.dirname(__file__)+'/../conf/', sys.argv[1]+'.conf')
		self.config = ConfigParser.ConfigParser()
		self.config.read(self.conf_name)

	def __prettyStr(self, datastr):
		return datastr[1:len(datastr)-1]

	def readData(self):

		fields = {}

		for section in self.params:
			parsed_params = {}

			available_param_names = []
			for group_name in ['params_int', 'params_str', 'params_bool']:
				if group_name in section:
					available_param_names += section[group_name]

			for param_name in available_param_names:
				try:
					raw_value = self.config.get(section['scope'], param_name)
				except ConfigParser.NoOptionError:
					raw_value = 0

				if 'params_int' in section and param_name in section['params_int']:
					try:
						value = int(raw_value)
					except ValueError:
						value = 0
						print '> WARNING! Wrong config int parameter value:', param_name, '=', raw_value

				elif 'params_bool' in section and param_name in section['params_bool']:
					value = unicode(raw_value) in ['True', 'true', '1']

				else:
					value = self.__prettyStr(self.config.get(section['scope'], param_name))

				parsed_params.update({param_name: value})

			fields.update({section['scope']: parsed_params})

		try:
			site_address = self.__prettyStr(self.config.get('global','site.host'))

			fields.update({
				'site_address': 'http://' + site_address + '/',
				'conf_name': self.conf_str_name
			})

		except Exception, e:
			print '> ERROR! Unable to load config data:'
			print str(e)
			exit()

		return fields

class core():

	__appname__  = u'Auchenflower Framework'
	__version__  = u'0.9'
	__revision__ = False

	__framework__ = {
		'name': u'Auchenflower Framework',
	    'version': u'0.9'
	}

	db = None
	model = None

	APP_DIR = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])+'/../'

	MODELS_DIR = './models'
	CONTROLLERS_DIR = './controllers'
	TEMPLATES_FOLDER = './templates/'
	ASSETS_FOLDER = './assets'

	SERVICE_TEMPLATES_DIR = './service/'
	SERVICE_TEMPLATES = {
		'default': SERVICE_TEMPLATES_DIR+'default',
	    'framework_error': SERVICE_TEMPLATES_DIR+'framework_error',
	    'debug': SERVICE_TEMPLATES_DIR+'debug',
	    'debug_model': SERVICE_TEMPLATES_DIR+'debug_model'
	}

	def __init__(self):
		config_loader = CoreConfigParser()
		self.conf = config_loader.readData()

		self.HOST = self.conf['site_address']
		self.conf_name = config_loader.conf_name

		self.base_fields = {'host': self.HOST}

		if self.conf['misc']['git_revision']:
			self.__getBuildInfo()

		if 'database' in self.conf and self.conf['database']['connector']:
			self.__databaseLoad(self.conf['database']['connector'])

		if 'sass' in self.conf and self.conf['sass']['enabled']:
			self.__sassParse()

		self.__modelLoad()

		# check debug mode
		is_debug = False
		for debug_var in self.conf['debug']:
			is_debug = is_debug or self.conf['debug'][debug_var]

		is_debug = is_debug or self.conf['global']['request.show_tracebacks']

		self.DEBUG_MODE = is_debug


	def __databaseLoad(self, connector_name):

		database_folder = self.APP_DIR+'/system/database'

		self.database_connector = False
		for item in os.listdir(database_folder):
			if item[-2:] == 'py' and item == connector_name:
				self.database_connector = __import__(item[:-3:])
				break
		else:
			print 'ERROR! Database module not found: '+connector_name
			exit()

		try:
			self.db = self.database_connector.dbAdapter(self)
		except Exception, e:
			print 'ERROR! Database load error: '+str(e)
			exit()

	def __modelLoad(self):
		self.model = DataModel.loadGlobalModel(self)

	def __getBuildInfo(self):
		result = os.popen('git log | grep "^commit" | wc -l')
		lines = result.readlines()
		self.__revision__ = int(lines[0])

	def __sassParse(self):
		self.css_preprocessor = sass_builder.sassParser(self)
		self.css_preprocessor.parseSass()
