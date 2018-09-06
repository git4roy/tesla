#!/usr/bin/python3.5
import api_r as api
import json
import datetime

print (datetime.datetime.now())

with open('../access_token','r') as fd:
    access_token=fd.readline()

c = api.Connection(access_token)
v = c.vehicles[0]
c.close()

for k in sorted(v.keys()):
    print ("{}:-----> {}".format(k,v[k]))
