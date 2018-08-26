from urllib.parse import urlencode
from urllib.request import Request, urlopen, build_opener
from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler
import json
import datetime
import calendar

TESLA_CLIENT_ID = "e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e"
TESLA_CLIENT_SECRET = "c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220"

class Connection(object):
        """Connection to Tesla Motors API"""
        def __init__(self,
                        email='',
                        password=''):
                self.baseurl = "https://owner-api.teslamotors.com" 
                self.api = "/api/1/"
                if 1:
                        self.oauth = {
                                "grant_type" : "password",
                                "client_id" : TESLA_CLIENT_ID,
                                "client_secret" : TESLA_CLIENT_SECRET,
                                "email" : email,
                                "password" : password }
                        self.expiration = 0 # force refresh
                self.vehicles = [Vehicle(v, self) for v in self.get('vehicles')['response']]

        def get(self, command):
                """Utility command to get data from API"""
                return self.post(command, None)

        def post(self, command, data={}):
                """Utility command to post data to API"""
                now = calendar.timegm(datetime.datetime.now().timetuple())
                if now > self.expiration:
                        auth = self.__open("/oauth/token", data=self.oauth)
                        self.__sethead(auth['access_token'],
                                       auth['created_at'] + auth['expires_in'] - 86400)
                return self.__open("%s%s" % (self.api, command), headers=self.head, data=data)

        def __sethead(self, access_token, expiration=float('inf')):
                """Set HTTP header"""
                self.access_token = access_token
                self.expiration = expiration
                self.head = {"Authorization": "Bearer %s" % access_token}

        def __open(self, url, headers={}, data=None, baseurl=""):
                """Raw urlopen command"""
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
