#!/bin/bash
SRCHOME="$(dirname $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}"))"

if [ ! -e $SRCHOME/config.cfg ]; then
  echo "Create a config.cfg in $SRCHOME based off of config.cfg.example to set your own variables"
  exit -1
fi
. $SRCHOME/config.cfg

cd $LOGDIR

# We try to shutdown previous instances if applicable.
$SRCHOME/shutdown.sh

ifconfig $DEV down
iwconfig $DEV mode monitor
ifconfig $DEV up

# Try to update our time.  Things like Raspberry pi has
# drift that we need to account for.
if [ ! $NTPUPDATE ]; then 
  ret=1
  while [ $ret -ne "0" ]; do
    ntpdate pool.ntp.org
    ret=$?
    [ $ret ] || sleep 5
  done
fi

$SRCHOME/probemon.py -r -t unix -i $DEV -o probemon-dev-0.log &

if [ ! $SYNC ]; then
  # /dev/urandom needs to "build up" entropy for uuidgen ...
  # this is obscure, but true ... might as well give it some space.
  if [ ! -s whoami ]; then
    uuidgen > whoami
  fi

  whoami=`cat whoami`

  while [ 0 ]; do
    rsync -avzr $LOGDIR $SYNCHOST/$whoami
    sleep 600
  done
fi
