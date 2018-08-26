#!/usr/bin/python3.5
import api
import json

with open('../access_token','r') as fd:
    access_token=fd.readline()

c = api.Connection(access_token)
v = c.vehicles[0]

print(v)
