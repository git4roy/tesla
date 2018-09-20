import numpy as np
import json, csv

def saveCsv(json_file, csv_file, tag):
    with open(json_file, 'r') as fi:
        data=[]
        for line in fi:
            s=line.split('=')
            if s[0]==tag:
                data.append(json.loads(s[1]))
    with open(csv_file,'w') as fo:
        w=csv.DictWriter(fo, data[0].keys())
        w.writeheader()
        for d in data:
            w.writerow(d)


saveCsv('mon.data','vehicle.csv','veh')
saveCsv('mon.data','drive.csv','dri')
saveCsv('mon.data','climate.csv','cli')
saveCsv('mon.data','charge.csv','chg')
