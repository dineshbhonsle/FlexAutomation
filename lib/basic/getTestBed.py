#This file provides API's to get the details of the devices mentioned in the testbed file.
#This provides and single point of change when ever any change is made in testbed file.
import json
from robot.api import logger
import os

"""
Gets the testbed absolute path from the env variable and loads the data from it.
"""
try:
    global data
    with open(os.environ["TESTBED"]) as data_file:
        data = json.load(data_file)
        
except Exception as ex:
    logger.info("%s"%(type(ex)), also_console = True)
    logger.info("Please provide the testbed file",also_console = True)


def getDevices():
    return data["Device"].keys()

def getDetails(device):
    return data["Device"][device]

def getHostname(device):
    return data["Device"][device]["hostname"]

def getUsername(device):
    return data["Device"][device]["username"] 

def getPassword(device):
    return data["Device"][device]["password"] 

def getPlatform(device):
    return data["Device"][device]["platform"] 

def getChassis(device):
    return data["Device"][device]["chassis"] 

def getMgmtIP(device):
    return data["Device"][device]["mgmtIP"] 

def getPortNames(device):
    return data["Device"][device]["ports"].keys()

def getPortName(device,port):
    return data["Device"][device]["ports"][port]

def getPorts(device):
    return data["Device"][device]["ports"].values() 

def getLinks():
    return data["Links"].keys() 

def getConnectedDevices(Link):
    return data["Links"][Link].keys()

def getConnectedPort(Link,device):
    port = data["Links"][Link][device]["Intf"]
    return data["Device"][device]["ports"][port]


