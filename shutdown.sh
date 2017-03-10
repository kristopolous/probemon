#!/bin/bash
pslist=`pgrep probemon`
[ -n "$pslist" ] && kill $pslist
