#!/usr/bin/python
import time
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def save_hist(filename, dict_list, field):
    fig,ax = plt.subplots(1, figsize=(16,6))
    y=[]
    t=[]
    for _dict in dict_list:
        d=_dict[field]
        if d!='None':
            y.append(d)
            t.append(_dict['timestamp']/float(1000))

    datetime=time.ctime(t[-1])
    t=np.array(t)/3600
    hrs = np.zeros(32)

    for t1,t2,y1,y2 in zip(t[:-1],t[1:],y[:-1],y[1:]):
        my=(y1+y2)/2
        dt=t2-t1
        hrs[int(my/10)]+=dt

    x=[n_ for n_ in range(0,320,10)]
    ypos=[n_ for n_ in range(len(hrs))]

    ax.bar(ypos,hrs,align='center') 
    ax.set_xticklabels(x)
    ax.set_xticks(ypos)
    
    y=np.array(hrs).cumsum()
    y/=y[-1]
    y*=100
    ax2 = ax.twinx()
    ax2.plot(ypos,y,'k-',linewidth=1.5)

    ax.set_xlabel('BATTERY RANGE (mile)')
    ax.set_ylabel('HOURS')
    ax2.set_ylabel('DISTRIBUTION (%)')
    ax2.grid(True)
    ax.set_title('Total Time={:.1f} days ({:.1f} hours), Updated Time={}'.format(sum(hrs)/24,sum(hrs),datetime))

    fig.savefig('/var/www/html/{}_hist'.format(filename))

def save_png(filename, dict_list, *fields, **kwargs):
    fig,ax = plt.subplots(1, figsize=(16,6))
  
    t=[]
    for _dict in dict_list:
        t.append(_dict['timestamp']/1000.0)
    datetime=time.ctime(int(list(t)[-1]))
   
    t = np.array(t)/3600

    if 'last24hr' in kwargs:
        if kwargs['last24hr']:
            mask=t>(t[-1]-24)
            t=t[mask]
    t = t-t[0]

    data=[]
   
    for field in fields:
        y=[]
        for _dict in dict_list:
            d=_dict[field]
            if d=='None':
                y.append(0)
            else:
                y.append(_dict[field])
        data.append(str(y[-1]))
        y=np.array(y)
        if 'last24hr' in kwargs:
            if kwargs['last24hr']:
                y=y[mask]
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
    with open("mon.data", "r") as fd:
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
    save_png('range1', chg, 'battery_range', last24hr=True)
    save_png('temp', cli, 'inside_temp', 'outside_temp')
    save_png('temp1', cli, 'inside_temp', 'outside_temp', last24hr=True)
    save_png('odo', veh, 'odometer')
    save_png('speed', dri, 'speed')
    save_hist('range', chg, 'battery_range')
