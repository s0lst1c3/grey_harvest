import os

from setuptools import setup

def read(*paths):
	with open(os.path.join(*paths), 'r') as fd:
		return fd.read()

setup(
	name = 'grey_harvest',
	version = '0.1.6',
	description = 'Generate lists of free, reliable http(s) proxies.',
	long_description=(read('README.rst')+'\n\n'+\
					  read('HISTORY.rst')+'\n\n'+\
					  read('AUTHORS.rst')+'\n\n'),
	url = 'https://github.com/s0lst1c3/grey_harvest',
	download_url = 'https://github.com/s0lst1c3/grey_harvest/tarball/0.1.2',
	license = 'MIT',
	author = 'Gabriel "s0lst1c3" Ryan',
	author_email = 'gabriel@solstice.me',
	py_modules = ['grey_harvest'],
	include_package_data = True,
	install_requires = [
		'requests',
		'pyOpenSSL',
		'beautifulsoup4',
		'lxml',
		'argparse',
	],
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 2.7',
		'Topic :: Internet :: Proxy Servers',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Security',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: System :: Systems Administration',
		'Topic :: Utilities',
	],
	entry_points = {
		'console_scripts' : [
			'grey_harvest=grey_harvest:main',
		],
	},
)
