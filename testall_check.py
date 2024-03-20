#!/usr/local/anaconda/bin/python

# testall_check.py:
#   is called by testall_check.csh in crontab on vm-nires
#   and calls testAll.py to determine if there are any current errors for default instrument

# ToDo 3/19/24 (NIRES):
# x- add uptime to testall without IDL error (or will trigger email every 5 min when no actual error)
# x- fix IDL_DIR error ssh'ing to niresserver2
#   - fixed .cshrc on niresserver2; awaiting Percy's ok to keep (restore) it
#   x- add uptime results to message var
# x- add Percy to email list in cron
#   x- restore send_email() call logic
# - split testall into instruments and telescpe
#   - verify terminology and files with Jeff
# - restore is_instrument_available()
# - restore is_instrument_scheduled()
#   date = datetime.strftime(datetime.now().date(), '%Y-%m-%d')   # added
#   print(date)
# - restore error for uptime MISSING INFO (to reduce email)?

import argparse
from datetime import datetime
import os
import sys
import subprocess
import smtplib
from email.mime.text import MIMEText
import socket
from urllib.request import urlopen
import json
from subprocess import Popen, PIPE
import pdb

def send_email(recipients, message, error):
    errorMsg = 'ERROR: ' if error == 1 else ''
    msg = MIMEText(message)
    msg['Subject'] = f"{errorMsg}{instrument.upper()} RTI Alarm ({socket.gethostname()})"
    msg['To'] = recipients
    msg['From'] = 'koaadmin@keck.hawaii.edu'
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

def get_uptime(server_name):
    uptime_cmd = ["ssh", server_name, " uptime"]
    uptime = subprocess.check_output(uptime_cmd)
    uptime = uptime.decode('utf-8')
    uptime = uptime.replace('IDL_DIR: Undefined variable.','')
    uptime = ' '.join((uptime.split("  ")[1:3])).replace(",","")
    #if 'ERROR' in uptime:
    #    return f'uptime not available for {server_name}'
    return uptime


parser = argparse.ArgumentParser()
parser.add_argument('--email', type=str, default=None, help='Email results to address')
args = parser.parse_args()
instrument = os.environ['INSTRUMENT']
recipients = args.email

#testallDir = '/kroot/rel/default/data'
testallDir = '/home/filer2/jhayashi/kroot/src/util/testall/data'

defaultFile = f'{testallDir}/testall-{instrument}.yaml'
#defaultFile = f'{testallDir}/testall-nires.yaml'

error = 0
uptime_msg = ''
if instrument.lower() == 'nires':
    uptime1 = get_uptime('niresserver1')
    uptime_msg  = f"\nniresserver1's uptime: "
    uptime_ck = uptime1.split()
    if 'up' in uptime_ck:
        #uptime_msg  = f"\nniresserver1's uptime: {uptime1}\n"
        uptime_msg  += f"{uptime1}\n"
    else:
        uptime_msg  += f"{uptime1}                           *** MISSING INFO ***\n"
        #error = 1                                           # restore if desired to reduce error emails

    uptime2 = get_uptime('niresserver2')
    uptime_msg += f"niresserver2's uptime: {uptime2}\n\n"
    print(uptime_msg)

message = uptime_msg

#tbd
#if instrument.lower() == 'lris':
#    uptime1 = get_uptime('lris-red')
#    print(f"uptime for lris-red: {uptime1}")
#    uptime2 = get_uptime('lris-blue')
#    print(f"uptime for lris-blue: {uptime2}")

#error = 0
sub_msg = ''
if not os.path.isfile(defaultFile):
    error = 1
    sub_msg = f'{defaultFile} does not exist'
else:
    #cmd = ['/kroot/rel/default/bin/testall.py']
    #cmd = ['/kroot/rel/default/bin/testall.py', '--datadir', testallDir]
    cmd = ['/home/filer2/jhayashi/kroot/src/util/testall/testall.py', '--datadir', testallDir]
    sub_msg = subprocess.check_output(cmd)
    sub_msg = sub_msg.decode('utf-8')
    if 'ERROR' in sub_msg:
        error = 1
        sub_msg = f'**** ERROR ****\n\n{sub_msg}'

message += sub_msg

#send_email(recipients, message, error)   # testing...

if (recipients and error):
   send_email(recipients, message, error)

##if (error and is_instrument_available() and email):
##    send_email(recipients, message, error)

print()
print(message)
print()
