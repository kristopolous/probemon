#!/bin/bash
cd /var/log/probemon
dev=wlan0
SRCHOME=/home/pi/probemon
#SRCHOME=/home/chris/code/probemon
# service ifplugd stop

ifconfig $dev down
iwconfig $dev mode monitor
ifconfig $dev up

ret=1
while [ $ret -ne "0" ]; do
  ntpdate pool.ntp.org
  ret=$?
  [ $ret ] || sleep 5
done

$SRCHOME/probemon.py -r -t unix -i $dev -o probemon-dev-0.log &
#ssh -NR 9ol.es:7000:localhost:22 chris@9ol.es&
#service ssh start

# /dev/urandom needs to "build up" entropy for uuidgen ...
# this is obscure, but true ... might as well give it some space.
if [ ! -s whoami ]; then
  uuidgen > whoami
fi

whoami=`cat whoami`

while [ 0 ]; do
  rsync -avzr /var/log/probemon/ chris@9ol.es:logs/$whoami
  sleep 600
done
