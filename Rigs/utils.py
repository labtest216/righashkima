#!/usr/bin/python
import smtplib, socket, time, os, signal
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import datetime


# Send mail.

def send_mail(sender_addr, sender_pass, notification_addr, subject, body, attach_file):
    toaddr = [elem.strip().split(',') for elem in notification_addr]
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
    server.login(sender_addr, sender_pass)
    server.sendmail(msg['From'], toaddr, msg.as_string())
    dprint('Send notification mail')
    server.quit()

# Debug printer.
def dprint(data_to_print):
    # os.system('echo ' + str(time()) + ' ' + str(data_to_print))
    print(str(time.time()) + " " + str(datetime.now()) + " " + data_to_print)

# Test net connection.
def connected():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname("www.google.com")
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        dprint('Test internet connection: PASS.')
        return True
    except:
        pass
        dprint('Test internet connection: FAIL.')
    return False

# Kill process.
def kill_proc(pid):
    dprint('Kill process '+str(pid))
    os.signal(pid, signal.SIGTERM)

