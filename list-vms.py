#!/usr/bin/python3
__author__ = 'Guido Rugo guido.rugo@microfocus.com'

import atexit
import ssl
import requests
import urllib3
import argparse
import getpass
from pyVim import connect
from pyVmomi import vim

parser = argparse.ArgumentParser(description='Standard arguments for talking to vCenter.')
required_parser = parser.add_argument_group('Required arguments')
required_parser.add_argument('-s', '--server', action='store', required=True, help='vSphere service hostname or IP to connect to.')
required_parser.add_argument('-u', '--username', action='store', required=True, help='Username to use when connecting to vc.')
parser.add_argument('-f', '--filter', action='store', help='Filter if contains.')
args = parser.parse_args()

session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
context = None
if hasattr(ssl, '_create_unverified_context'):
    context = ssl._create_unverified_context()
password = getpass.getpass('Password for '+args.username+': ')

service_instance = connect.SmartConnect(host=args.server, user=args.username, pwd=password, sslContext=context)

atexit.register(connect.Disconnect, service_instance)

content = service_instance.RetrieveContent()

container = content.rootFolder
viewType = [vim.VirtualMachine]
containerView = content.viewManager.CreateContainerView(container, viewType, True)
children = containerView.view

for child in children:
    summary = child.summary
    if args.filter:
        if args.filter in summary.config.name:
            print(summary.config.name)
    else:
        print(summary.config.name)