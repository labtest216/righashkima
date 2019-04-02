#!/usr/bin/python

# 1. Edit this  lines on /etc/rc.local (without #), this script will run on boot
# 2. Logs will print to /tmp/rc.local.log
# 3. Run pip install schedule

# exec 2> /tmp/rc.local.log      # send stderr from rc.local to a log file
# exec 1>&2                      # send stdout to the same log file
# set -x                         # tell sh to display commands before execution
# sleep 50
# /home/gil/RigAuto/Main.py




import RigAutomation

RigAutomation.Rig().send_gpu_stats_mail_schedule()
