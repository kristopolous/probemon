#!/bin/sh
cd /var/log/probemon
# service ifplugd stop

for id in 0 1 2 ; do
	dev=wlan$id
	ifconfig $dev down
	iwconfig $dev mode monitor
	ifconfig $dev up
	/home/pi/probemon/probemon.py -r -t unix -i $dev -o probemon-dev-$id.log &
done
