# -*- coding: UTF-8 -*-

import pymongo

class dbAdapter():

	def	__init__(self, settings):
		self.core = settings

		try:
			self.con = pymongo.Connection(
				settings.conf['database']['address'],
				settings.conf['database']['port']
			)
		except pymongo.errors.AutoReconnect:
			print settings.formatError('ERROR! Could not connect to mongo instance -> '+settings.conf['database']['address']+':'+str(settings.conf['database']['port']))
			exit()

		self.db = self.con[settings.conf['database']['database']]

		self.db.authenticate(
			settings.conf['database']['user'],
			settings.conf['database']['pass']
		)

	def __getSorted(self, sort):
		sort_buff = []

		if isinstance(sort, dict):
			for item in sort:
				sort_buff.append([item, sort[item]])

		return sort_buff

	def setCollection(self, collection_name):
		self.collection = self.db[collection_name]

	def collectionExist(self, collection_name):
		return collection_name in self.db.collection_names()

	def createCollection(self, collection_name):
		try:
			self.db.create_collection(collection_name)
			return True
		except Exception:
			return False

	def cleanUp(self, collection_name):
		if self.collectionExist(collection_name):
			items = self.db[collection_name]
			items.remove()
		else:
			self.createCollection(collection_name)

	def addIndex(self, collection_name, field):
		collection = self.db[collection_name]
		collection.ensure_index(field, unique=True)

	def insert(self,collection_name,item):
		items = self.db[collection_name]
		return items.insert(item)

	def remove(self, collection_name, search = {}):
		items = self.db[collection_name]
		items.remove(search)

	def update(self, collection_name, search, update, insert = False, multi = False):
		items = self.db[collection_name]

		if multi:
			return items.update(search, update, multi=True)

		return items.update(search, update, insert, multi)

	def getLastError(self):
		return self.db.error()

	def count(self, collection_name, search = {}):
		items = self.db[collection_name]
		return items.find(search).count()

	def findOne(self, collection_name, search = {}, fields = {}):
		output = self.get(collection_name, search = search, fields = fields, limit=1)
		if output:
			return output[0]
		else:
			return False

	def get(self, collection_name, search = {}, fields = {}, limit = 0, sort = {}, skip = 0):

		items = self.db[collection_name]
		output = []

		if limit:
			if sort:
				if fields:
					result = items.find(search, fields).sort(self.__getSorted(sort)).skip(skip).limit(limit)
				else:
					result = items.find(search).sort(self.__getSorted(sort)).skip(skip).limit(limit)
			else:
				if fields:
					result = items.find(search, fields).skip(skip).limit(limit)
				else:
					result = items.find(search).skip(skip).limit(limit)
		else:
			if sort:
				if fields:
					result = items.find(search, fields).sort(self.__getSorted(sort))
				else:
					result = items.find(search).sort(self.__getSorted(sort))
			else:
				if fields:
					result = items.find(search, fields)
				else:
					result = items.find(search)

		if result:
			for i in result:
				output.append(i)

		return output