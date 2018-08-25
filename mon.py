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
if 1:
    while 1:
        for retry in range(20):
            try:
                v.wake_up()
                time.sleep(1)
                charge_state = v.data_request('charge_state')
                climate_state = v.data_request('climate_state')
                vehicle_state = v.data_request('vehicle_state')
                odo = vehicle_state['odometer']
                bat_rng = charge_state['battery_range']
                bat_lvl = charge_state['battery_level']
                tmp_in =  climate_state['inside_temp']
                for i in range(10):
                    tmp_in_2 = v.data_request('climate_state')['inside_temp']
                    if abs(tmp_in-tmp_in_2)<1:
                        break
                    tmp_in = tmp_in_2
                
                tmp_out = climate_state['outside_temp']
	        with open("data.csv","a") as fd:            
                    fd.write("{},{},{},{},{},{}\n".format(
                        time.time(), odo, bat_rng, bat_lvl, tmp_in, tmp_out))
                print (time.time(), odo, bat_rng, bat_lvl, tmp_in, tmp_out)
                break
            except:
                print ("Error requestin data...retry={}".format(retry))
                time.sleep(3)
                continue
        plot.plot_it()
        go_sleep(SAMPLE_TIME_IN_MIN*60)
