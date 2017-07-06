# This file consists of API's written for configuring interface IPv4 and port parameters.
import re
import sys
import time
import json
from robot.api import logger
from os import path
from os.path import dirname, abspath
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from flexswitchV2.flexswitchV2 import FlexSwitch
from getTestBed import *

"""
Procedure   : createIPv4Intf
Description : Dictionary of devices and their ports with IP addresses.
           Configures IP addresses on the ports of the devices. Collects the status of all the
           interfaces and displays the final result with succeeded and failed configurations.
Arguments   : {
            "IntfRef"   : N/A,  [KEY] Interface name or ifindex of port/lag or vlan on which this IPv4 object is configured
            "AdminState": "UP",       Administrative state of this IP interface
            "IpAddr"    : N/A   [KEY] Interface IP/Net mask in CIDR format to provision on switch interface
              }
Sample input:
                args={ "DUT1": {
                               "fpPort25" : "192.168.0.2/24",
                               "fpPort35" : "192.168.1.2/24
                               },
                       "DUT2": {
                               "fpPort25" : "192.168.0.3/24",
                               "fpPort35" : "192.168.1.3/24
                               }
                     }
"""
http_port = 8080   
def createIPv4Intf(args={}):

    if args:

        logger.info("*** CONFIGURING IP ADDRESS ON INTERFACES OF DEVICES ***")
        StatusList ={}
        for device in args.keys():

            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or Password == "":
                Password = None

            for intf in args[device].keys():        
                IfaceIP = args[device][intf]
                logger.info("Configuring IP Address on %s interface of %s with IP %s"%(intf,device,IfaceIP))
                swtch = FlexSwitch (DeviceIP, http_port, user=Username, passwd = Password)
                logger.info("createIPv4Intf(%s) : %s"%(intf,device))
                response = swtch.createIPv4Intf(intf, IfaceIP, AdminState='UP')
                jData = json.loads(response.content)
                if jData['Result'] == "Success":
                    logger.info("RESULT : %s"%jData['Result'])
                    response1 = swtch.getIPv4Intf(intf)
                    logger.info("IP CONFIGURATION STATUS")
                    logger.info("INTF OBJECT DETAILS:%s"%json.loads(response1.content))
                    logger.info("IP address configured on %s interface of %s"%(intf,device))
                    StatusList.update({"%s[%s]"%(device,intf) : "PASS"})
                else:
                    logger.info("ERROR:%s"%jData['Result'])
                    logger.info("IP address could not be configured on %s interface of %s"%(intf,device))
                    StatusList.update({"%s[%s]"%(device,intf) : "FAIL"})

        if "FAIL" in StatusList.values():
	    logger.debug(StatusList)
            return False
        else:
	    logger.info(StatusList)
            return True
    else:
        logger.info("Please specify the list of devices and it's interface ip addresses in the arguments")
        sys.exit(1)

"""
Procedure  : deleteIPv4Intf
Description: Dictionary of devices and list of ports.
           Deletes IP addresses on the ports of the devices. Collects the status of all the
           interfaces and displays the final result with succeeded and failed configurations.
Arguments  : {
          "IntfRef" : N/A,  [KEY] Interface name or ifindex of port/lag which should be deleted.
             }
Sample input:
   args={
          "DUT1" :["fpPort25","fpPort65"],
          "DUT2" :["fpPort35"]
        }
"""
def deleteIPv4Intf(args={}):

    if args:
        logger.info("UNCONFIGURING IP ADDRESS ON DEVICE[S]")
        StatusList ={}
        for device in args.keys():

            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or Password == "":
                Password = None
  
            for intf in args[device]:
	        logger.info("Unconfiguring IP Address on %s interface of %s "%(intf,device))
                swtch = FlexSwitch (DeviceIP, http_port, user=Username, passwd = Password)
                logger.info("deleteIPv4(%s) : %s"%(intf,device))
	        response = swtch.deleteIPv4Intf(intf)
                jData = json.loads(response.content) 
	        if jData['Result'] == "Success":
                    logger.info("RESULT : %s"%jData['Result'])
                    logger.info("VALIDATING IP ADDRESS UNCONFIGURATION")
                    response = swtch.getIPv4Intf(intf)
                    logger.info("RESULT:%s"%response)
                    logger.info("Failed To Find Entry of the interface, thus ip address is unconfigured")
                    StatusList.update({"%s[%s]"%(device,intf) : "PASS"})
                else:
                    logger.info(jData['Result'])
	            logger.info("IP address could not be unconfigured on %s interface of %s"%(intf,device))
		    StatusList.update({"%s[%s]"%(device,intf) : "FAIL"})
        if "FAIL" in StatusList.values():
	    logger.info(StatusList)
            return False
        else:
            logger.info(StatusList)
            return True
    else:
        logger.info("Please specify the list of devices and it's interfaces in the arguments")
        sys.exit(1)
