import requests
import json

TESLA_CLIENT_ID = "e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e"
TESLA_CLIENT_SECRET = "c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220"

class Connection(object):
        def __init__(self, access_token=''):
                self.url = "https://owner-api.teslamotors.com/api/1/" 
                self.head = {"Authorization": "Bearer %s" % access_token, "Connection": "close"}
                self.vehicles = [Vehicle(v, self) for v in self.get('vehicles')['response']]
        
        def get(self, command):
                return self.post(command, None)

        def post(self, command, data={}):
                return self.__open("{}{}".format(self.url, command), data=data)

        def close(self):
                return self.get("vehicles")

        def __open(self, url, data=None):
                req = requests.get(url, headers=self.head)
                if req.status_code == 200:
                    response = req.json()
                elif req.status_code == 401:
                    response = 'Incorrect username or password'
                elif req.status_code == 404:
                    response = 'API server has changed, contact the developer of this script'
                elif req.status_code == 500:
                    response = 'An internal server error occurred. Either Tesla API is down or the API has changed!'
                return response

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
