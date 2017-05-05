#!/usr/bin/python

import time
import datetime
import argparse
import netaddr
import sys
import logging
import os
import uuid
from multiprocessing import Process, Queue
from scapy.sendrecv import sniff
from scapy.layers import dot11
from pprint import pprint

NAME = 'probemon'
DESCRIPTION = "a command line tool for logging 802.11 probe request frames"

def build_packet_callback(time_fmt, output, delimiter, mac_info, ssid, rssi):
	def packet_callback(packet):
		if not packet.haslayer(dot11.Dot11):
			return

		# we are looking for management frames with a probe subtype
		# if neither match we are done here
		if packet.type != 0 or packet.subtype != 0x04:
			return

		# list of output fields
		fields = []

		# determine preferred time format 
		log_time = str(int(time.time()))
		if time_fmt == 'iso':
			log_time = datetime.datetime.now().isoformat()

		fields.append(log_time)

		# append the mac address itself
		fields.append(packet.addr2)

		# include the SSID in the probe frame
		if ssid:
			fields.append(packet.info)
			
		if rssi:
			rssi_val = -(256-ord(packet.notdecoded[-4:-3]))
			fields.append(str(rssi_val))

                q.put(delimiter.join(fields))

	return packet_callback

def writer(q, fname):
    while True:
        line = q.get()
        # This is to avoid file corruption on reboot
        fd = os.open(fname, os.O_WRONLY | os.O_APPEND | os.O_SYNC | os.O_CREAT)
        os.write(fd, line + "\n")
        os.close(fd)

def sniff_wrap(iface, prn, store):
    while True:
        try:
            sniff(iface=iface, prn=prn, store=store)
        except:
            pass

def main():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument('-i', '--interface', help="capture interface")
	parser.add_argument('-t', '--time', default='iso', help="output time format (unix, iso)")
	parser.add_argument('-o', '--output', default='probemon.log', help="logging output location")
	parser.add_argument('-d', '--delimiter', default='\t', help="output field delimiter")
	parser.add_argument('-f', '--mac-info', action='store_true', help="include MAC address manufacturer")
	parser.add_argument('-s', '--ssid', action='store_true', help="include probe SSID in output")
	parser.add_argument('-r', '--rssi', action='store_true', help="include rssi in output")
	args = parser.parse_args()

	if not args.interface:
	    print "error: capture interface not given, try --help"
	    sys.exit(-1)
	
	built_packet_cb = build_packet_callback(args.time, args.output, 
		args.delimiter, args.mac_info, args.ssid, args.rssi)

        # Start the sniffer and hb writer
        Process(target = writer, args=(q,args.output)).start()
        Process(target = sniff_wrap, args=(args.interface, built_packet_cb, 0)).start()

        counter = 0
        instance = str(uuid.uuid4())
        while True:
            q.put(args.delimiter.join([str(int(time.time())), instance, str(counter)]))
            counter += 1
            time.sleep(10)

if __name__ == '__main__':
        q = Queue()
	main()
