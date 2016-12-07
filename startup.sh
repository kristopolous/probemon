#!/bin/sh
dev=wlan1
cd /var/log/probemon
service ifplugd stop
ifconfig $dev down
iwconfig $dev mode monitor
ifconfig $dev up
exec /home/pi/probemon/probemon.py -t unix -i $dev
