#!/usr/bin/python3.5
from urllib.parse import urlencode
from urllib.request import Request, urlopen, build_opener
from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler
import json

TESLA_CLIENT_ID = "e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e"
TESLA_CLIENT_SECRET = "c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220"

URL = "https://owner-api.teslamotors.com/oauth/token" 
with open("../login.info","r") as fd:
    email=fd.readline().rstrip()
    password=fd.readline().rstrip()

oauth = {"grant_type" : "password",
         "client_id" : TESLA_CLIENT_ID,
         "client_secret" : TESLA_CLIENT_SECRET,
         "email" : email,
         "password" : password }

req = Request(URL)
req.data = urlencode(oauth).encode('utf-8') # Python 3
opener = build_opener()
resp = opener.open(req)
charset = resp.info().get('charset', 'utf-8')
v = json.loads(resp.read().decode(charset))

print("Response:")
print(v)
print("Save to ../access_token")
with open("../access_token", "w") as fd:
    fd.write(v['access_token'])
