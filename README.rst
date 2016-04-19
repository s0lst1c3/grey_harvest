grey_harvest
============

Scrapes the web for reliable http/https proxies and tests them for
speed and reliability. Can be used as both a python module and a 
command line utility. When run as a command line utility, proxies
are sent to stdout. When run as a module, it returns a generator.

Check out the project on PyPi at https://pypi.python.org/pypi/grey_harvest/0.1.3.5

Key Features
------------
- Quickly and easily generate a list of reliable http/https proxies
- Usable as a comamnd line utility or a python module
- Can filter for proxies that support SSL
- Can filter for proxies locationed within specific countries
- Can exclude proxies located within specific countries

Installation
------------

First, install the following dependencies::

	# On Centos/RHEL/Fedora:
	sudo yum install python-devel libxlt-devel libxml-devel

	# On Debian/Ubuntu:
	sudo apt-get install python-dev libxml2-dev libxslt1-dev

Then install grey_harvest using pip as follows::
	
	pip install grey_harvest

Usage
-----

We can generate a list of 10 viable proxies with the following command::

	# use the -n flag to specify number of proxies to generate
	grey_harvest -n 10
		
To select only proxies with SSL enabled, we do this::

	# use the -H flag to select only https proxies
	grey_harvest -n 10 -H

We can use the -a flag to filter for proxies located within a
list of specific countries. For example, to choose proxies located
within Ukraine, Hong Kong, and the United States, we'd use this::

	# use the -a flag to filter by country
	grey_harvest -a "United States" "Hong Kong" Ukraine -n 10


We can use the -p flag to filter for ports running on specific ports::

	# the -p flag to only use proxies that run on port 80
	grey_harvest -p 80 -n 10


We can deny proxies located within specific countries by using
the -d flag. Proxies located within China are blocked by default
as they are often located behind the Great Firewall, and as such
tend to be unreliable. This can be changed within grey_harvest.py's
internal configs.::

	# use the -d flag to deny proxies located within France and
	# Germany
	grey_harvest -d France Germany -n 10 -H

grey_harvest library - basic example
------------------------------------

Before diving into the documentation for the grey_harvest library,
check out how easily we can generate a list of 20 proxies::

	import gray_harvest

	''' spawn a harvester '''
	harvester = grey_harvest.GreyHarvester()

	''' harvest some proxies from teh interwebz '''
	count = 0
	for proxy in harvester.run():
		print proxy
		count += 1
		if count >= 20:
			break

That's it. We now have 20 http/https proxies ready to go.
		




