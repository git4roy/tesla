#!/usr/bin/python
import time
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def save_png(filename, dict_list, *fields):
    fig,ax = plt.subplots(1, figsize=(16,6))
  
    t=[]
    for _dict in dict_list:
        t.append(_dict['timestamp']/1000.0)
    datetime=time.ctime(int(list(t)[-1]))
    
    t = [(_t-t[0])/3600 for _t in t]

    data=[]
   
    for field in fields:
        y=[]
        for _dict in dict_list:
            d=_dict[field]
            if d=='None':
                y.append(9)
            else:
                y.append(_dict[field])
        data.append(str(y[-1]))
        ax.plot(t, y, '-o', label=field)
    
    ax.set_title("Updated Time: {}, Latest Data: {}".format(datetime,", ".join(data)))
    ax.set_xlabel('HOURS')
    ax.legend()
    ax.grid()
    
    fig.savefig('/var/www/html/{}'.format(filename))

if __name__=='__main__':
    veh=[]
    chg=[]
    cli=[]
    dri=[]
    with open("mon.csv", "r") as fd:
        for line in fd:
            s = line.split('=')
            if s[0]=='veh':
                veh.append(json.loads(s[1]))
            elif s[0]=='cli':
                cli.append(json.loads(s[1]))
            elif s[0]=='chg':
                chg.append(json.loads(s[1]))
            elif s[0]=='dri':
                dri.append(json.loads(s[1]))
    save_png('range', chg, 'battery_range')
    save_png('temp', cli, 'inside_temp', 'outside_temp')
    save_png('odo', veh, 'odometer')
    save_png('speed', dri, 'speed')
