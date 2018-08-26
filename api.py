from urllib.parse import urlencode
from urllib.request import Request, urlopen, build_opener
from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler
import json
import datetime
import calendar

TESLA_CLIENT_ID = "e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e"
TESLA_CLIENT_SECRET = "c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220"

class Connection(object):
        def __init__(self, access_token=''):
                self.baseurl = "https://owner-api.teslamotors.com" 
                self.api = "/api/1/"
                self.__sethead(access_token)
                self.vehicles = [Vehicle(v, self) for v in self.get('vehicles')['response']]
        
        def get(self, command):
                return self.post(command, None)

        def post(self, command, data={}):
                return self.__open("%s%s" % (self.api, command), headers=self.head, data=data)

        def __sethead(self, access_token, expiration=float('inf')):
                self.access_token = access_token
                self.head = {"Authorization": "Bearer %s" % access_token}

        def __open(self, url, headers={}, data=None, baseurl=""):
                if not baseurl:
                        baseurl = self.baseurl
                req = Request("%s%s" % (baseurl, url), headers=headers)
                try:
                        req.data = urlencode(data).encode('utf-8') # Python 3
                except:
                        try:
                                req.add_data(urlencode(data)) # Python 2
                        except:
                                pass

                opener = build_opener()
                resp = opener.open(req)
                charset = resp.info().get('charset', 'utf-8')
                return json.loads(resp.read().decode(charset))

class Vehicle(dict):
        def __init__(self, data, connection):
                super(Vehicle, self).__init__(data)
                self.connection = connection

        def data_request(self, name):
                result = self.get('data_request/%s' % name)
                return result['response']

        def wake_up(self):
                return self.post('wake_up')

        def command(self, name, data={}):
                return self.post('command/%s' % name, data)

        def get(self, command):
                return self.connection.get('vehicles/%i/%s' % (self['id'], command))

        def post(self, command, data={}):
                return self.connection.post('vehicles/%i/%s' % (self['id'], command), data)
