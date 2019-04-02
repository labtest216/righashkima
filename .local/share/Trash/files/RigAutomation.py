#!/usr/bin/python

import smtplib
import sched
import json
import time
import schedule
import os
from shutil import copyfile
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class Rig:
    script_dir = str(os.path.dirname(os.path.realpath(__file__)))
    status = False
    just_reset_fleg = False
    curent_mining_coin = 'null'
    # coins['ZEC', 'ETH', 'ETC', 'XMR']
    stats_file = script_dir + '/gpu.txt'
    cofig_file = script_dir + '/RigAutoConfig'
    notification_add = ['eshyazalame@gmail.com']
    soft_oc = 'Soft'
    hard_oc = 'Hard'
    rig_hash = 0.0
    gpu_fails = -1
    counter = 0
    
    # Copy and replace local.conf to soft/hard oc depend rig status fail/pass.
    def load_oc_config(self, coin, oc_type):
        try:
            copyfile('./'+str(coin)+'/'+str(oc_type)+'/local.conf', './')
            os.system('ethos-overclock')
        except IOError:
            self.send_mail(self.notification_add, 'load_oc_config fail')
            print('load_oc_config fail')

    #  Get or set parameters in jeson file rig configuration.
    def setget_rig_config_file(self, key, value):
        json_file = open(self.cofig_file, "r+")
        data = json.load(json_file)
        if(value == 'get'):
            return str(data[str(key)])
        else:
            data[str(key)] = str(value)
            json_file.seek(0)  # rewind
            json.dump(data, json_file, sort_keys=True, indent=4)
            json_file.truncate()

    # Get rig statistics and gpu status to file.
    def get_stats(self):
        os.system('date > '+str(self.stats_file))
	time.sleep(1)
	print('add date to file')
	try:
        	os.system('/opt/ethos/bin/stats >>'+str(self.stats_file))
	except:
		print('can not add stats to file')
	time.sleep(5)

    def reset_rig(self):
        self.setget_rig_config_file("RigJustReset", "True")
        self.setget_rig_config_file("Counter", str(self.counter))
        time.sleep(15)
	os.system('echo reset rig')
        #os.system('/opt/ethos/bin/r')
        os.system('reboot 5')
	
    def reset_counter(self):
        self.setget_rig_config_file("Counter", "0")

    @staticmethod
    def send_mail(self, notification_add, subject, body, attach_file):
        toaddr = [elem.strip().split(',') for elem in notification_add]
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = 'rigautolog@gmail.com'
        msg['Reply-to'] = 'rigautolog@gmail.com'
        msg.preamble = 'Multipart massage.\n'
        part = MIMEText(body)
        msg.attach(part)
        part = MIMEApplication(open(attach_file, "rb").read())
        part.add_header('Content-Disposition', 'attachment', filename=attach_file)
        msg.attach(part)
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login("rigautolog@gmail.com", "rigautologpass")
        server.sendmail(msg['From'], toaddr, msg.as_string())
        server.quit()

    # Event every 1 hours check gpu's status.
    def send_gpu_stats_mail_schedule(self):

        # schedule.every(1).hours.do(self.update_gpu_status)
        # schedule.every(30).minutes.do(self.update_gpu_status)
	schedule.every(50).seconds.do(self.update_gpu_status)
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Get GPU status and rig hash rate from stats file.
    def update_gpu_status(self):
        print(str(time.time())+" Cunter="+str(self.counter))
        self.get_stats()
        file = open(self.stats_file, 'r').read()
	if file.find('crashed_gpus:') != -1:
		start = file.find('\ncrashed_gpus:')+14
		end = file.find('\ngpus:')
		crashed_gpus_line = file[start:end]
		crashed_gpus_line = crashed_gpus_line.replace(" ", "")
		start = file.find('\nhash:') + 6
		end = file.find('\nminer:')
		hash_line = file[start:end]
		hash_line = hash_line.replace(" ", "")
		self.rig_hash = int(float(hash_line))
		self.gpu_fails = 0
		self.counter += 1
        	if crashed_gpus_line == "":
		    self.status = True
		    self.gpu_fails = 0
		    self.send_mail(self, self.notification_add, 'GPU PASS', 'Rig hash:' + str(self.rig_hash),str(self.stats_file))
		    print(str(self.gpu_fails) + ' GPU fails' + ' Rig hash=' + str(self.rig_hash))
		else:
		    self.status = False
		    self.gpu_fails = int(crashed_gpus_line)
		    print(str(self.gpu_fails) + ' GPU fails' + ' Rig hash=' + str(self.rig_hash))
		    self.send_mail(self, self.notification_add, 'GPU FAIL', 'Rig hash:' + str(self.rig_hash), str(self.stats_file))
		    self.reset_rig()
	else:
		self.send_mail(self, self.notification_add, 'Stats file not have gpu status', 'Rig hash:' + str(self.rig_hash), str(self.stats_file))
		os.system('Stats file not have gpu status')
