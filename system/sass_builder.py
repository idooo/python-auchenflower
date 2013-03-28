from sassutils import builder
import os
import shutil

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

	def parseSass(self):

		def clearDir():
			folder = self.output_dir
			for the_file in os.listdir(folder):
				file_path = os.path.join(folder, the_file)
				try:
					if os.path.isdir(file_path):
						shutil.rmtree(file_path)
					else:
						os.unlink(file_path)
				except Exception, e:
					print e

		print '> SASS/SCSS files compiling...'

		clearDir()

		for item in os.listdir(self.src_dir):

			if os.path.isdir(self.src_dir+'/'+item):
				os.mkdir(self.output_dir+'/'+item)
				builder.build_directory(self.src_dir+'/'+item, self.output_dir+'/'+item)

		builder.build_directory(self.src_dir, self.output_dir)

		print '> CSS files were created'


