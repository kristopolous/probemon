#!/bin/sh
set -x
cp logrotate /etc/logrotate.d/probemon
cp initd /etc/init.d/probemon
update-rc.d probemon defaults
