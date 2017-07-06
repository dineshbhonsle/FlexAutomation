#This flie consists of API's written specifically for testbed validation.
#These API's are called in robot testcases which validate one aspect of the testbed.
#It performs checks such as the reachability of the devices, existence of the
#ports, adminstate of the interfaces and more.

from robot.api import logger
import sys
import time
import re
from os import path
from os.path import dirname, abspath
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from robot.api import logger
from getTestBed import *
from configVariables import *
from flexswitchV2.flexswitchV2 import FlexSwitch

http_port = 8080
"""
Procedure  : deviceStatus
Description: This procedure checks if the devices mentioned in the testbed
             are reachable. It does not take any input and performs check on all
             devices in the testbed.
"""
def deviceStatus():
    logger.info("*** VALIDATING DEVICE STATUS ***")
    DeviceState = {}
    devices = getDevices()
        
    for device in devices:
        DeviceIP = getMgmtIP(device)
        Username = getUsername(device)
        if Username == "None" or Username == "":
            Username = None
        Password = getPassword(device)
        if Password == "None" or Password == "":
            Password = None	
        swtch = FlexSwitch(DeviceIP, http_port, user=Username, passwd = Password)
        logger.info("Checking the status of %s"%(device))
	try:
            logger.info("%s.getAllSystemStatusStates()"%device)
	    response = swtch.getAllSystemStatusStates()
            #logger.info("RESULT: %s"%response)
            logger.info("DEVICE %s --> EXISTS"%device)
            DeviceState.update({device : "Exists"})

	except Exception as ex:
	    logger.debug("%s,--> %s"%(type(ex).__name__,device))
            logger.info("DEVICE %s --> DOESN'T EXISTS"%device)
            DeviceState.update({device : "None"})
    if re.search("None",str(DeviceState)):
        logger.info("*** DEVICE STATUS ***")
        logger.debug(DeviceState)
        return False
    else:
        return True
	
"""
Procedure  : portStatus
Description: This procedure checks if the ports described for all devices exist.
             It does not take any input and performs check on all devices in the testbed.
"""
def portStatus():
    logger.info("***VALIDATING PORT EXISTENCE***")
    devices = getDevices()
    PortState = {}
    for device in devices:
        PortState.update({device : {}})
        ports = getPorts(device)
        DeviceIP = getMgmtIP(device)
        Username = getUsername(device)
        if Username == "None" or Username == "":
            Username = None
        Password = getPassword(device)
        if Password == "None" or Password == "":
            Password = None	
        swtch = FlexSwitch(DeviceIP, http_port, user=Username, passwd = Password)
        for port in ports:
            logger.info("Checking %s port of %s"%(port,device))
            try:
                logger.info("getPort(%s): %s"%(port,device))
                response = swtch.getPort(port)
                jdata = json.loads(response.content)
                logger.info("RESULT: %s"%response)
                logger.info("PORT OBJECT DETAILS:%s"%jdata)
                if (str(response)) != "<Response [200]>":
                    logger.info("PORT  %s of %s --> DOESN'T EXISTS"%(port,device))
                    PortState[device].update({port : "None"})
       	        else:
                    logger.info("PORT  %s of %s --> EXISTS"%(port,device))
                    PortState[device].update({port : "Exists"}) 
            except Exception as ex:
                logger.info("RESULT: %s"%response)
	        logger.debug("%s,--> %s"%(type(ex).__name__,device))
                logger.info("PORT  %s of %s --> DOESN'T EXISTS"%(port,device))
                PortState[device].update({port : "None"})

    if re.search("None",str(PortState)):
        logger.info("*** PORT STATUS ***")
        logger.debug(PortState)
        return False
    else:
        return True
	
"""
Procedure  : linkStatus
Description: This procedure checks if the link described for all devices are UP.
             It checks for the OperState on both the interfaces of a link and checks if the
             OperState is UP and fails the check if it is found DOWN.
             It does not take any input and performs check on all devices in the testbed.
"""
def linkStatus():
    logger.info("***VALIDATING LINK STATUS***")
    operStateList = {}
    Links = getLinks()
    status = [] 
    for link in Links:
        EndDevices = getConnectedDevices(link)
        for device in EndDevices:
            ConnectedPort = getConnectedPort(link,device) 	
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or Password == "":
                Password = None	
            swtch = FlexSwitch (DeviceIP, http_port, user=Username, passwd = Password)
            logger.info("Checking operational state of %s port of %s"%(ConnectedPort,device))
            try:
                logger.info("%s.getPortState()"%device)
                response = swtch.getPortState(ConnectedPort)
                logger.info("RESULT: %s"%response)
                jdata = json.loads(response.content)
                logger.info("PORT STATE OBJECT DETAILS: %s"%jdata)
                operState = jdata['Object']["OperState"]
                logger.info("OperState on %s is %s"%(ConnectedPort,operState))
                if operState == "UP":
                    status.append(True)
                else:
                    status.append(False)
	    except Exception as ex:
		logger.info("%s"%(type(ex)))
		status.append(False)
        if False in status:
            logger.info("The operState of link %s is DOWN"%link)
            operStateList[link]="DOWN"
        else:
            logger.info("The operState of link %s is UP"%link)
            operStateList[link]="UP"
    if "DOWN" in operStateList.values():
        logger.debug("The operState of one/more links is DOWN. Please check the setup")
        logger.debug(operStateList)
        return False
    else:
        logger.info("The operState of all links are UP")
        return True

"""
Procedure  : adminStatus
Description: This procedure checks if the ports described for all devices are in adminState.
             UP. If the port is found "DOWN", it tries to bring the port UP for a pre defined
             interval and fails the test if the port does not come UP.
             It does not take any input and performs check on all devices in the testbed.
"""
def adminStatus():
    logger.info("***VALIDATING INTERFACE STATUS***")
    global LinkStartVal
    global LinkmaxVal
    global LinkStepVal
    portAdminState = {}
    linkStateList = {}
    links = getLinks()
    for device in getDevices():
        for port in getPorts(device):
            portAdminState.update({port:""})
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or Password == "":
                Password = None	
            swtch = FlexSwitch (DeviceIP, http_port, user=Username, passwd = Password)
            logger.info("Checking admin state of %s port of %s"%(port,device))
            try:
		logger.info("%s.getPort()"%device)
        	response = swtch.getPort(port)
                logger.info("RESULT: %s"%response)
		jdata = json.loads(response.content)
                logger.info("PORT OBJECT DETAILS: %s"%jdata)
                AdminState = jdata['Object']["AdminState"]
                logger.info("The AdminState on interface %s is %s"%(port,AdminState))
                portAdminState[port]= AdminState
                if AdminState == "DOWN":
                    response = swtch.updatePort(port, "UP")
                    logger.info("IN here %s"%response)
                    while (LinkStartVal < LinkmaxVal):
                        time.sleep(interval)
                        LinkStartVal += LinkStepVal
                        linkStatus()
                else:
                   continue
            except Exception as ex:
		logger.info("%s"%(type(ex)), also_console = True)
    logger.info(portAdminState)
    if "DOWN" in portAdminState.values():
        logger.info("*** LINK STATUS ***")
        logger.debug("The one/more links is DOWN. Please check the setup")
        logger.debug(linkStateList)
        return False
    else:
        return True

