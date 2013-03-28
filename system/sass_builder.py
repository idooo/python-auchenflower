import sass
import os

class sassParser():

	src_dir = None
	output_dir = None
	enabled = False

	def __init__(self, core):
		self.core = core
		self.enabled = core.conf['sass']['enabled']

		if self.enabled:
			self.src_dir = core.APP_DIR + core.conf['sass']['src_dir']
			self.output_dir = core.APP_DIR + core.conf['sass']['output_dir']

	def parse(self):

		files = []
		for item in os.listdir(self.src_dir):

			#if os.path.isdir(self.src_dir+'/'+item):
			#	print 'DIR',item

			if item[-4:] == 'scss' or item[-4:] == 'sass':
				data = {
					'name': item,
					'clearname': item[:-5:],
				}

				f = open(self.src_dir+'/'+item)
				text = f.read()
				print sass.compile(text)
				f.close()


