import time
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
BAT_MIN=30

def plot_it():
    df = pd.read_csv('data.csv')
    df
    t = df['time']
    t = (t-t[0])/1e5
    y = df['bat_range']
    z = np.polyfit(t,y,1)
    print ("long-term", z) 
    yfit = np.poly1d(z)
    tt = np.linspace(min(t),100,num=100)
    yy = yfit(tt)
    fig,ax = plt.subplots(2, figsize=(16,12))
    xlim=[0,30]
    #xlim=[7.9,max(t)+0.05]
    p=0
    ax[p].plot(t, df['bat_range'], '.', ms=10, label='data')
    ax[p].plot(tt, yy, 'r', alpha=0.50, label='long-term')
    t2=np.array(t[4:])
    y2=np.array(y[4:])
    z = np.polyfit(t2,y2,1)
    print ("short-term", z)
    yfit = np.poly1d(z)
    tt = np.linspace(0,100,num=100)
    yy = yfit(tt)
    ax[p].plot(tt,yy,'b',alpha=0.50,label='short-term')
    ax[p].legend(loc='upper right', fontsize=14)
    ax[p].set_xlabel('DAYS')
    ax[p].set_ylabel('BATTERY_RANGE (mile)')
    ax[p].fill_between([0,100],0,BAT_MIN,color='r',alpha=0.3)
    ax[p].set_xlim(xlim)
    ax[p].set_ylim([0, 160])
    ax[p].grid()
    p+=1
    ax[p].plot(t,df['temp_in'],'-o',label="inside")
    ax[p].plot(t,df['temp_out'],'-o',label="outside")
    ax[p].fill_between(t,0,df['temp_in']-df['temp_out'],color='r',alpha=0.5,label="difference")
    ax[p].legend(loc='upper right', fontsize=14)
    ax[p].set_xlabel('DAYS')
    ax[p].set_ylabel('TEMPERATURE (degC)')
    ax[p].set_xlim([t[6], max(t)])
    ax[p].set_ylim([0, 60])
    ax[p].grid()
    fig.savefig('data.png')
