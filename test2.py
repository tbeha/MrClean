# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 18:14:57 2019

@author: BEHAT
"""

from cryptography.fernet import Fernet
import getpass
from lxml import etree 
from SimpliVityClass import *
from vCenterClass import *
from datetime import datetime
import json

keyfile='mrclean.key'
xmlfile='mrclean.xml'

""" Read keyfile """
f = open(keyfile, 'r')
k2=f.readline()
f.close()
key2=k2.encode('ASCII')

""" Parse XML File """

tree = etree.parse(xmlfile)
u2=(tree.find("user")).text
p2=(tree.find("password")).text

f = Fernet(key2)
user = f.decrypt(u2.encode('ASCII')).decode('ASCII')
password = f.decrypt(p2.encode('ASCII')).decode('ASCII')

ovc=tree.find("ovc").text
vcenter=tree.find("vcenter").text
VMsToStay=tree.findall("VM")
backups=tree.findall("Backup")
datastores=tree.findall("Datastore")
localCluster=tree.find("LocalCluster").text
remoteCluster=tree.find("RemoteCluster").text

""" Open a connection to the SimpliVity Rest API          
url="https://"+ovc+"/api/"          
svt = SimpliVity(url)
svt.connect(user,password)

svtdatastores = svt.GetDataStore()['datastores']
for svtdx in svtdatastores:
    print(svtdx.get("name"))
""" 

parsed_json = json.loads('BBNRefPolicies.json')
