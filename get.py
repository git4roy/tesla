#! /usr/bin/python3.5
import time
import json
import api
import plot

SAMPLE_TIME_IN_MIN=60*2

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

for retry in range(20):
    try:
        v.wake_up()
        time.sleep(1)
        
        vehicle_state = v.data_request('vehicle_state')
        save_data("veh_{}".format(vehicle_state['timestamp']), vehicle_state)
        
        charge_state = v.data_request('charge_state')
        save_data("cha_{}".format(charge_state['timestamp']), vehicle_state)
        
        climate_state = v.data_request('climate_state')
        save_data("cli_{}".format(climate_state['timestamp']), vehicle_state)

        odo = vehicle_state['odometer']
        ts = charge_state['timestamp']
        bat_rng = charge_state['battery_range']
        bat_lvl = charge_state['battery_level']
        tmp_in =  climate_state['inside_temp']
        
        for i in range(10):
            tmp_in_2 = v.data_request('climate_state')['inside_temp']
            if abs(tmp_in-tmp_in_2)<1:
                break
            tmp_in = tmp_in_2
         
        tmp_out = climate_state['outside_temp']

        with open("data.csv", "a") as fd: 
            fd.write("{},{},{},{},{},{}\n".format(
                time.time(), odo, bat_rng, bat_lvl, tmp_in, tmp_out))

        with open("data2.csv", "a") as fd:
            fd.write("{},{},{},{},{},{}\n".format(
                ts, odo, bat_rng, bat_lvl, tmp_in, tmp_out))

        print (ts, odo, bat_rng, bat_lvl, tmp_in, tmp_out)
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

plot.plot_it('data.csv')
plot.plot_it("data2.csv")