"""
Procedure  : getIPv4IntfState
Description: This procedure takes interface ref as input and returns the details if the interface exists.
Arguments  : {
            "IntfRef" : N/A  [KEY]  STRING  System assigned interface id of L2 interface (port/lag/vlan) to which this IPv4 object is linked.
            }
Sample Input:{
             "DUT1" :["fpPort25","fpPort65"],
             "DUT2" :["fpPort35"]
             }
"""
def getIPv4IntfState(args = {}):

    if args:
        logger.info("*** CHECKING INTERFACE STATUS OF ALL DEVICES ***")
        StatusList = {}
        for device in args.keys():

            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or Password == "":
               Password = None
 	
            for intf in args[device]:
                logger.info("Checking interface state on %s interface of %s "%(intf,device))
                swtch = FlexSwitch (DeviceIP, http_port, user=Username, passwd = Password)
                logger.info("getIPv4IntfState(%s) : %s"%(intf,device))
                response = swtch.getIPv4IntfState(intf)
                logger.info("RESULT: %s"%response)
                logger.info("INTF STATE OBJECT DETAILS:%s"%json.loads(response.content))
                if str(response) == "<Response [200]>":
                    logger.info("%s interface of %s UP"%(intf,device))
                    StatusList.update({"%s[%s]"%(device,intf) : "UP"})
                else:
	            logger.info("%s interface of %s DOWN"%(intf,device))
                    StatusList.update({"%s[%s]"%(device,intf) : "DOWN"})

        if "DOWN" in StatusList.values():
	    logger.info(StatusList)
            return False
        else:
            logger.debug(StatusList)
            return True
    else:
        logger.info("*** Please specify the list of devices ***")
        sys.exit(1)

"""
Procedure  : updatePort
Description: This procedure updates port properties. Default values are taken for optional parameters.
             Currently support has been added only to update adminState.
Arguments  : {
              "IntfRef" : N/A,         [KEY] string 	Front panel port name or system assigned interface id
              "IfIndex" : "",                int32 	System assigned interface id for this port. Read only attribute
              "PhyIntfType" : "",            string 	Type of internal phy interface
              "MacAddr" : "",                string 	Mac address associated with this port
              "Speed" : "",                  int32 	Port speed in Mbps
              "MediaType" : "",              string 	Type of media inserted into this port
              "Mtu" : "",                    int32 	Maximum transmission unit size for this port
              "BreakOutMode" : "",           string 	Break out mode for the port. Only applicable on ports that support breakout. Valid modes - 1x40
              "PRBSRxEnable" : "",           bool 	Enable/Disable PRBS checker on this port
              "Description" : "",            string 	User provided string description
              "PRBSPolynomial" : "",         string 	PRBS polynomial to use for generation/checking
              "Duplex" : "",                 string 	Duplex setting for this port
              "LoopbackMode" : "",           string 	Desired loopback setting for this port
              "EnableFEC" : "",              bool 	Enable/Disable 802.3bj FEC on this interface
              "AdminState" : "",             string 	Administrative state of this port
              "Autoneg" : "",                string 	Autonegotiation setting for this port
              "PRBSTxEnable" : ""            bool 	Enable/Disable generation of PRBS on this port
            }
Sample input : "DUT1", "fpPort25", "UP"
"""
def updatePort(device, IntfRef, adminState):

    logger.info("UPDATING THE PORT STATUS")
    DeviceIP = getMgmtIP(device)
    Username = getUsername(device)
    if Username == "None" or Username == "":
        Username = None
    Password = getPassword(device)
    if Password == "None" or Password == "":
        Password = None
    logger.info("Updating port %s of %s to %s"%(IntfRef,device,adminState))
    swtch = FlexSwitch (DeviceIP, http_port, user=Username, passwd = Password)
    logger.info("updatePort(%s,%s) : %s"%(IntfRef,adminState,device))
    response = swtch.updatePort(IntfRef=IntfRef,AdminState=adminState)
    time.sleep(1)
    jData = json.loads(response.content) 
    portState = json.loads(swtch.getPortState(IntfRef).content)["Object"]["OperState"]
    if jData['Result'] == "Success":
        logger.info("RESULT : %s"%jData['Result'])
        logger.info("PORT %s STATUS : %s"%(IntfRef,portState))
        if portState == adminState:
            return True
        else:
            return False
    elif jData['Result'] == "Error: Nothing to be updated.":
        logger.info("RESULT : %s"%jData['Result'])
        logger.info("PORT %s STATUS : %s"%(IntfRef,portState))
        if portState == adminState:
            return True
        else:
            return False
    else:
        logger.info("ERROR : %s"%jData['Result'])
        logger.info("PORT %s STATUS : %s"%(IntfRef,portState))
        if portState == adminState:
            return True
        else:
            return False

