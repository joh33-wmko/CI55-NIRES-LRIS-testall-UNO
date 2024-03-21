#!/usr/local/anaconda/bin/python

# testall_check.py:
# - called by testall_check.csh in crontab on instrument's virtual machine
# - and calls testall.py to determine if there are any current errors for default instrument

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

parser = argparse.ArgumentParser()
parser.add_argument('--email', type=str, default=None, help='Email results to address')
args = parser.parse_args()
instrument = os.environ['INSTRUMENT']
recipients = args.email

#testallDir = '/kroot/rel/default/data'
testallDir = '/home/filer2/jhayashi/kroot/src/util/testall/data'

defaultFile = f'{testallDir}/testall-{instrument}.yaml'

error = 0
message = ''
if not os.path.isfile(defaultFile):
    error = 1
    message = f'{defaultFile} does not exist'
else:
    #cmd = ['/kroot/rel/default/bin/testall.py']
    #cmd = ['/kroot/rel/default/bin/testall.py', '--datadir', testallDir]
    cmd = ['/home/filer2/jhayashi/kroot/src/util/testall/testall.py', '--datadir', testallDir]
    message = subprocess.check_output(cmd)
    message = message.decode('utf-8')
    if 'ERROR' in message:
        error = 1
        message = f'**** ERROR ****\n\n{message}'

send_email(recipients, message, error)   # testing...

if (recipients and error):
   send_email(recipients, message, error)

print()
print(message)
print()
