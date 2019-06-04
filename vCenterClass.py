# -*- coding: utf-8 -*-
"""
Python Class Library for VMware vCenter Rest API
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
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime

#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

DEBUG = True

class vCenter:
    """
    class vCenter
    routines for the SimpliVity RestAPI
    """
    def __init__(self, url):
        self.url = url          # base URL
        self.s= []    # session access token
        #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
    def connect(self, username, password):
        self.s=requests.Session()
        self.s.verify=False
        response = self.s.post(self.url+'com/vmware/cis/session',auth=(username,password))
        return response
        
    def disconnect(self):
        response = self.s.delete(self.url+'com/vmware/cis/session')
        return(0)
        
    def getVMs(self):
        vms= self.s.get(self.url+'vcenter/vm')
        return(vms)
        
    def getVM(self,vmid=None):
        if vmid:
            url = self.url+'vcenter/vm/'+str(vmid)
        else:
            url= self.url+'vcenter/vm'
        return self.s.get(url)

    def powerOffVM(self, vmid):
        response = self.s.post(self.url+'vcenter/vm/'+vmid+'/power/stop')
        return(response)

    def powerOnVM(self, vmid):
        response = self.s.post(self.url+'vcenter/vm/'+vmid+'/power/start')
        return(response)

    def resetVM(self, vmid):
        response = self.s.post(self.url+'vcenter/vm/'+vmid+'/power/reset')
        return(response)    

    def getVMpower(self, vmid):
        response = self.s.get(self.url+'vcenter/vm/'+vmid+'/power')
        return(response)
        
    def suspendVM(self, vmid):
        response = self.s.post(self.url+'vcenter/vm/'+vmid+'/power/suspend')
        return(response)
        
        
    def deleteVM(self, vmid):
        response = self.s.delete(self.url+'vcenter/vm/'+vmid)
        return(response)
        
        