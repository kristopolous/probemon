#!/bin/bash
cd /var/log/probemon
dev=wlan0
SRCHOME=/home/pi/probemon
LOG=probemon-dev-0.log
#SRCHOME=/home/chris/code/probemon
# service ifplugd stop

ifconfig $dev down
iwconfig $dev mode monitor
ifconfig $dev up

# Try to sync with the NTP server
ret=1
attempts=20
while [ $ret -ne "0" -a $attempts -gt "0" ]; do
  ntpdate pool.ntp.org >& /dev/null
  ret=$?
  attempts=$(( attempts - 1 ))

  if [ $ret -ne "0" ]; then 
     echo -n $attempts" "
     sleep 5
  fi
done

# If this fails then we just push our timestamps 3
# minutes forward from the last recorded time. The 
# focus here is that we don't want overlap.  This
# policy may be (ok, it's very likely) incorrect
# but it's the best we can do
if [ $attempts -eq "0" -a -s $LOG ]; then
  lasttime=`tail -1 $LOG | awk ' { print $1 } '`
  newtime=$(( lasttime + 180 ))
  date -s @$newtime
fi
  
$SRCHOME/probemon.py -r -t unix -i $dev -o $LOG &

# /dev/urandom needs to "build up" entropy for uuidgen ...
# this is obscure, but true ... might as well give it some space.
if [ ! -s whoami ]; then
  uuidgen > whoami
fi

whoami=`cat whoami`

while [ 0 ]; do
  rsync -avzr /var/log/probemon/ chris@9ol.es:logs/$whoami

  sleep 600

  # If we're here this means that we initially timed out
  # in an attempt to find the network. More than likely the
  # rsync above totally failed. But we'll try in vain to
  # get the more accurate timestamp, hoping that eventually
  # we will see the internet again.
  if [ $attempts -eq "0" ]; then
    ntpdate pool.ntp.org >& /dev/null
  fi
done
