# -*- coding: utf-8 -*-
"""
CTC SimpliVity Demo environment Clean Up script
Copyright (c) 2019 Thomas Beha

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    https://www.gnu.org/licenses/gpl-3.0.en.html 

"""

from cryptography.fernet import *
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

#path = '/opt/mrclean/'
path = './'
keyfile= path + 'data/mrclean.key'
xmlfile=path + 'data/mrclean.xml'

today=datetime.today()
logfile=path+"data/mrclean."+str(datetime.today())[0:10]+".log"
log=logopen(logfile)

""" Read keyfile #########################################################################"""
f = open(keyfile, 'r')
k2=f.readline()
f.close()
key2=k2.encode('ASCII')

""" Parse XML File #########################################################################"""

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
svt.Connect(user,password)
logwriter(log,"Opened a connection to OVC: "+ovc+"   "+url)    

""" Open a connection to the vCenter """
url="https://"+vcenter+"/rest/"
vc = vCenter(url)
token = vc.connect(user,password)
logwriter(log,"Connection opened to vcenter"+vcenter)
      
logwriter(log,"Start Clean Up Action")

""" clean up VMs #########################################################################"""

logwriter(log,"Clean up VMs")
vms = vc.getVMs()
vm_response=json.loads(vms.text)
json_data=vm_response["value"]
for vm in json_data:
    rmVM=True
    vmname = vm.get("name")
    for vmp in VMsToStay:
        if(vmp.text == vmname):
            rmVM = False
    if rmVM:
        logwriter(log,vm.get("name")+" is not on the blacklist.")
        if vm.get("power_state") == "POWERED_ON":
            logwriter(log,"Power Off VM")
            vc.powerOffVM(vm.get("vm"))
        logwriter(log,"Remove VM")
        vc.deleteVM(vm.get("vm"))
        
""" Clean up backups #########################################################################"""

logwriter(log,"Clean up backups")
svtbackups = (svt.GetBackups(past_hours=144)).get("backups")
for svtbx in svtbackups:
    rmBackup = True
    if(svtbx.get("type") != "POLICY" ):
        bxname = svtbx.get("name")
        for bxp in backups:
            if(bxp.text == bxname):
                rmBackup = False
    else:
        bxvmname = svtbx.get("virtual_machine_name")
        for vmp in VMsToStay:
            if(vmp.text == bxvmname):
                rmBackup = False        
    if rmBackup:
        logwriter(log,"Delete backup: "+svtbx.get("name")+"::"+svtbx.get("type")+"::"+svtbx.get("virtual_machine_name")+"::"+svtbx.get("id"))
        res =svt.DeleteBackup(svtbx.get("id"))
        logwriter(log,"Result: "+str(res))

""" Clean up datastores #########################################################################"""

logwriter(log,"Clean up datastores")
svtdatastores = svt.GetDataStore()['datastores']
for svtdx in svtdatastores:
    rmDataStore = True
    for dxp in datastores:
        if(dxp.text == svtdx.get("name")):
            rmDataStore = False
    if rmDataStore:
        logwriter(log,"Delete Datastore: "+svtdx.get("name")+"::"+svtdx.get("omnistack_cluster_name")+"::"+svtdx.get("id"))
        res = svt.RemoveDataStore(svtdx.get("name"))
        logwriter(log,"Result: "+str(res))

""" Clean up policies #########################################################################"""

logwriter(log,"Clean up policies") 
localClusterId = svt.GetClusterId(localCluster)
remoteClusterId = svt.GetClusterId(remoteCluster)      
svt_policies = svt.GetPolicy()
with open(path+'data/BBNRefPolicies.json', 'r') as fp:
    policies = json.load(fp) 
""" Delete unnecessary policies """
logwriter(log,"Delete unnecessary policies")
for svt_pol in svt_policies["policies"]:
    rmPol = True
    for policy in policies:
        if svt_pol["name"] == policy["name"]:
            rmPol = False
    if rmPol:
        logwriter(log,"Remove Backup Policy: "+svt_pol["name"])
        res = svt.DeletePolicy(svt_pol["name"])
        logwriter(log,str(res))
""" Check for missing policies """
logwriter(log,"Check for missing policies")
for policy in policies:
    addPol = True
    for svt_pol in svt_policies["policies"]:
        if svt_pol["name"] == policy["name"]:
            addPol = False
    if addPol:
        logwriter(log,"Add missing Policy: "+policy["name"])
        res = svt.DefinePolicy(policy["name"])
        logwriter(log,str(res))        

""" Update the existing policies"""
logwriter(log,"Update existing policies")    
for policy in policies:
    pname = policy.get("name")
    logwriter(log,"Checking Policy: "+pname)
    for svt_pol in svt_policies["policies"]:
        svt_pol_name = svt_pol["name"]
        svt_pol_id = svt_pol["id"]
        if svt_pol_name == pname:
            if len(svt_pol["rules"]) > 0:
                logwriter(log,"Remove existing rules") 
                for rule in svt_pol["rules"]:
                    res=svt.DeletePolicyRule(svt_pol_id,rule["id"])
                    logwriter(log,"Policy removed: "+svt_pol_name+"::"+svt_pol_id)
                    logwriter(log,str(rule))
                    logwriter(log,"Result: "+str(res)) 
            rules = policy.get("rules")
            if len(rules) > 0:
                logwriter(log,"Create the new rules")
                for rule in rules:
                    if rule["destination_name"] == 'Local':
                        clusterId = localClusterId
                    else:
                        clusterId = remoteClusterId
                    if rule["application_consistent"]:
                        appcon = 'true'
                    else:
                        appcon = 'false'
                    res=svt.AddPolicyRule(\
                                          policy_id=svt_pol_id,\
                                          destination=clusterId,\
                                          frequency=rule["frequency"],\
                                          retention=rule["retention"],\
                                          days=rule["days"],\
                                          startTime=rule["start_time"],\
                                          endTime=rule["end_time"],\
                                          appConsistent=rule["application_consistent"],\
                                          consistencyType=rule["consistency_type"],\
                                          replace=False)             
                    logwriter(log,"Backup Policy added to Policy: "+pname)                    
                    logwriter(log,str(rule))
                    logwriter(log,"Result: "+str(res))  


""" Close the vCenter connection and the logfile """            
vc.disconnect()  
logclose(log)