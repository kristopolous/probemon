# probemon

Reqs: uuid-runtime and rsync

This is a fork from Nik Harris.  The changes:

  * A 10 second, incrementing, uuid based heartbeat has been added to the logs to be able to differentiate whether the software was recording 0 for an interval of time, or whether it was not running at all.
  * The logs are written synchronously to avoid file corruption if power is cut.
  * There's a startup script (see config.cfg) that 
    * tries to synchronize the system clock prior to running
    * tries to rsync the logs to a remote server

The original readme:

A simple command line tool for monitoring and logging 802.11 probe frames

I decided to build this simple python script using scapy so that I could record 802.11 probe frames over a long period of time. This was specifically useful in my use case: proving that a person or device was present at a given location at a given time.

## Usage

```
usage: probemon.py [-h] [-i INTERFACE] [-t TIME] [-o OUTPUT] 
                   [-d DELIMITER] [-s]

a command line tool for logging 802.11 probe request frames

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        capture interface
  -t TIME, --time TIME  output time format (unix, iso)
  -o OUTPUT, --output OUTPUT
                        logging output location
  -d DELIMITER, --delimiter DELIMITER
                        output field delimiter
  -s, --ssid            include probe SSID in output
```

