#!/bin/bash
set -x
cd /var/log/probemon
# service ifplugd stop

dev=wlan0
ifconfig $dev down
iwconfig $dev mode monitor
ifconfig $dev up
/home/pi/probemon/probemon.py -r -t unix -i $dev -o probemon-dev-0.log &

while [ 0 ]; do
  scp -C /var/log/probemon/probemon-dev-0.log chris@9ol.es:logs/
  sleep 10
  ntpdate pool.ntp.org

  sleep 30
  ntpdate pool.ntp.org

  sleep 590
done
