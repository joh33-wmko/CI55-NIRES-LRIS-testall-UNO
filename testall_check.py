#!/usr/local/anaconda/bin/python

# Uses TestAll.py to determine if there are any current errors for input instrument

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

def send_email(message, error):
    errorMsg = 'ERROR: ' if error == 1 else ''
    msg = MIMEText(message)
    msg['Subject'] = f"{errorMsg}{instrument.upper()} RTI Alarm ({socket.gethostname()})"
    msg['To'] = email
    msg['From'] = 'koaadmin@keck.hawaii.edu'
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

parser = argparse.ArgumentParser()
#parser.add_argument('instrument', type=str, help='Instrument name')
#parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='Specific HST date to search')
parser.add_argument('--email', type=str, default=None, help='Email results to address')
args = parser.parse_args()
#instrument = args.instrument.lower()
instrument = os.environ['INSTRUMENT']
#date = args.date
email = args.email

date = datetime.strftime(datetime.now().date(), '%Y-%m-%d')   # added
#print(date)
print(email)

#testallDir = '/kroot/rel/default/data'
testallDir = '/home/filer2/jhayashi/kroot/src/util/testall/data'

defaultFile = f'{testallDir}/testall-{instrument}.yaml'
#defaultFile = f'{testallDir}/testall-nires.yaml'

#print(testallFile)

error = 0
#if not os.path.isfile(testallFile):
    #error = 1
    #message = f'{testallFile} does not exist'
if not os.path.isfile(defaultFile):
    error = 1
    message = f'{defaultFile} does not exist'
else:
    #cmd = ['/kroot/rel/default/bin/testall.py']
    cmd = ['/home/filer2/jhayashi/kroot/src/util/testall/testall.py', '--datadir', testallDir]
    message = subprocess.check_output(cmd)
    message = message.decode('utf-8')
    if 'ERROR' in message:
        error = 1
        message = f'**** ERROR ****\n\n{message}'

#if (error and is_instrument_available() and email):
#    send_email(message, error)

if email != None:
    send_email(message, error)

print()
print(message)
print()
