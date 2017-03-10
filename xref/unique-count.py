#!/usr/bin/python

import sys
import datetime
import time
import dateutil.parser
import csv

macMap = {}
daily = []
weekly = []

hourly = []
currentHour = False
factor = 6
tslice = 10 * 60


def tots(what):
    return datetime.datetime.fromtimestamp(what).strftime('%d %H:%M')

def usage(start, stop):
    print start, stop
    history = sys.argv[2]
    timeMap = {}
    tsList = []
    with open(history, 'rb') as csvfile:
        # we're going to get coupled start/end and then degrade the
        # time stamp to an hour.
        stream = csv.reader(csvfile, delimiter=',', quotechar='"')
        # these are in GMT time
        for row in stream:
            state, timeStr = row[2], row[11]
            timeInt = time.mktime(dateutil.parser.parse(timeStr).timetuple()) - 8 * 3600
            tsList.append([state, timeInt])

    tsPoint = 0
    if tsList[tsPoint][0] != 'start':
        tsPoint += 1 

    tsStart = tsList[tsPoint][1]
    tsEnd = tsList[tsPoint + 1][1]

    for ts in xrange(start, stop, 3600):
        timeMap[ts] = 0

        # This means that we started the ride before
        # the time stamp that we are looking at.
        if ts > tsStart:
            timeMap[ts] = 1

            # We ended the ride AFTER the time stamp
            # we are looking at.
            #if ts < tsEnd:

        if ts > tsEnd:
            # partial time is computed as follows:
            partial_time = ts - tsEnd - 3600

            if partial_time > 0:
                timeMap[ts] = 1

            tsPoint += 2 

            while tsList[tsPoint][0] != 'start' and tsPoint < len(tsList):
                tsPoint += 1 

            if tsPoint + 1 > len(tsList):
                break

            tsStart = tsList[tsPoint][1]
            tsEnd = tsList[tsPoint + 1][1]
            #print tots(tsStart), tots(tsEnd), (tsEnd - tsStart) / 3600

    return timeMap

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

        if timeInt > 2 ** 32:
            continue

        if lastTime and timeInt < lastTime:
            continue

        lastTime = timeInt
        if not currentHour or timeInt > nextHour:

            if not currentHour:

                # if we havne't found the start hour, then we use the first time stamp we've received.
                hour, m, s = [int(x) for x in datetime.datetime.fromtimestamp(timeInt).strftime('%H %M %S').split(' ')]

                # we want to start the cycle at midnight so we take this time and back-date it to midnight
                currentHour = timeInt - (hour * 3600 + m * 60 + s)

                # This is our end-point
                nextHour = currentHour + tslice
                hourIx = 0
                hourSet = set()

            while timeInt > nextHour:
                # the hour, the total number of signals, the *unique* number of signals
                currentHour = nextHour
                nextHour = currentHour + tslice
                hourly.append([currentHour, hourIx, len(hourSet), hourSet])

                hourIx = 0
                hourSet = set()

        else:
            hourIx += 1
            hourSet.add(mac)

        if not mac in macMap:
            macMap[mac] = 0
        macMap[mac] += 1
    
    ix = 0
    ttl = 0
    freq = 0
    starthour = hourly[0][0]
    dailyList = []
    impressionTTL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
    dayCount = 0

    hourwrap = int(datetime.datetime.fromtimestamp(starthour).strftime('%H'))

    for hour in hourly:
        ix += 1
        ts = hour[0]

        #sys.stdout.write("%4d%s" % (hour[2], inride))
        #sys.stdout.write("%s" % inride)
        ttl += hour[2]

        if hour[2] > 5:
            freq += 1

        dailyList = dailyList + list(hour[3])

        if ix % (24 * 6) == 0:
            dayCount += 1
            if freq == 0:
                freq = 1

            dailyList = set(dailyList)
            for iy in xrange(0, 10): 
                counted = filter(lambda x: macMap[x] > iy, dailyList)
                impressionTTL[iy] += len(counted)

            print " %3d %s" % ( len(dailyList), datetime.datetime.fromtimestamp(hour[0]).strftime('%a %m-%d %H') )
            dailyList = []
            ttl = 0
            freq = 0
            starthour = hour[0]


    print " %s" % datetime.datetime.fromtimestamp(starthour).strftime('%a %m-%d')

    print
    print impressionTTL, dayCount
    print [ 3 * (365/12) * (x / 46) for x in impressionTTL ], dayCount
    print len(macMap)
