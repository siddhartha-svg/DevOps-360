#!/bin/python
import boto3
import time
import os

os.environ['http_proxy'] = "http://proxy.ebiz.verizon.com:80/"
os.environ['https_proxy'] = "http://proxy.ebiz.verizon.com:80/"
os.environ['NO_PROXY'] = "169.254.169.254"
#os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

region = os.environ['AWS_REGION']
print(region)

if region == 'us-east-1':
   os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
else:
   os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

http_proxy = os.environ['http_proxy']
https_proxy = os.environ['https_proxy']
NO_PROXY = os.environ['NO_PROXY']

ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

Instance_ID = os.environ['Cur_InstID']
cmd = os.environ['Action']

List1 = Instance_ID.split("\n")

for x in List1:
     print(x)
     if cmd == 'Start' :
         ec2.Instance(x).start()
         print('Instance started')
     elif cmd == 'Stop' :
         ec2.Instance(x).stop()
         print('Instance stopped')
     elif cmd == 'Reboot':
         ec2.Instance(x).reboot()
         print('Instance rebooted')
     else:
         print('Enter select Action correctly.')

#Instance_ID = input('Enter instance id: ')

#cmd = int(input('Enter you objective: Start / Stop or Restart the EC2: '))

'''
if cmd == 'Start' :
    ec2.Instance(Instance_ID).start()
    print('Instance started')
elif cmd == 'Stop' :
    ec2.Instance(Instance_ID).stop()
    print('Instance stopped')
elif cmd == 'Reboot':
    ec2.Instance(Instance_ID).reboot()
    print('Instance rebooted')
else:
    print('Enter select Action correctly.')
'''

print('End of script')
