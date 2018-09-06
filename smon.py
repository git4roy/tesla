#!/usr/bin/python3.5
import json
import time
import datetime
import api

print (datetime.datetime.now())
STATE=('asleep', 'offline', 'online')

with open('../access_token','r') as fd:
    access_token=fd.readline()

while True:
    try:
        print ("trying to connect...\n")
        c = api.Connection(access_token)
        state = c.vehicles[0]['state']
        c.close()
        rec=""
        for s,ss in enumerate(STATE):
            if ss==state:
                rec = "{},{},{}\n".format(datetime.datetime.now(),s,state)
    except:
        rec="{},{},{}\n".format(datetime.datetime.now(),-1,'error')

    print (">> {} <<".format(rec))
    with open('smon.csv','a') as fd:
        fd.write(rec)

    print ("sleep(120)\n")
    time.sleep(120)
