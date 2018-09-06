#! /usr/bin/python3.5
import time
import json
import api

def go_sleep(sec):
    for d in range(sec):
        with open('/tmp/mon','w') as fd:
            fd.write("{}/{}".format(d,sec))
        time.sleep(1)

def save_data(filename, data):
    with open("data/{}.json".format(filename), 'w') as fd:
        fd.write(json.dumps(data))

with open('../access_token','r') as fd:
    access_token=fd.readline()

c = api.Connection(access_token)
v = c.vehicles[0]

if v['state']!='online':
    v.close()
    exit()

for retry in range(10):
    try:
        v.wake_up()
        time.sleep(1)
        
        vehicle_state = v.data_request('vehicle_state')
        charge_state = v.data_request('charge_state')
        climate_state = v.data_request('climate_state')
        drive_state = v.data_request('drive_state')

        with open('mon.csv','a') as fd:
            fd.write('veh={}\n'.format(json.dumps(vehicle_state)))
            fd.write('chg={}\n'.format(json.dumps(charge_state)))
            fd.write('cli={}\n'.format(json.dumps(climate_state)))
            fd.write('dri={}\n'.format(json.dumps(drive_state)))
        break
    except:
        print ("Error requestin data...retry={}".format(retry))
        time.sleep(3)
        continue

for _ in range(10):
    try:
        v.close()
        break
    except:
        continue
