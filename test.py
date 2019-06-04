# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 10:21:11 2019

@author: BEHAT
"""

from cryptography.fernet import Fernet
import getpass
from lxml import etree 
from SimpliVityClass import *
from vCenterClass import *
from datetime import datetime
import json


def logwriter(f, text):
    f.write(str(datetime.today()) +": "+text+" \n")
    
def logopen(filename):
    f = open(filename,'w')
    f.write(str(datetime.today())+": Logfile opened \n")
    return f

def logclose(f):
    f.write(str(datetime.today())+": Logfile closed \n")
    f.close()


keyfile='mrclean.key'
xmlfile='mrclean.xml'

today=datetime.today()
logfile="mrclean."+str(datetime.today())[0:10]+".log"
log=logopen(logfile)

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

logwriter(log,"Clean Up Parameters")
logwriter(log,"OVC: "+ovc)
logwriter(log,"vCenter: "+vcenter)
logwriter(log,"VMs to stay:")
for vm in VMsToStay:
    logwriter(log,vm.text)
logwriter(log,"Permanent Backups:")
for backup in backups:
    logwriter(log,backup.text)
logwriter(log,"Permanent Datastores:")
for datastore in datastores:
    logwriter(log,datastore.text)    
logwriter(log,"LocalCluster:  "+localCluster)
logwriter(log,"RemoteCluster: "+remoteCluster)
logwriter(log,"###################################################")

""" Open a connection to the SimpliVity Rest API """          
url="https://"+ovc+"/api/"          
svt = SimpliVity(url)
svt.connect(user,password)
logwriter(log,"Opened a connection to OVC: "+ovc+"   "+url)    


res = svt.GetCertificate()
cert = res["certificates"]
logwriter(log,"Certificate:")
logwriter(log,cert[0]["certificate"])
logwriter(log,"hash: "+cert[0]["hash"])
logwriter(log,"serialno: "+cert[0]["serialno"])
logwriter(log,"subject: "+cert[0]["subject"])


"""
res=svt.DefinePolicy(policyname)
res=svt.AddPolicyRule(\
        policy_id=svt.GetPolicyId(policyname),\
        destination=svt.GetClusterId(clustername),\
        frequency=1440,\
        retention=1440,\
        days='All',\
        startTime='00:00',\
        endTime='02:00',\
        replace=True)
"""
        
""" Close the vCenter connection and the logfile """            
#vc.disconnect()  
logclose(log)    
    
