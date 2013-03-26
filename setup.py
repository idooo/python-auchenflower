from setuptools import setup

# @TODO remove setup.py and write script to download requires

setup(
	name='python-auchenflower',
	version='0.0.4',
	author='Alex Shteinikov',
	author_email='alex.shteinikov@gmail.com',
	url='https://github.com/idooo/python-auchenflower',
	license='LICENSE.txt',
	description='Python Auchenflower is simply framework for fast creating web applications.',
	long_description=open('README.txt').read(),
	install_requires=[
		"jinja2 >= 2.6",
		"cherrypy >= 3.2.2",
		],
	)
