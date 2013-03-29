from sassutils import builder
import os
import re
import shutil

class sassParser():

	src_dir = None
	output_dir = None
	enabled = False

	RE_EXTENTIONS = re.compile('\.s(c|a)ss')

	def __init__(self, core):
		self.core = core
		self.enabled = core.conf['sass']['enabled']

		if self.enabled:
			self.src_dir = core.APP_DIR + core.conf['sass']['src_dir']
			self.output_dir = core.APP_DIR + core.conf['sass']['output_dir']

	def parseSass(self):

		def clearDir(folder):
			try:
				os.listdir(folder)
			except Exception, e:
				return {
					'status': False,
				    'error': str(e)
				}

			for the_file in os.listdir(folder):
				file_path = os.path.join(folder, the_file)

				try:
					if os.path.isdir(file_path):
						clearDir(file_path)
						shutil.rmtree(file_path)
					else:
						os.unlink(file_path)
				except Exception, e:
					return {
						'status': False,
						'error': str(e)
					}

			return {'status': True}

		def clearOutput(folder):
			os.listdir(folder)

			for the_file in os.listdir(folder):
				file_path = os.path.join(folder, the_file)

				try:
					if os.path.isdir(file_path):
						clearOutput(file_path)
					else:
						if the_file[0] == '_':
							os.remove(file_path)
						else:
							new_file_name = re.sub(self.RE_EXTENTIONS, '', file_path)
							os.rename(file_path, new_file_name)
				except Exception, e:
					print e

		print '> SASS/SCSS files compiling...'

		result = clearDir(self.output_dir)

		if not result['status']:
			print '> ERROR! SASS/SCSS compile FAIL:\n',result['error']
			exit()

		for item in os.listdir(self.src_dir):

			if os.path.isdir(self.src_dir+'/'+item):
				os.mkdir(self.output_dir+'/'+item)
				builder.build_directory(self.src_dir+'/'+item, self.output_dir+'/'+item)

		builder.build_directory(self.src_dir, self.output_dir)

		clearOutput(self.output_dir)

		print '> CSS files were created'


