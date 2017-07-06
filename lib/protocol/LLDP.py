import re
import sys
from robot.api import logger
from os import path
from os.path import dirname, abspath
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from basic.getTestBed import *
from flexswitchV2.flexswitchV2 import FlexSwitch

"""
Procedure: updateLLDPGlobal
Description:
Sample input: 
args = {
       "DUT1" : {
        "Vrf" : "default",       string       "KEY", ACCESS:"w", MULTIPLICITY:"1", DESCRIPTION: "LLDP Global Config For Default VRF", DEFAULT:"default",    					              AUTOCREATE:"true"`
        "TxRxMode" : "TxRx",     string      'DESCRIPTION: "Transmit/Receive mode configruration for the LLDP agent", SELECTION:"TxOnly/RxOnly/TxRx",     					              DEFAULT :  "TxRx"`
        "Enable" : True,         bool        'DESCRIPTION: "Enable/Disable LLDP Globally", DEFAULT:false'
        "TranmitInterval" : 30   int32       'DESCRIPTION: "LLDP Re-Transmit Interval in seconds", DEFAULT:30'
        "SnoopAndDrop" : False   bool        'DESCRIPTION: "Operational mode to determine whether LLDP traffic is bi-directionally forwarded. This 						     configuration is only available on select platforms", DEFAULT:false'
                },
       "DUT2" : {
        "Vrf" : "default",    
        "TxRxMode" : "TxRx",  
        "Enable" : True,      
        "TranmitInterval" : 30
        "SnoopAndDrop"    : False
                }
        }
"""
http_port = 8080
def updateLLDPGlobal(args ={}):

    LLDPGlobalStatusList = {}
    vrf,enable,tranmitinterval,txrxmode,snoopanddrop = "default",True,30,"TxRx",False
    if args:
        for device in args.keys():
	    
            DeviceIP = getMgmtIP(device)
	    Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None
            for parameter in args[device].keys():
                if parameter == "Vrf":
                    vrf = args[device][parameter]
                if parameter == "TxRxMode":
                    txrxmode = args[device][parameter]
                if parameter == "Enable":
                    enable = args[device][parameter]
                if parameter == "TranmitInterval":
                    tranmitinterval = args[device][parameter]
                if parameter == "SnoopAndDrop":
                    snoopandrop = args[device][parameter]

            swtch = FlexSwitch (DeviceIP, http_port, Username, Password)
            logger.info("updateLLDPGlobal():%s"%device)
            output = swtch.updateLLDPGlobal(Vrf=vrf,Enable=enable,TranmitInterval=tranmitinterval,TxRxMode=txrxmode,SnoopAndDrop=snoopanddrop)
            jData = json.loads(output.content)
            if ((jData['Result'] == "Success") or (jData['Result'] == "Error: Nothing to be updated.")):
                response = swtch.getAllLLDPGlobals()
                logger.info("LLDP GLOBAL OBJECT DETAILS:%s"%response)
                logger.info("LLDP Enabled on %s"%device)
                LLDPGlobalStatusList.update({device:"LLDP Enabled"})
            else:
                logger.debug("ERROR :%s"%jData['Result'])
                logger.info("LLDP not enabled in %s"%device)
	        LLDPGlobalStatusList.update({device:"None"})

        if "None" in LLDPGlobalStatusList.values():
            logger.info("ERROR : %s" %LLDPGlobalStatusList)
            return False
        else:
            return True
    else:
        logger.info("PLEASE PROVIDE ONE/MORE DEVICES")
        sys.exit(1)

"""
Procedure:
Description:
Sample Input:
args = {
       "DUT1" : ["fpPort45","fpPort55"],      //List of the ports of peer devices to which the DUT is connected
       "DUT2" : ["fpPort25"]
       }
"""

def verifyConnectivity(args=[]):
    alldetails = {}
    LLDPIntfList = []
    if args:
        for device in args:
	     DeviceIP = getMgmtIP(device)
	     Username = getUsername(device)
             if Username == "None" or Username == "":
                 Username = None
             Password = getPassword(device)
             if Password == "None" or  Password == "":
                 Password = None
        
             swtch = FlexSwitch (DeviceIP, http_port, Username, Password)
             logger.info("getAllLLDPIntfStates():%s"%device)
             output = swtch.getAllLLDPIntfStates()
             logger.info("LLDP INTF STATE DETAILS:%s"%output)
             for connectedDevices in output:
                 LLDPIntfList.append(connectedDevices["Object"]["PeerPort"])
             for expectedPort in args[device]:
                 if expectedPort not in LLDPIntfList:
                     alldetails.update({"%s_%s"%(device,expectedPort) : "Not Found"})
                 else:
                     alldetails.update({"%s_%s"%(device,expectedPort) : "Found"})
             LLDPIntfList = []
        logger.info(alldetails)
        if "Not Found" in alldetails.values():
            return False
        else:
            return True
    else:
        logger.info("PLEASE PROVIDE ONE/MORE DEVICES")
        sys.exit(1)




