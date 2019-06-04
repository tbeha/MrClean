# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 08:19:38 2019

@author: BEHAT
"""

from cryptography.fernet import Fernet
import getpass
from lxml import etree 

keyfile='mrclean.key'
xmlfile='mrclean.xml'

uname = input("Username: ")
password = getpass.getpass()

key = Fernet.generate_key()
k1 = key.decode('ASCII')
f = open(keyfile,'w')
f.write(key.decode('ASCII'))
f.close()

f = Fernet(key)
token = f.encrypt(password.encode('ASCII'))
user = f.encrypt(uname.encode('ASCII'))

root = etree.Element("data")
etree.SubElement(root,"username").text=uname
etree.SubElement(root,"user").text=user
etree.SubElement(root,"password").text=token
xmloutput = etree.tostring(root, pretty_print=True)
f = open(xmlfile,'w')
f.write(xmloutput.decode('ASCII'))
f.close()

"""
# Read the data again

f = open(keyfile, 'r')
k2=f.readline()
f.close()
key2=k2.encode('ASCII')

tree = etree.parse(xmlfile)
u2=(tree.find("user")).text
p2=(tree.find("password")).text

f = Fernet(key2)
u3 = f.decrypt(u2.encode('ASCII')).decode('ASCII')
p3 = f.decrypt(p2.encode('ASCII')).decode('ASCII')
print("User:     ",u3)
print("Password: ",p3)
"""