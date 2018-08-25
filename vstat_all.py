#!/usr/bin/python3.5
import time
import api as teslajson
import plot
SAMPLE_TIME_IN_MIN=60*2
def go_sleep(sec):
    for d in range(sec):
        with open('/tmp/mon','w') as fd:
            fd.write("{}/{}".format(d,sec))
        time.sleep(1)
with open("../login.info","r") as fd:
    email=fd.readline().rstrip()
    pwd=fd.readline().rstrip()
try:
    c = teslajson.Connection(email, pwd)
    v = c.vehicles[0]
except:
    print ("Error connection...")
    exit()
for kk,vv in v.items():
    print ("{}:----{}".format(kk,vv))
    
v.wake_up()

cha = v.data_request('charge_state')
cli = v.data_request('climate_state')
veh = v.data_request('vehicle_state')
dri = v.data_request('drive_state')

print ("[CHARGE]")
for kk,vv in cha.items():
    print ("{}:----{}".format(kk,vv))

print ("[CLIMATE]")
for kk,vv in cli.items():
    print ("{}:----{}".format(kk,vv))

print ("[VEHICLE]")
for kk,vv in veh.items():
    print ("{}:----{}".format(kk,vv))

print ("[DRIVE]")
for kk,vv in dri.items():
    print ("{}:----{}".format(kk,vv))
    
