from json import loads
import json
import threading
import paramiko
import argparse
import time
import os 
from os import walk
from os import listdir
sourceDir='platformRepository'
avaialableNodes='freeNodeList.json' 
pathToNodeUNit='nodeUnit.py'


ip='172.17.0.3'
port='22'
username='test'
password='test'

ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip,port=port,username=username,password=password)
ssh_client.exec_command('mkdir src')
ssh_client.exec_command('mkdir conf')

ftp_client=ssh_client.open_sftp()
ftp_client.put('clean.py','clean.py')
ftp_client.close()

    # toStart=[]
