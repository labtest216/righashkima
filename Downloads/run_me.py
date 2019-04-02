#!/usr/bin/python

# this script will:
# 1. Edit lines on /etc/rc.local to run on boot schedule scripts .
# 2. Script Logs will print to /tmp/rc.local.log .
# 3. Run pip install schedule .

# exec 2> /tmp/rc.local.log      # send stderr from rc.local to a log file
# exec 1>&2                      # send stdout to the same log file
# set -x                         # tell sh to display commands before execution
# sleep 50
# /home/ethos/RigAuto/Main.py



import os
import time

script_dir = str(os.path.dirname(os.path.realpath(__file__)))

os.system('pip install schedule')
time.sleep(5)

os.system('echo "#!/bin/sh -e" > /etc/rc.local')
os.system('echo "PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin" >> /etc/rc.local')

os.system('echo "exec 2> /tmp/rc.local.log" >> /etc/rc.local')
os.system('echo "exec 1>&2" >> /etc/rc.local')
os.system('echo "set -x" >> /etc/rc.local')
os.system('echo "sleep 50" >> /etc/rc.local')


os.system('echo ' +str(script_dir)+'"/Main.py" >> /etc/rc.local')
os.system('echo "exit 0" >> /etc/rc.local')


