# -*- coding: utf-8 -*-

# Core settings
# author: Alex Shteinikov

import __main__
import sys, os, inspect
import ConfigParser
from models_loader import DataModel

class CoreConfigParser():

	params = [
		{
			'scope': 'database',
			'params_int': ['port'],
			'params_str': ['address', 'user', 'pass', 'database', 'connector'],
		},
		{
			'scope': 'debug',
			'params_bool': ['web_debug', 'model_debug']
		},
		{
			'scope': 'misc',
		    'params_bool': ['git_revision']
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
					if 'params_int' in section and param_name in section['params_int']:
						value = int(self.config.get(section['scope'], param_name))
					else:
						value = self.__prettyStr(self.config.get(section['scope'], param_name))
						if 'params_bool' in section and param_name in section['params_bool']:
							value = bool(value)
				except:
					value = False

				parsed_params.update({param_name: value})

			fields.update({section['scope']: parsed_params})

		try:
			site_address = self.__prettyStr(self.config.get('global','site.host'))

			fields.update({
				'site_address': 'http://' + site_address + '/',
				'conf_name': self.conf_str_name
			})

		except Exception, e:
			print '>>> Error! Unable to load config data'
			print str(e)
			exit()

		return fields

class core():

	__appname__  = u'Auchenflower Framework'
	__version__  = u'0.5'
	__revision__ = False

	db = None
	model = None

	APP_DIR = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])+'/../'

	MODELS_DIR = './models'
	CONTROLLERS_DIR = './controllers'
	TEMPLATES_FOLDER = './templates/'

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

		self.__modelLoad()

	def __databaseLoad(self, connector_name):

		database_folder = self.APP_DIR+'/system/database'

		self.database_connector = False
		for item in os.listdir(database_folder):
			if item[-2:] == 'py' and item == connector_name:
				self.database_connector = __import__(item[:-3:])
				break
		else:
			print 'No module found'

		try:
			self.db = self.database_connector.dbAdapter(self)
		except Exception, e:
			print self.formatError('Database load error: '+str(e))
			exit()

	def __modelLoad(self):
		self.model = DataModel.loadGlobalModel(self)

	def __getBuildInfo(self):
		result = os.popen('git log | grep "^commit" | wc -l')
		lines = result.readlines()
		self.__revision__ = int(lines[0])

	def formatError(self, text):
		length = len(text)
		decor = '# '+'-'*(length+2)+' #'
		return decor+'\n#  '+text+'  #\n'+decor