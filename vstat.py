#!/usr/bin/python3.5
import time
import api

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
    c = api.Connection(email, pwd)
    v = c.vehicles[0]
except:
    print ("Error connection...")
    exit()
for kk,vv in v.items():
    print ("{}:----{}".format(kk,vv))
