#!/kroot/rel/default/bin/kpython3

# testall_check.py:
#   is called by testall_check.csh in crontab on vm-nires
#   and calls testall.py to determine if there are any current errors for default instrument

import argparse
import datetime as dt
import ktl
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
import socket
from urllib.request import urlopen
import json
from subprocess import Popen, PIPE

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

# write TESTALL = Checking
ktl_service = 'niresmon'
ktl_keyword_name = 'TESTALL'
ktl_keyword = 'niresmon.testall'
keyword_value = 'Checking'
keyword = ktl.cache(ktl_keyword)
keyword.write(keyword_value)
value = keyword.read()
upd_msg1 = 'Updated ' + ktl_service + ' service KTL keyword(s):\n'
upd_msg1 += '        ' + ktl_keyword_name + ' = ' + value + '\n\n'

parser = argparse.ArgumentParser()
parser.add_argument("--datadir", type=str, default=None, help='Dir path to config data for tests. \
               If not specified, will look in script dir.  File should be "testall-[instr].yaml"')
parser.add_argument('--email', type=str, default=None, help='Email results to address')
args = parser.parse_args()
instrument = os.environ['INSTRUMENT']
testallDir = args.datadir
recipients = args.email

if testallDir == '':
    testallDir = '/kroot/rel/default/data'

defaultFile = f'{testallDir}/testall-{instrument}.yaml'

error = 0
uptime_msg = ''
if instrument.lower() == 'nires':
    uptime1 = get_uptime('niresserver1')
    uptime_msg  = f"\nniresserver1's uptime: "
    uptime_ck = uptime1.split()
    if 'up' in uptime_ck:
        uptime_msg  += f"{uptime1}\n"
    else:
        uptime_msg  += f"{uptime1.strip()}\t*** MISSING INFO ***\n"
        error = 1     # comment out to reduce error emails

    uptime2 = get_uptime('niresserver2')
    uptime_msg += f"niresserver2's uptime: {uptime2}\n\n"

message = upd_msg1
message += uptime_msg

sub_msg = ''
if not os.path.isfile(defaultFile):
    error = 1
    sub_msg = f'{defaultFile} does not exist'
else:
    #cmd = ['/kroot/rel/default/bin/testall.py']
    cmd = ['/kroot/rel/default/bin/testall.py', '--datadir', testallDir]
    sub_msg = subprocess.check_output(cmd)
    sub_msg = sub_msg.decode('utf-8')
    if 'ERROR' in sub_msg:
        error = 1
        sub_msg = f'**** ERROR ****\n\n{sub_msg}'

message += sub_msg

# write TESTALL = Passed or Failed
value = ''
if (error):
    keyword_value = 'Failed'
else:
    keyword_value = 'Passed'
keyword = ktl.cache(ktl_keyword)
keyword.write(keyword_value)
value = keyword.read()
upd_msg2 = '\nUpdated niresmon service KTL keyword(s):\n'
upd_msg2 += '        ' + ktl_keyword_name + ' = ' + value + '\n'

# write TESTALL_DONE = <current epoch time in sec>
ktl_keyword = 'niresmon.testall_done'
ktl_keyword_name = 'TESTALL_DONE'
now = dt.datetime.strftime(dt.datetime.now(),'%s')
value = keyword_value = now
keyword = ktl.cache(ktl_keyword)
keyword.write(keyword_value)
epoch = keyword.read()
value = dt.datetime.fromtimestamp(int(epoch)).strftime('%c')
upd_msg2 += '        ' + ktl_keyword_name + ' = ' + now + ' (' + value + ')'

message += upd_msg2

#send_email(recipients, message, error)   # force email

if (recipients and error):
   send_email(recipients, message, error)

#if (error and is_instrument_available() and email):
#    send_email(recipients, message, error)

print()
print(message)
print()
