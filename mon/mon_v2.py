#! /usr/bin/python3.5
import time
import json,csv
import api

def go_sleep(sec):
    for d in range(sec):
        with open('/tmp/mon','w') as fd:
            fd.write("{}/{}".format(d,sec))
        time.sleep(1)

def save_dict(csv_file,newdata):
    data=[]
    with open(csv_file,'r') as fi:
        reader=csv.DictReader(fi)
        for row in reader:
           data.append(row) 
    data.append(newdata) 
    with open(csv_file,'w') as fo:
        writer=csv.DictWriter(fo,newdata.keys())
        writer.writeheader()
        for d in data:
            writer.writerow(d)

with open('../../access_token','r') as fd:
    access_token=fd.readline()

c = api.Connection(access_token)
v = c.vehicles[0]

if v['state']!='online':
    c.close()
    exit()

for retry in range(10):
    if True:
        v.wake_up()
        time.sleep(1)
        
        save_dict('vehicle.csv', v.data_request('vehicle_state'))
        save_dict('charge.csv', v.data_request('charge_state'))
        save_dict('climate.csv',v.data_request('climate_state'))
        save_dict('drive.csv',v.data_request('drive_state'))
        break

    if False:
        print ("Error requestin data...retry={}".format(retry))
        time.sleep(3)
        continue

for _ in range(10):
    try:
        v.close()
        break
    except:
        continue
