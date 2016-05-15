"""
''' File:        grey_harvest.py
''' Author:      Gabriel "s0lst1c3" Ryan
''' Created:     Tue May 26 2015
''' Source:      https://github.com/s0lst1c3/grey_harvest
''' License:     MIT (see attached)
''' Description: Scrapes the web for reliable http or https proxies and prints
'''              them  to  stdout.  Can  also be  used as a  python library to 
'''              easily  generate  reliable  proxies  for  use  within  Python
'''              application (see README.md).
"""

__version__   = '0.1.6'
__author__    = 'Gabriel "s0lst1c3" Ryan'
__license__   = 'MIT'
__copyright__ = 'Copyright (c) 2015'

import requests
import socket
import sys
import argparse
from time import sleep
from bs4  import BeautifulSoup
from lxml import etree

''' configs '''
DOC_ROOT          = 'http://freeproxylists.com'
ELITE_PAGE        = 'elite.html'
HTTPS_ONLY        = True
ALLOWED_COUNTRIES = None
DENIED_COUNTRIES  = ['China']
MAX_TIMEOUT       = 1
TEST_SLEEPTIME    = 1
TEST_DOMAIN       = 'example.com'

class Proxy(dict):

    def __init__(self, ip, port, country=None,
            latency=None, https=False, last_checked=None):

        dict.__init__(self)
        self.ip = ip
        self.port = int(port)
        self.country = country
        self.latency = int(latency)
        self.https = https
        self['ip'] = ip
        self['port'] = port
        self['country'] = country
        self['latency'] = latency
        self['https'] = https

    def test(self,
            test_domain=TEST_DOMAIN,
            test_sleeptime=TEST_SLEEPTIME,
            max_timeout=MAX_TIMEOUT):
    
                ''' get ready for test '''
                protocol = 'https' if self['https'] else 'http'
                test_url = '%s://%s' % (protocol, test_domain)
                proxies = {
                    'https://%s' : str(self),
                    'http://%s' : str(self),
                }
    
                ''' make a brief HEAD request to test_domain and see if it times out '''
                requests.head(test_url, timeout=max_timeout, proxies=proxies)
                try:
                    response = requests.head(test_url, timeout=max_timeout, proxies=proxies)
                    if test_sleeptime > 0:
                        sleep(test_sleeptime)
                    return True
                except requests.exceptions.ConnectionError:
                    if test_sleeptime > 0:
                        sleep(test_sleeptime)
                    return False

    def __str__(self):
        return '%s:%s' % (self.ip, self.port)

class GreyHarvester(object):

    def __init__(self,
            test_domain=TEST_DOMAIN,
            test_sleeptime=TEST_SLEEPTIME,
            https_only=HTTPS_ONLY,
            allowed_countries=ALLOWED_COUNTRIES,
            denied_countries=DENIED_COUNTRIES,
            ports=None,
            max_timeout=MAX_TIMEOUT):
                        
                self.allowed_countries = allowed_countries
                self.denied_countries = denied_countries
                self.max_timeout = max_timeout
                self.test_sleeptime = test_sleeptime 
                self.test_domain = test_domain
                self.https_only = https_only

                self.all_ports = ports is None
                self.ports = ports

    def run(self):
        for endpoint in self._extract_ajax_endpoints():
            for proxy in self._extract_proxies(endpoint):
                if self._passes_filter(proxy) and proxy.test(
                        test_domain=self.test_domain,
                        test_sleeptime=self.test_sleeptime,
                        max_timeout = self.max_timeout,
                    ) == True: yield proxy

    def _extract_proxies(self, ajax_endpoint):
    
        ''' request the xml object '''
        proxy_xml = requests.get(ajax_endpoint)
        print(proxy_xml.content)
        root = etree.XML(proxy_xml.content)
        quote = root.xpath('quote')[0]
        
        ''' extract the raw text from the body of the quote tag '''
        raw_text = quote.text
        
        ''' eliminate the stuff we don't need '''
        proxy_data = raw_text.split('You will definitely love it! Give it a try!</td></tr>')[1]
        
        ''' get rid of the </table> at the end of proxy_data '''
        proxy_data = proxy_data[:-len('</table>')]
        
        ''' split proxy_data into rows '''
        table_rows = proxy_data.split('<tr>')
        
        ''' convert each row into a Proxy object '''
        for row in table_rows:
            
            ''' get rid of the </tr> at the end of each row '''
            row = row[:-len('</tr>')]
        
            ''' split each row into a list of items '''
            items = row.split('<td>')
            
            ''' sometimes we get weird lists containing only an empty string '''
            if len(items) != 7:
                continue
    
            ''' we'll use this to remove the </td> from the end of each item '''
            tdlen = len('</td>')
    
            ''' create proxy dict '''
            proxy = Proxy(
                ip=items[1][:-tdlen],
                port=int(items[2][:-tdlen]),
                https=bool(items[3][:-tdlen]),
                latency=int(items[4][:-tdlen]),
                last_checked=items[5][:-tdlen],
                country=items[6][:-tdlen],
            )
            yield proxy

    def _passes_filter(self, proxy):


        ''' avoid redudant and space consuming calls to 'self' '''
        
        ''' validate proxy based on provided filters '''
        if self.allowed_countries is not None and proxy['country'] not in self.allowed_countries:
            return False
        if self.denied_countries is not None and  proxy['country'] in self.denied_countries:
            return False
        if self.https_only and proxy['https'] == False:
            return False

        if not self.all_ports and str(proxy.port) not in self.ports:
            return False

        return True

    def _extract_ajax_endpoints(self):
    
        ''' make a GET request to freeproxylists.com/elite.html '''
        url = '/'.join([DOC_ROOT, ELITE_PAGE])
        response = requests.get(url)
    
        ''' extract the raw HTML doc from the response '''
        raw_html = response.text
    
        ''' convert raw html into BeautifulSoup object '''
        soup = BeautifulSoup(raw_html, 'lxml')

        for url in soup.select('table tr td table tr td a'):
            if 'elite #' in url.text:
                yield '%s/load_elite_d%s' % (DOC_ROOT, url['href'].lstrip('elite/'))

