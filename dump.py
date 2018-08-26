#!/usr/bin/python3.5

import time
import pandas as pd


df = pd.read_csv("data.csv")

datetime = [ time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(_t)) for _t in df['time'] ]

for dt,odo,rng,bl in zip(datetime, df['odometer'], df['bat_range'], df['bat_level']):
    print ("{}: {}mi {:.2f} ({}%)".format(dt, odo, rng, bl))
