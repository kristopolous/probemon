#!/bin/bash
set -x
cd /var/log/probemon
dev=wlan8
#SRCHOME=/home/pi/probemon
SRCHOME=/home/chris/code/probemon
# service ifplugd stop

ifconfig $dev down
iwconfig $dev mode monitor
ifconfig $dev up

$SRCHOME/probemon.py -r -t unix -i $dev -o probemon-dev-0.log &

# /dev/urandom needs to "build up" entropy for uuidgen ...
# this is obscure, but true ... might as well give it some space.
if [ ! -e whoami ]; then
  uuidgen > whoami
fi

whoami=`cat whoami`

while [ 0 ]; do
  rsync -avzr /var/log/probemon/ chris@9ol.es:logs/$whoami
  sleep 10
  ntpdate pool.ntp.org

  sleep 30
  ntpdate pool.ntp.org

  sleep 590
done
