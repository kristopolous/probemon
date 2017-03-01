#!/usr/bin/python

import sys
import datetime

macMap = {}
daily = []
weekly = []

hourly = []
offset = 8 * 3600
RSS_cutoff = -80
currentHour = False

with open(sys.argv[1]) as f:
    data = f.readlines()
    content = [ line.strip().split('\t') for line in data ]
    for row in content:
        try:
            time, mac, sig = row
            time = int(time)# - offset
            sig = int(sig)
        except:
            continue

        if time > 2 ** 32:
            continue

        if sig < RSS_cutoff:
            continue

        if not currentHour or time > nextHour:

            if not currentHour:
                hour, m = [int(x) for x in datetime.datetime.fromtimestamp(time).strftime('%H %M').split(' ')]
                currentHour = time - (hour * 3600 + m * 60)
                nextHour = currentHour + 60 * 60
                hourIx = 0
                hourSet = set()

            while time > nextHour:
                hourly.append([currentHour, hourIx, len(hourSet)])
                currentHour = nextHour
                nextHour = currentHour + 60 * 60
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
    hourwrap = int(datetime.datetime.fromtimestamp(starthour).strftime('%H'))
    for i in xrange(0, 24):
        sys.stdout.write("%4d" % ((i + hourwrap) % 24))
    print

    for hour in hourly:
        ix += 1
        sys.stdout.write("%4d" % hour[2])
        ttl += hour[2]

        if hour[2] > 5:
            freq += 1

        if ix % 24 == 0:
            if freq == 0:
                freq = 1

            print " %3d %s" % ( ttl / freq, datetime.datetime.fromtimestamp(starthour).strftime('%a %m-%d %H:%M') )
            ttl = 0
            freq = 0
            starthour = hour[0]

    while ix % 24 != 0:
        ix += 1
        sys.stdout.write("%4d" % 0)

    print " %s" % datetime.datetime.fromtimestamp(starthour).strftime('%a %m-%d')

    for i in xrange(0, 24):
        sys.stdout.write("%4d" % ((i + hourwrap) % 24))
    print
    print len(macMap)
