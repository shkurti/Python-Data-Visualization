#!/usr/bin/env python -W ignore::DeprecationWarning
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import csv
import time
from collections import namedtuple
print ("Preparing map...")	
m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='c')
print ("Done...")
stations = []
# Stations : "usaf-wban", "lat", "lon"
print ("Preparing stations...")
with open("stations.csv", "r")    as scoreFile:
    scoreFileReader = csv.reader(scoreFile, delimiter=",")
    for row in scoreFileReader:
        if row[6]!="" and row[7] != "":
			
            stations.append([row[0]+row[1],row[6],row[7]])
stations = stations[1:]
print ("Done...")
values = namedtuple('values', 'lon lat temp')
temp=[]
tmpval = []
days = []
print ("Preparing temperatures...")
# Temperature Values : "usaf-wban", "day", "month", "temp"
with open("2000.csv", "r") as tempfile:
	tempreader = csv.reader(tempfile, delimiter=",")
	for row in tempreader:
		if row[5]!="":
			temp.append([row[0]+row[1],row[4],row[3],row[5]])
			days.append(row[4]+"."+row[3])
temp = temp[1:]
print ("Done...")
for i in range(len(temp)):
	tmpval.append(float(temp[i][3]))
tempmax = max(tmpval)
tempmin = min(tmpval)
for j in range(12):
	if j+1 < 10:
		chk2 = "0"+str(j+1)
	else:
		chk2 = str(j+1)
	for i in range(31):
		if i+1 < 10:
			chk1 = "0"+str(i+1)
		else:
			chk1 = str(i+1)
		cntval = days.count(chk1+"."+chk2)
		print (str(cntval) + " datas exist in " + chk1 + "/" + chk2 + "/2000. Processing...")
		if cntval != 0:
			x = []
			y = []
			t = []
			seritemp = []
			seritemp = [[serial,tmpval1] for (serial,day,month,tmpval1) in temp if int(day) == i+1 and int(month) == j+1]
			for index1, item in enumerate(seritemp):
				tmp = float(item[1])
				st = item[0]
				if len(st) < 11:
					st = "0" + st
				res = [[lon,lat,tmp] for (serial,lat,lon) in stations if serial == st]
				if len(res) == 1:
					x.append(float(res[0][0]))
					y.append(float(res[0][1]))
					t.append(float(res[0][2]))
			plt.clf()
			m.drawcountries()
			m.drawstates()
			m.bluemarble()
			x1,y1 = m(x,y)
			color_by = t
			scat = plt.scatter(x1,y1,c=t,s=2,marker='.',cmap=plt.cm.jet, vmin=tempmin, vmax = tempmax)
			plt.title(chk2+"/"+chk1+"/2000")
			plt.draw()
			plt.savefig("map{}.png".format(i),dpi=300)

