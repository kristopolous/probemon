#!/bin/sh
cd /var/log/probemon
# service ifplugd stop

dev=wlan0
ifconfig $dev down
iwconfig $dev mode monitor
ifconfig $dev up
exec /home/pi/probemon/probemon.py -r -t unix -i $dev -o probemon-dev-0.log 
