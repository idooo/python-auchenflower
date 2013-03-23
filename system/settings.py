# -*- coding: utf-8 -*-

# Core settings
# author: Alex Shteinikov

from time import time
import __main__
import sys, os, inspect
import ConfigParser

class CoreConfigParser():

	debug_var_names =  []

	def __init__(self):

		try:
			print '> Loading', sys.argv[1], 'config for Twitter'
		except Exception:
			print '> Loading default config for Twitter'
			try:
				sys.argv[1] = 'default'
			except Exception:
				sys.argv.append('default')

		self.conf_str_name = sys.argv[1]

		self.conf_name = os.path.join(os.path.dirname(__file__)+'/../conf/', sys.argv[1]+'.conf')
		self.config = ConfigParser.ConfigParser()
		self.config.read(self.conf_name)

	def prettyStr(self, datastr):
		return datastr[1:len(datastr)-1]

	def readData(self):
		try:
			site_address = self.prettyStr(self.config.get('global','site.host'))

			fields = {
				'site_address': 'http://' + site_address + '/',
				'conf_name': self.conf_str_name
			}

		except Exception, e:
			print '>>> Error! Unable to load config data'
			print str(e)
			exit()

		return fields

class core():

	__version__ = u"1.0"

	APP_DIR = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])+'/../'

	TEMPLATES_FOLDER = './templates/'

	def __init__(self):
		config_loader = CoreConfigParser()
		self.loaded_data = config_loader.readData()

		self.HOST = self.loaded_data['site_address']

		self.conf_name = config_loader.conf_name

		self.base_fields = {'host': self.HOST}

		self.getBuildInfo()

	def getBuildInfo(self):
		result = os.popen('git log | grep "^commit" | wc -l')
		lines = result.readlines()

		self.__build__ = int(lines[0])

