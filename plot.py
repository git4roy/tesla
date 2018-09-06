import time
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
BAT_MIN=30

def plot_it(filename):
    fig,ax = plt.subplots(2, figsize=(16,12))
    df = pd.read_csv(filename)
    
    t = df['time']
    datetime=time.ctime(int(list(t)[-1]/1000))
    print(datetime)
    t = (t-t[0])/1e5
    is_new = filename.split('.')[0][-1]=='2'
    if is_new:
        t=t/1000
    y = df['bat_range']
    z = np.polyfit(t,y,1)
    #print ("long-term", z) 
    #yfit = np.poly1d(z)
    #if is_new:
    #    tt = np.linspace(min(t),14,num=100)
    #else:
    #    tt = np.linspace(min(t),max(t)*3,num=100)
    #yy = yfit(tt)
   
    p=0
    ax[p].plot(t, y, '-o', ms=10, label='data')
    #ax[p].plot(tt, yy, 'r', alpha=0.50, label='long-term')
    ax[p].set_xlim([0,max(t)])
    ax[p].set_ylim([0, int((max(y)+10)/10)*10])
  
    n=0
    #t2=np.array(t[n:])
    #y2=np.array(y[n:])
    #z = np.polyfit(t2,y2,1)
    #print ("short-term", z)
    #yfit = np.poly1d(z)
    #yy = yfit(tt)
   
    ax[p].set_title(datetime)
    #ax[p].plot(tt,yy,'b',alpha=0.50,label='short-term')
    #ax[p].legend(loc='upper right', fontsize=14)
    ax[p].set_xlabel('DAYS')
    ax[p].set_ylabel('BATTERY_RANGE (mile)')
    ax[p].fill_between([min(t),max(t)],0,BAT_MIN,color='r',alpha=0.3)
    ax[p].grid()
    
    p=1
    ax[p].plot(t,df['temp_in'],'-o',label="inside")
    ax[p].plot(t,df['temp_out'],'-o',label="outside")
    ax[p].fill_between(t,0,df['temp_in']-df['temp_out'],color='r',alpha=0.5,label="difference")
    ax[p].legend(loc='upper right', fontsize=14)
    ax[p].set_xlabel('DAYS')
    ax[p].set_ylabel('TEMPERATURE (degC)')
    ax[p].set_xlim([min(t), max(t)])
    ax[p].set_ylim([0, 60])
    ax[p].grid()
    
    fig.savefig('{}.png'.format(filename.split('.')[0]))

if __name__=='__main__':
    plot_it('data.csv')
    plot_it('data2.csv')
