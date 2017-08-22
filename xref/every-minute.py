#!/usr/bin/python

import sys
import datetime
import time
import dateutil.parser
import csv

macMap = {}
macMapSignal = {}
daily = []
weekly = []

hourly = []
currentSlice = False
tslice = 60
RSS_CUTOFF = -80

def tots(what):
    return datetime.datetime.fromtimestamp(what).strftime('%d %H:%M')

def sigdistrib(hourly, cutoff, macMap, macAvg):
    step = 5
    max = 110
    sys.stdout.write("         ")
    for i in xrange(0, max, step):
       sys.stdout.write("%4d " % i)
    
    sys.stdout.write("\n")

    for hour in hourly:
        sys.stdout.write("%s " % tots(hour[0]))
        for i in xrange(1, max, step):
            frequent = filter(lambda x: macMap[x] > i and macAvg[x] > cutoff, hour[2])
            sys.stdout.write("%4d " % len(frequent))

        sys.stdout.write("\n")

with open(sys.argv[1]) as f:
    data = f.readlines()
    content = [ line.strip().split('\t') for line in data ]
    lastTime = False
    for row in content:
        try:
            timeStr, mac, sig = row
            timeInt = int(timeStr)
            sig = int(sig)
        except:
            continue

        if lastTime and timeInt < lastTime:
            continue

        if sig > -1:
            continue

        lastTime = timeInt
        if not currentSlice or timeInt > nextSlice:

            if not currentSlice:
                # if we havne't found the start hour, then we use the first time stamp we've received.
                hour, m, s = [int(x) for x in datetime.datetime.fromtimestamp(timeInt).strftime('%H %M %S').split(' ')]

                # we want to start the cycle at midnight so we take this time and back-date it to midnight
                currentSlice = timeInt 

                # This is our end-point
                nextSlice = currentSlice + tslice
                hourIx = 0
                sliceSet = set()

            while timeInt > nextSlice:
                # the hour, the total number of signals, the *unique* number of signals
                currentSlice = nextSlice
                nextSlice = currentSlice + tslice
                hourly.append([currentSlice, hourIx, sliceSet])

                hourIx = 0
                sliceSet = set()

        else:
            hourIx += 1
            sliceSet.add(mac)

        if not mac in macMap:
            macMap[mac] = 0
            macMapSignal[mac] = []

        if sig != -256:
            macMapSignal[mac].append(sig)

        macMap[mac] += 1
    
macAvg = {}

for mac, sigList in macMapSignal.iteritems():
    sample_size = len(sigList)
    if sample_size < 2:
        if len(sigList) > 0:
            macAvg[mac] = sigList[0]
        else:
            macAvg[mac] = -200
        continue

    sample_mean = sum(sigList) / sample_size
    numerator = sum([ (x - sample_mean)**2 for x in sigList ])
    variance = (numerator / (sample_size - 1)) ** 0.5
    macAvg[mac] = sample_mean
    #print sample_mean
    #print "%.2f" % variance, sample_mean, '*' * (max(sigList) - min(sigList))

sigdistrib(hourly, RSS_CUTOFF, macMap, macAvg)
