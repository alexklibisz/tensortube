#!/bin/sh
# Add this to /etc/rc.local on a python server.
# cd /path/to/app
# ./start.sh
nohup python server/main.py > logging.out
