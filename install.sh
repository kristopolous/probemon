#!/bin/sh
set -x
apt-get install -y python-netaddr python-scapy tcpdump
mkdir -p /var/log/probemon
cp configs/logrotate /etc/logrotate.d/probemon
cp configs/initd /etc/init.d/probemon
sudo chmod 0700 /etc/init.d/probemon
update-rc.d probemon defaults
