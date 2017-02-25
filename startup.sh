#!/bin/bash
pwd=$PWD
cd /var/log/probemon
#service ifplugd stop
set -x

for id in 1 6 7 ; do
	dev=wlan$id
	ifconfig $dev down
	iwconfig $dev mode monitor
	ifconfig $dev up
	$pwd/probemon.py -r -t unix -i $dev -o probemon-dev-$id.log &
done