def setup(parser):
    
    parser.add_argument('-a', '--allowed-countries',
                    dest='allowed_countries',
                    nargs='*',
                    metavar='<country>',
                    required=False,
                    default=ALLOWED_COUNTRIES,
                    help='''Only use proxies physically located in the specified countries.'''
    )
    parser.add_argument('-p', '--ports',
                    dest='ports',
                    nargs='*',
                    metavar='<port>',
                    required=False,
                    help='''Only use proxies running on the specified ports.'''
    )
    parser.add_argument('-d', '--denied-countries',
                    dest='denied_countries',
                    nargs='*',
                    metavar='<country_1>',
                    default=DENIED_COUNTRIES,
                    required=False,
                    help='Do not use proxies physically located these countries. This flag takes precedence over --allowed-countries.'''
    )
    parser.add_argument('-t', '--max-timeout', 
                    dest='max_timeout',
                    nargs=1,
                    type=int,
                    metavar='<N>',
                    default=MAX_TIMEOUT,
                    required=False,
                    help='Discard proxies that do not respond within <N> seconds of HEAD request.'
    )
    parser.add_argument('-H', '--https-only',
                    action='store_true',
                    dest='https_only',
                    default=HTTPS_ONLY,
                    help='Only keep proxies with https support.',
    )
    parser.add_argument('-D', '--test-domain', 
                    dest='test_domain',
                    type=str,
                    metavar='<test_domain>',
                    default=TEST_DOMAIN,
                    required=False,
                    help='Test proxies by making HEAD request to <test domain>',
    )
    parser.add_argument('-n', '--num-proxies',
                    dest='num_proxies',
                    nargs=1,
                    type=int,
                    metavar='<N>',
                    required=True,
                    help='Harvest <N> working and free proxies from teh interwebz',
    )
    
    args = parser.parse_args()

    if args.ports:
        ALL_PORTS = False

    return {
        'num_proxies' : args.num_proxies[0],
        'test_domain' : args.test_domain,
        'https_only' : args.https_only,
        'max_timeout' : args.max_timeout,
        'allowed_countries' : args.allowed_countries,
        'denied_countries' : args.denied_countries,
        'ports' : args.ports,
    }

def main():

    ''' set things up '''
    configs =  setup(argparse.ArgumentParser())
    harvester = GreyHarvester(
        test_domain=configs['test_domain'],
        test_sleeptime=TEST_SLEEPTIME,
        https_only=configs['https_only'],
        allowed_countries=configs['allowed_countries'],
        denied_countries=configs['denied_countries'],
        ports=configs['ports'],
        max_timeout=configs['max_timeout']
    )

    ''' harvest free and working proxies from teh interwebz '''
    count = 0
    for proxy in harvester.run():
        if count >= configs['num_proxies']:
            break
        print(proxy)
        count += 1

if __name__ == '__main__':
    main()
