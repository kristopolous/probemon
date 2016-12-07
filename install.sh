#!/bin/sh
set -x
mkdir -p /var/log/probemon
cp configs/logrotate /etc/logrotate.d/probemon
cp configs/initd /etc/init.d/probemon
sudo chmod 0700 /etc/init.d/probemon
update-rc.d probemon defaults
