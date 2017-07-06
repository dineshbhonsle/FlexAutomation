#This file consists of all the API's needed to configure and unconfigure ARP protocol.

import re
import sys
from robot.api import logger
from os import path
from os.path import dirname, abspath
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from basic.getTestBed import *
from flexswitchV2.flexswitchV2 import FlexSwitch

http_port = 8080

"""
Procedure    : updateArpGlobal
Description  : This procedure updates the ARP Global.
Sample input :
  args = {
      "DUT1" : {
              "Vrf" : "default",   string "KEY", ACCESS:"w", MULTIPLICITY:"1", AUTOCREATE: "true", DESCRIPTION: "System Vrf", DEFAULT:"default"`
              "Timeout" : 600      int32 `DESCRIPTION: "Global Arp entry timeout value. Default value: 600 seconds, Minimum Possible Value: 300 seconds, Unit: second", MIN:300, MAX:1500, DEFAULT: "600"
               }
      "DUT2" : {
              "Vrf" : "default",
              "Timeout" : 600
               }
       }
"""
def updateArpGlobal(args={}):

    logger.info("*** ENABLING ARP GLOBAL ON DEVICES ***")
    Vrf, Timeout = "default",600
    StatusList = {}
    if args:	
        for device in args:
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or Password == "":
                Password = None
            for parameter in args[device].keys():
                if parameter == "Vrf":
                    Vrf = args[device][parameter]
                if parameter == "Timeout":
                    Timeout = args[devce][parameter]
                logger.info("Enabling ARP on device %s"%device)
                ARPObj = FlexSwitch(DeviceIP, http_port, Username, Password)
                logger.info("updateArpGlobal():%s"%device)
                output = ARPObj.updateArpGlobal(Vrf,Timeout)
                jData = json.loads(output.content)
                logger.info(jData)
                if jData['Result'] == "Success":
                    logger.info("RESULT:%s"%jData['Result'])
                    logger.info("ARP Enabled on %s"%device)
                    StatusList.update({device:"ARP Enabled"})
                else:
                    logger.debug("ERROR :%s"%jData['Result'])
                    logger.info("ARP not enabled in %s"%device)
                    StatusList.update({device:"None"})
        if "None" in StatusList.values():
            logger.info("ERROR : %s" %StatusList)
            return False
        else:
            return True
    else:
        logger.info("Please specify the dictionary of devices with ARP details to be configured")
        sys.exit(1)

"""
Procedure   : getAllArpLinuxEntryStates
Description : This procedure returns all the entries in the ARP table
Sample input: ["DUT1","DUT2","DUT3"]
"""
def getAllArpLinuxEntryStates(args = []):
    logger.info("*** CHECKING ARP TABLE ***")
    StatusList = {}
    if args:	
        for device in args:
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or Password == "":
                Password = None
            logger.info("Checking ARP Table on %s"%device)
            ARPObj = FlexSwitch(DeviceIP, http_port, Username, Password)
            logger.info(ARPObj.getAllArpLinuxEntryStates())
    else:
        logger.info("Please specify the list of devices")
        sys.exit(1)  
 
    return True

"""
Procedure   : getArpLinuxEntryState
Description : This procedure returns the ARP entry details of particular interface
              of the peer device
Sample input:
    ("DUT1","fpPort2")
"""
def getArpLinuxEntryState(device, intf):
    logger.info("*** CHECKING ARP TABLE FOR ENTRY ***")
    StatusList = {}
    DeviceIP = getMgmtIP(device)
    Username = getUsername(device)
    if Username == "None" or Username == "":
        Username = None
    Password = getPassword(device)
    if Password == "None" or Password == "":
        Password = None

    logger.info("Checking ARP Table on %s"%device)
    ARPObj = FlexSwitch(DeviceIP, http_port, Username, Password)
    logger.info("getArpLinuxEntryState(%s)"%intf)
    response = ARPObj.getArpLinuxEntryState(intf)
    logger.info("RESULT:%s"%response)
    logger.info(json.loads(response.content))
    if response == "<Response [200]>":
        return True
    else:
        return False


def executeArpRefreshByIfName(device,
                                          IfName):
    logger.info("*** REFRESHING ARP TABLE ***")
    StatusList = {}
    DeviceIP = getMgmtIP(device)
    Username = getUsername(device)
    if Username == "None" or Username == "":
        Username = None
    Password = getPassword(device)
    if Password == "None" or Password == "":
        Password = None

    logger.info("Refreshing ARP Table on %s"%device)
    ARPObj = FlexSwitch(DeviceIP, http_port, Username, Password)
    logger.info("executeArpRefreshByIfName(%s)"%IfName)
    response = ARPObj.executeArpRefreshByIfName(IfName)
    logger.info("RESULT:%s"%response)
    #logger.info(json.loads(response.content))
    if response == "<Response [200]>":
        return True
    else:
        return False


def executeArpRefreshByIPv4Addr(device,
                                    IpAddr):
    logger.info("*** REFRESHING ARP TABLE ***")
    StatusList = {}
    DeviceIP = getMgmtIP(device)
    Username = getUsername(device)
    if Username == "None" or Username == "":
        Username = None
    Password = getPassword(device)
    if Password == "None" or Password == "":
        Password = None

    logger.info("Refreshing ARP Table on %s"%device)
    ARPObj = FlexSwitch(DeviceIP, http_port, Username, Password)
    logger.info("executeArpRefreshByIPv4Addr(%s)"%IpAddr)
    response = ARPObj.executeArpRefreshByIPv4Addr(IpAddr)
    logger.info("RESULT:%s"%response)
    #logger.info(json.loads(response.content))
    if response == "<Response [200]>":
        return True
    else:
        return False




    
