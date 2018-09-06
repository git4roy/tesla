#!/usr/bin/python3.5
with open("smon.csv", "r") as fi, open("smon2.csv","w") as fo:
    line0=fi.readline()
    fo.write(line0)
    for line in fi:
        if line.split(',')[-1]!=line0.split(',')[-1]:
            fo.write(line)
        line0=line
