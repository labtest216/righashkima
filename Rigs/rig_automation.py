#!/usr/bin/python
import json, os, schedule, time
from utils import connected, send_mail, kill_proc, dprint
from shutil import copyfile
from datetime import timedelta


class Rig:
    # Fields
    rig_mail_addr = "rigautolog@gmail.com"
    rig_mail_pass = "rigautologpass"
    script_dir = str(os.path.dirname(os.path.realpath(__file__)))
    stats_file = script_dir + '/gpu.txt'
    cfg_file = script_dir + '/RigAutoConfig'

    # Constractor.
    def __init__(self):
        self.rig_up_time = 0
        self.rig_hash = 0
        self.rig_name = ""
        self.num_of_gpu = ""
        self.coin = ""
        self.rig_min_hash = self.get_min_hash()
        # Get notification addresses.
        self.notification_addr = self.config_file("NotificationAddr", "get").split(',')
        # Enable notification.
        self.config_file("NotificationEnable", "true")
        # Init min rig hash.
        dprint("Coin=" + self.coin + " NumOfGpu=" + self.num_of_gpu + " " + "RigMinHash=" + str(self.rig_min_hash))

    # Properties.

    # Methods.

    # Copy and replace local.conf to soft/hard oc depend rig status fail/pass.
    def load_oc_config(self, coin, oc_type):
        try:
            copyfile('./' + str(coin) + '/' + str(oc_type) + '/local.conf', './')
            os.system('ethos-overclock')
        except IOError:
            self.send_mail(self.notification_add, 'load_oc_config fail')
            dprint('load_oc_config fail')

    # Get or set parameters in json file rig configuration.
    def config_file(self, key, value):
        json_file = open(self.cfg_file, "r+")
        data = json.load(json_file)
        try:
            if value == 'get':  # Get value.
                return str(data[str(key)])
            else:  # Set value.
                data[str(key)] = str(value)
                json_file.seek(0)  # rewind
                json.dump(data, json_file, sort_keys=True, indent=4)
                json_file.truncate()
        except:
            dprint("Can not set value on cfg file.")

    # Get rig statistics and gpu status to file.
    def get_stats(self):
        os.system('date > '+str(self.stats_file))
        time.sleep(1)
        try:
            dprint("Get stats file")
            os.system('/opt/ethos/bin/stats >>'+str(self.stats_file))
        except:
            dprint('can not add stats to file')
            time.sleep(5)

    def reset_rig(self):
        if self.config_file("RigResetWhenGpuFail", "get") == "true":
            dprint("Reset rig, RIG UP TIME was "+str(self.rig_up_time))
            time.sleep(1)
            # Ethos reset.
            os.system('/opt/ethos/bin/r')
            # Ubuntu reset just in case.
            time.sleep(5)
            os.system('sudo reboot')
        else:
            dprint("Can not reset rig, check RigResetWhenGpuFail fleg")

    # Event every 1 hours check gpu's status.
    def check_rig_status(self):
        # schedule.every(5).hours.do(self.rig_schedule_task)
	schedule.every(10).minutes.do(self.rig_schedule_task)
        # schedule.every(2).seconds.do(self.rig_schedule_task)
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Get GPU status and rig hash from stats file.
    def get_rig_fields_from_stats_file(self):
        # Get stats file.
        self.get_stats()
        # Get rig hash.
        try:
            self.rig_hash = int(float(self.get_string_from_file(self.stats_file, "hash:", "miner:")))
            if self.rig_hash == "":
                dprint("Can not get rig hash from file.")
            # Get rig up time.
            sec = timedelta(seconds=int(self.get_string_from_file(self.stats_file, "uptime:", "mac:")))
            self.rig_up_time = str(sec)
            # Get rig name.
            self.rig_name = self.get_string_from_file(self.stats_file, "hostname:", "ip:")
        except:
            dprint("Can not get rig fields from stats file.")

    def rig_schedule_task(self):
        # Check if enable or disable script.
        if self.config_file("ScriptEnable", "get") != "true":
            kill_proc(os.getppid())
        else:
            # Check net connection, power off the rig if connection fail and fleg is true.
            if not connected():
                dprint("Internet connection fail, rig will power off, " + str(self.rig_up_time))
                if self.config_file("RigOffWhenConnectionFail", "get") == "true":
                    # Ethos shoutdown
                    os.system("sudo poweroff")
                else:
                    dprint("Can not power off rig, check RigOffWhenConnectionFail fleg")
            else:  # Send notification mail, reset rig if gpu fail and flegs are true.
                self.get_rig_fields_from_stats_file()
                self.rig_min_hash = self.get_min_hash()
                if int(self.rig_min_hash) > int(self.rig_hash):
                    dprint("RigName=" + self.rig_name + " RigMinHash=" + str(self.rig_min_hash) + " RigHash=" + str(
                        self.rig_hash) + " HASH TEST FAIL.")
                    if self.config_file("NotificationEnable", "get") == "true":
                        subject = "Rig name=" + str(self.rig_name) + " Rig hash=" + str(self.rig_hash) + " Rig up time=" + str(self.rig_up_time)
                        send_mail(self.rig_mail_addr, self.rig_mail_pass, self.notification_addr, subject, "Rig just reset: " + str(self.rig_up_time), str(self.stats_file))
                    else:
                        dprint("Can not send mail, check NotificationEnable fleg")
                    self.reset_rig()
                else:
                    dprint("RigName=" + self.rig_name + " RigMinHash=" + str(self.rig_min_hash) + " RigHash=" + str(self.rig_hash) + " HASH TEST PASS.")

    def get_min_hash(self):
        self.coin = self.config_file("NowMiningCoin", "get")
        self.num_of_gpu = self.config_file("NumOfGpus", "get")
        if self.coin == "ZEC":
            self.rig_min_hash = 420 * int(self.num_of_gpu)
        elif self.coin == "ETH" or self.coin == "ETC":
            self.rig_min_hash = 26 * int(self.num_of_gpu)
        else:
            dprint("Can not init rig min hash.")
        return self.rig_min_hash

    def get_string_from_file(self, file, start_str, end_str):
        f = open(file, 'r').read()
        start = f.find('\n' + str(start_str)) + len(start_str) + 1
        end = f.find('\n' + str(end_str))
        line = f[start:end]
        line = line.replace(" ", "")
        return line

