#!/usr/bin/python3.5
import time
import datetime
import api
import plot

print (datetime.datetime.now())

with open("../access_token","r") as fd:
    access_token=fd.readline()

c = api.Connection(access_token)
v = c.vehicles[0]

for kk,vv in v.items():
    print ("{}:----{}".format(kk,vv))

print ('[WAKE_UP]')
v.wake_up()

print ("[VEHICLE]")
veh = v.data_request('vehicle_state')
for kk,vv in veh.items():
    print ("{}:----{}".format(kk,vv))

print ("[CHARGE]")
cha = v.data_request('charge_state')
for kk,vv in cha.items():
    print ("{}:----{}".format(kk,vv))

print ("[CLIMATE]")
cli = v.data_request('climate_state')
for kk,vv in cli.items():
    print ("{}:----{}".format(kk,vv))

print ("[DRIVE]")
dri = v.data_request('drive_state')
for kk,vv in dri.items():
    print ("{}:----{}".format(kk,vv))
    
