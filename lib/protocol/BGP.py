#This file consists of all the API's for configuring and unconfiguring of BGP protocol
#These API's are capable of handling optional parameters that can be sent in the argument,
#default values are taken for all the parameters to which a value is not received.

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
Procedure   : updateBGPGlobal
Description : Dictionary of devices and parameters required for enabling BGPGlobal.
                   Enables BGP on devices. Collects the status of configuration and displays the final result with succeeded and failed configurations.
Sample input:
args = { 
          "DUT1" : {
           "Vrf"  :  "default"              string             `"KEY", ACCESS:"w", MULTIPLICITY:"1", AUTOCREATE: "true", DESCRIPTION: "VRF id for BGP global config", DEFAULT:"default"`
	   "ASNum" :  ""                    string             `DESCRIPTION: "Local AS for BGP global config. Both AsPlain and AsDot formats are supported.", DEFAULT: ""`
	   "RouterId" :  "0.0.0.0"          string             `DESCRIPTION: "Router id for BGP global config", DEFAULT: "0.0.0.0"`
	   "Disabled"  : False              bool               `DESCRIPTION: "Enable/Disable BGP globally", DEFAULT: False
	   "UseMultiplePaths" : False       bool               `DESCRIPTION: "Enable/disable ECMP for BGP", DEFAULT: False
	   "EBGPMaxPaths" : 0               uint32             `DESCRIPTION: "Max ECMP paths from External BGP neighbors", DEFAULT: 0
	   "EBGPAllowMultipleAS" : False    bool               `DESCRIPTION: "Enable/diable ECMP paths from multiple ASes", DEFAULT: False
	   "IBGPMaxPaths" :  0              uint32             `DESCRIPTION: "Max ECMP paths from Internal BGP neighbors", DEFAULT: 0
           "Redistribution" :  [ ]          [ ] SourcePolicyList `DESCRIPTION: "Provide redistribution policies for BGP from different sources", DEFAULT: [ ]
                        }
            }
"""
def updateBGPGlobal(args={}):

    vrf,asnum,routerid,usemultiplepaths,ebgpmaxpaths,ebgpallowmultipleas,disabled,ibgpmaxpaths,redistribution = "default", "","0.0.0.0", False, False, 0, False, 0,[]
        
    logger.info("*** ENABLING BGP GLOBAL ***")
    StatusList = {}
    if args:	
        for device in args:
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
                if parameter == "Disabled":
                    disabled = args[device][parameter]
                if parameter == "EBGPAllowMultipleAS":
                    ebgpallowmultipleas = args[device][parameter]
                if parameter == "EBGPMaxPaths":
                    ebgpmaxpaths = args[device][parameter]
                if parameter == "Redistribution":
                    redistribution = args[device][parameter]
                if parameter == "RouterId":
                    routerid = args[device][parameter]
                if parameter == "UseMultiplePaths":
                    usemultiplepaths = args[device][parameter] 
                if parameter == "ASNum":
                    asnum = args[device][parameter]
                if parameter == "IBGPMaxPaths":
                    ibgpmaxpaths = args[device][parameter]

            logger.info("Enabling BGP on device %s"%device)
            swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
            response = swtch.updateBGPGlobal(Vrf = vrf, 
                                             Disabled = disabled, 
                                             EBGPAllowMultipleAS = ebgpallowmultipleas, 
                                             EBGPMaxPaths = ebgpmaxpaths, 
                                             Redistribution = redistribution,  
                                             RouterId = routerid, 
                                             UseMultiplePaths = usemultiplepaths,
                                             ASNum = asnum, 
                                             IBGPMaxPaths = ibgpmaxpaths)
            jData = json.loads(response.content)
            if jData['Result'] == "Success":
	        logger.info("RESULT:%s"%jData['Result'])
                response = swtch.getAllBGPGlobals()
                logger.info("BGP GLOBAL OBJECT DETAILS:%s"%response)
                logger.info("BGP Global enabled on %s"%device)
                StatusList.update({device:"PASS"})
	    else:
	        logger.debug("ERROR :%s"%jData['Result'])
                StatusList.update({device:"FAIL"})
        if "FAIL" in StatusList.values():
            logger.info("%s"%StatusList)
            return False
        else:
            return True
    else:
        logger.info("PLEASE PROVIDE DEVICE AND REQUIRED PARAMETERS TO ENABLE BGP GLOBAL")
        sys.exit(1)
 
 
"""
Procedure   : createBGPv4Neighbor
Description : This procedure creates BGPv4 neighbor. Default values will be taken for parameters whose values are not sent in args
Arguments   : Dictionary of devices and parameters required for enabling BGPGlobal.
           Sets BGP Neighbor on devices. Collects the status of configuration and displays the final result with  succeeded and failed configurations.
	 :param string IntfRef : Interface of the BGP neighbor Interface of the BGP neighbor
         :param string NeighborAddress : Address of the BGP neighbor Address of the BGP neighbor
         :param string Description : Description of the BGP neighbor Description of the BGP neighbor
         :param string PeerGroup : Peer group of the BGP neighbor Peer group of the BGP neighbor
         :param string PeerAS : Peer AS of the BGP neighbor Peer AS of the BGP neighbor
         :param string LocalAS : Local AS of the BGP neighbor Local AS of the BGP neighbor
         :param string UpdateSource : Source IP to connect to the BGP neighbor Source IP to connect to the BGP neighbor
         :param string AuthPassword : Password to connect to the BGP neighbor Password to connect to the BGP neighbor
         :param string AdjRIBInFilter : Policy that is applied for Adj-RIB-In prefix filtering Policy that is applied for Adj-RIB-In prefix filtering
         :param string AdjRIBOutFilter : Policy that is applied for Adj-RIB-Out prefix filtering Policy that is applied for Adj-RIB-Out prefix filtering
         :param bool BfdEnable : Enable/Disable BFD for the BGP neighbor Enable/Disable BFD for the BGP neighbor
         :param uint8 MultiHopTTL : TTL for multi hop BGP neighbor TTL for multi hop BGP neighbor
         :param uint32 KeepaliveTime : Keep alive time for the BGP neighbor Keep alive time for the BGP neighbor
         :param bool AddPathsRx : Receive additional paths from BGP neighbor Receive additional paths from BGP neighbor
         :param bool RouteReflectorClient : Set/Clear BGP neighbor as a route reflector client Set/Clear BGP neighbor as a route reflector client
         :param uint8 MaxPrefixesRestartTimer : Time in seconds to wait before we start BGP peer session when we receive max prefixes Time in seconds to wait before  		 	   we start BGP peer session when we receive max prefixes
         :param bool MultiHopEnable : Enable/Disable multi hop for BGP neighbor Enable/Disable multi hop for BGP neighbor
         :param uint32 RouteReflectorClusterId : Cluster Id of the internal BGP neighbor route reflector client Cluster Id of the internal BGP neighbor route reflector client
         :param bool MaxPrefixesDisconnect : Disconnect the BGP peer session when we receive the max prefixes from the neighbor Disconnect the BGP peer session when we receive the 		  max prefixes from the neighbor
         :param uint8 AddPathsMaxTx : Max number of additional paths that can be transmitted to BGP neighbor Max number of additional paths that can be transmitted to BGP neighbor
         :param uint32 MaxPrefixes : Maximum number of prefixes that can be received from the BGP neighbor Maximum number of prefixes that can be received from the BGP neighbor
         :param uint8 MaxPrefixesThresholdPct : The percentage of maximum prefixes before we start logging The percentage of maximum prefixes before we start logging
         :param string BfdSessionParam : Bfd session param name to be applied Bfd session param name to be applied
         :param bool NextHopSelf : Use neighbor source IP as the next hop for IBGP neighbors Use neighbor source IP as the   next hop for IBGP neighbors
         :param bool Disabled : Enable/Disable the BGP neighbor Enable/Disable the BGP neighbor
         :param uint32 HoldTime : Hold time for the BGP neighbor Hold time for the BGP neighbor
         :param uint32 ConnectRetryTime : Connect retry time to connect to BGP neighbor after disconnect Connect retry time to connect to BGP neighbor after disconnect

Sample input:

args = {
 "DUT1":{      
    "Peer1":{
        "NeighborAddress" : None,
	"IntfRef" : None,
	"Description" : "",
	"Disabled" : False,
	"PeerGroup" : 0,
	"PeerAS" : 0,
	"LocalAS" : "",
	"UpdateSource" : "",
	"NextHopSelf" : False,
	"AuthPassword" : "",
	"RouteReflectorClusterId" : 0,
	"RouteReflectorClient" : False,
	"MultiHopEnable" : False,
	"MultiHopTTL" : 0,
	"ConnectRetryTime" : 0,
	"HoldTime" : 0,
	"KeepaliveTime" : 0,
	"AddPathsRx" : False,
	"AddPathsMaxTx" : 0,
	"BfdEnable" : False,
	"BfdSessionParam" : "default",
	"MaxPrefixes" : 0,
	"MaxPrefixesThresholdPct" : 80,
	"MaxPrefixesDisconnect" : False,
	"MaxPrefixesRestartTimer" : 0,
	"AdjRIBInFilter" : "",
        "AdjRIBOutFilter" : ""
                        }
               }
        }          
"""

def createBGPv4Neighbor(args={}):

    description,peergroup,peeras,localas,updatesource,authpassword,adjribinfilter,adjriboutfilter,bfdenable, multihopttl, keepalivetime, addpathsrx, routereflectorclient, maxprefixesrestarttimer, multihopenable, routereflectorclusterid, maxprefixesdisconnect, addpathsmaxtx, maxprefixes, maxprefixesthresholdpct, bfdsessionparam,nexthopself,disabled,holdtime, connectretrytime  ='','' ,'' ,'' ,'', '', '', '', False, 0, 0, False, False, 0, False, 0, False, 0, 0, 80, 'default', False, False, 0, 0
                                                  
    logger.info("*** CONFIGURING BGP NEIGHBORS ON DEVICES ***")
    StatusList = {}
    if args:
        for device in args.keys():
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None
            for Peer in args[device].keys():
                for parameter in args[device][Peer].keys():
                    if parameter == "NeighborAddress":
                        neighboraddress = args[device][Peer][parameter]
                    if parameter == "IntfRef":
                        intfref = args[device][Peer][parameter]
                    if parameter == "AdjRIBInFilter":
                        adjribinfilter = args[device][Peer][parameter]
                    if parameter == "AdjRIBOutFilter":
                        adjriboutfilter = args[device][Peer][parameter]
                    if parameter == "PeerAS":
                        peeras = args[device][Peer][parameter]
                    if parameter == "MaxPrefixesDisconnect":
                        maxprefixesdisconnect = args[device][Peer][parameter]
                    if parameter == "MaxPrefixesRestartTimer":
                        maxprefixesrestarttimer = args[device][Peer][parameter]
                    if parameter == "MultiHopTTL":
                        multihopttl = args[device][Peer][parameter]
                    if parameter == "LocalAS":
                        localas = args[device][Peer][parameter]
                    if parameter == "MaxPrefixesThresholdPct":
                        maxprefixesthresholdpct = args[device][Peer][parameter]
                    if parameter == "ConnectRetryTime":
                        connectretrytime = args[device][Peer][parameter]
                    if parameter == "Description":
                        description = args[device][Peer][parameter]
                    if parameter == "MaxPrefixes":
                        maxprefixes = args[device][Peer][parameter]
                    if parameter == "MultiHopEnable":
                        multihopenable = args[device][Peer][parameter]
                    if parameter == "RouteReflectorClient":
                        routereflectorclient = args[device][Peer][parameter]
                    if parameter == "AddPathsRx":
                        addpathsrx = args[device][Peer][parameter]
                    if parameter == "PeerGroup":
                        peergroup = args[device][Peer][parameter]
                    if parameter == "BfdSessionParam":
                        bfdsessionparam = args[device][Peer][parameter]
                    if parameter == "Disabled":
                        disabled = args[device][Peer][parameter]
                    if parameter == "NextHopSelf":
                        nexthopself = args[device][Peer][parameter]
                    if parameter == "RouteReflectorClusterId":
                        routereflectorclusterid = args[device][Peer][parameter]
                    if parameter == "AddPathsMaxTx":
                        addpathsmaxtx = args[device][Peer][parameter]
                    if parameter == "BfdEnable":
                        bfdenable = args[device][Peer][parameter]
                    if parameter == "KeepaliveTime":
                        keepalivetime = args[device][Peer][parameter]
                    if parameter == "UpdateSource":
                        updatesource = args[device][Peer][parameter]
                    if parameter == "AuthPassword":
                        authpassword = args[device][Peer][parameter]
                    if parameter == "HoldTime":
                        holdtime = args[device][Peer][parameter]          

                logger.info("Configuring BGP Neighbor on %s"%device)
                swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
                response = swtch.createBGPv4Neighbor(NeighborAddress=neighboraddress, IntfRef=intfref, AdjRIBInFilter=adjribinfilter, AdjRIBOutFilter=adjriboutfilter, PeerAS=peeras, MaxPrefixesDisconnect=maxprefixesdisconnect, MaxPrefixesRestartTimer=maxprefixesrestarttimer, MultiHopTTL=multihopttl, LocalAS=localas, MaxPrefixesThresholdPct=maxprefixesthresholdpct, ConnectRetryTime=connectretrytime, Description=description, MaxPrefixes=maxprefixes, MultiHopEnable=multihopenable, RouteReflectorClient=routereflectorclient, AddPathsRx=addpathsrx, PeerGroup=peergroup, BfdSessionParam=bfdsessionparam, Disabled=disabled, NextHopSelf=nexthopself, RouteReflectorClusterId=routereflectorclusterid, AddPathsMaxTx=addpathsmaxtx, BfdEnable=bfdenable, KeepaliveTime=keepalivetime, UpdateSource=updatesource, AuthPassword=authpassword, HoldTime=holdtime)
                jData = json.loads(response.content)
                logger.info(jData)
	        if jData['Result'] == "Success":
	            logger.info("RESULT:%s"%jData['Result'])
                    response = swtch.getAllBGPv4Neighbors()
                    logger.info("BGP NEIGHBOR OBJECT DETAILS:%s"%response)
                    logger.info("BGP Neighbor configured on %s"%device)
                    StatusList.update({device:"PASS"})
                elif jData['Result'] == "Error: Already configured. Delete and Update operations are allowed.":
	            logger.info("RESULT:%s"%jData['Result'])
                    logger.info("POLICY STATEMENT OBJECT DETAILS")
                    logger.info(swtch.getAllPolicyStmts())
                    logger.info("Policy Statement Added on %s"%device)
                    StatusList.update({device:"PASS"})
                else:
                    logger.info("BGP Neighbor not configured on %s"%device) 
	            StatusList.update({device:"FAIL"})
        if "FAIL" in StatusList.values():
            logger.info("%s" %StatusList)
            return False
        else:
            return True
    else:
        logger.info("PLEASE PROVIDE ONE/MORE DEVICE AND RELATED PARAMETERS INORDER TO CONFIGURE BGP NEIGHBORS ")
        sys.exit(1)
 
    
"""
Procedure   : deleteBGPv4Neighbor
Description : This procedure deletes BGPv4 neighbor. Default values will be taken for parameters whose values are not sent in args
Arguments   :	 
            : param string IntfRef : Interface of the BGP neighbor Interface of the BGP neighbor
            : param string NeighborAddress : Address of the BGP neighbor Address of the BGP neighbor 
Sample Input: 
args= { 
    "DUT1" : {
      "Peer1": {
        "NeighborAddress" : None,
	"IntfRef" : None,
	"Description" : "",
	"Disabled" : False,
	"PeerGroup" : 0,
	"PeerAS" : 0,
	"LocalAS" : "",
	"UpdateSource" : "",
	"NextHopSelf" : False,
	"AuthPassword" : "",
	"RouteReflectorClusterId" : 0,
	"RouteReflectorClient" : False,
	"MultiHopEnable" : False,
	"MultiHopTTL" : 0,
	"ConnectRetryTime" : 0,
	"HoldTime" : 0,
	"KeepaliveTime" : 0,
	"AddPathsRx" : False,
	"AddPathsMaxTx" : 0,
	"BfdEnable" : False,
	"BfdSessionParam" : "default",
	"MaxPrefixes" : 0,
	"MaxPrefixesThresholdPct" : 80,
	"MaxPrefixesDisconnect" : False,
	"MaxPrefixesRestartTimer" : 0,
	"AdjRIBInFilter" : "",
        "AdjRIBOutFilter" : ""
                }
           }
    }
"""
def deleteBGPv4Neighbor(args={}):
  
    neighboraddress,intfref,description,peergroup,peeras,localas,updatesource,authpassword,adjribinfilter,adjriboutfilter,bfdenable, multihopttl, keepalivetime, addpathsrx, routereflectorclient, maxprefixesrestarttimer, multihopenable, routereflectorclusterid, maxprefixesdisconnect, addpathsmaxtx, maxprefixes, maxprefixesthresholdpct, bfdsessionparam,nexthopself,disabled,holdtime, connectretrytime  = None,None,'','' ,'' ,'' ,'', '', '', '', False, 0, 0, False, False, 0, False, 0, False, 0, 0, 80, 'default', False, False, 0, 0
    logger.info("*** UNCONFIGURING BGP NEIGHBORS ON DEVICES ***")
    StatusList = {}
    if args:	
        for device in args:
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None
            for Peer in args[device].keys():
                for parameter in args[device][Peer].keys():
                    if parameter == "IntfRef":
                        intfref = args[device][Peer][parameter]
                    if parameter == "NeighborAddress":
                        neighboraddress = args[device][Peer][parameter]
                logger.info("Unconfiguring BGP Neighbors on device %s"%device)
                swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
                logger.info("%s.deleteBGPv4Neighbor(%s,%s)"%(device,intfref,neighboraddress))
                response = swtch.deleteBGPv4Neighbor(IntfRef=intfref,NeighborAddress=neighboraddress)
                jData = json.loads(response.content) 
	        if jData['Result'] == "Success":
	            logger.info("RESULT:%s"%jData['Result'])
                    response =swtch.getAllBGPv4Neighbors()
                    logger.info("BGP NEIGHBOR OBJECT DETAILS:%s"%response)
                    logger.info("BGP Neighbor unconfigured on %s"%device)
                    StatusList.update({device:"PASS"})
	        else:
	            logger.debug("ERROR :%s"%jData['Result'])
                    StatusList.update({device:"FAIL"})

        if "FAIL" in StatusList.values():
            logger.info("%s"%StatusList)
            return False
        else:
            return True

    else:
        logger.info("PLEASE PROVIDE DEVICE AND REQUIRED PARAMETERS TO UNCONFIGURE BGP NEIGHBORS")
        sys.exit(1)
  

"""
Procedure   : getBGPv4NeighborState
Description : This procedure gives the status of a BGP neighbor depending on the CheckParameter 
              sent in the args. Currently it can handle SessionState and support for other
              parameters can be added.
Arguments   :
            :param string Device : Device on which the BGP neighbor state must be checked
            :param string IntfRef : Interface of the BGP neighbor.
            :param string NeighborAddress : Address of the BGP neighbor.
            :param string CheckParameter : Parameter from the BGP neighbor state output which is to
                                           be checked.
            :param string ExpectedState : Expected state or value of the checkparameter.
Sample Input:
args = {
        "DUT1":{      
                "IntfRef" : "", [KEY]
                "NeighborAddr" : "", [KEY]
                "CheckParameter":"SessionState",
                "ExpectedState" : "ESTABLISHED"
                }
          }
"""
def getBGPv4NeighborState(args = {}):

    logger.info("*** CHECKING BGP NEIGHBOR STATUS ***")
    StatusList = []
    if args:
        for device in args.keys():
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            Password = getPassword(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None
            for peer in args[device].keys():
                intfref = args[device][peer]["IntfRef"]
                neighboraddress = args[device][peer]["NeighborAddress"]
                Parameter = args[device][peer]["CheckParameter"]
                logger.info("Checking BGP Neighbor Status on device %s"%device)
                swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
                logger.info ("getBGPv4NeighborState(%s,%s)"%(intfref,neighboraddress))
                response = swtch.getBGPv4NeighborState(IntfRef = intfref, NeighborAddress = neighboraddress)
                logger.info(response)
                jData = json.loads(response.content)
                logger.info(jData)
                if Parameter == "SessionState":
	            if str(response) == "<Response [200]>":
                        logger.info("BGP NEIGHBOR STATUS ON %s"%device)
                        if int(jData["Object"][Parameter]) == 1:
                            check = "IDLE"
                        elif int(jData["Object"][Parameter]) == 2:
                            check = "CONNECT"
                        elif int(jData["Object"][Parameter]) == 3:
                            check = "ACTIVE"
                        elif int(jData["Object"][Parameter]) == 4:
                            check = "OPENSENT"
                        elif int(jData["Object"][Parameter]) == 5:
                            check = "OPENCONFIRM"
                        elif int(jData["Object"][Parameter]) == 6:
                            check = "ESTABLISHED"
                        else:
                            check = "Unknown State"
                        logger.info("The BGP session state of peer %s is %s"%(peer,check))
                        if check == args[device][peer]["ExpectedState"]:
                            StatusList.append("EXPECTED")
                        else:
                            StatusList.append("NOT EXPECTED")
                    else:
                        StatusList.append("Neighbor Does Not Exist")
        logger.info(StatusList)
        if (("NOT EXPECTED" in StatusList) or ("Neighbor Does Not Exist" in StatusList)):
            return False
        else:
            return True
    else:
        logger.info("PLEASE PROVIDE DEVICE AND REQUIRED PARAMETERS TO GET BGP NEIGHBORS STATE")
        sys.exit(1)

"""
Procedure : getBGPv4Neighbor
Description : This procedure checks if a particular BGP neighbor 
Sample Input :
args = {

           "DUT1":{      
               "Peer1":{
                 "PeerAS":"201",
                 "NeighborAddress":"192.168.0.2",
                 "IntfRef":"fpPort25",
                        },
               "Peer2":{
                 "PeerAS":"204",
                 "NeighborAddress":"192.168.1.4",
                 "IntfRef":"fpPort65",
                       }
                    }
"""
def getBGPv4Neighbor(args = {}):

    logger.info("*** VERIFYING BGP NEIGHBOR CONFIGURATION ***")
    StatusList = {}
    if args:	
        for device in args:
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None
            
            for Peer in args[device].keys():
                for parameter in args[device][Peer].keys():
                    if parameter == "IntfRef":
                        intfref = args[device][Peer][parameter]
                    if parameter == "NeighborAddress":
                        neighboraddr = args[device][Peer][parameter]
                swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
                logger.info("%s.getBGPv4Neighbor(%s,%s)"%(device,intfref,neighboraddr))
                response = swtch.getBGPv4Neighbor(IntfRef = intfref, NeighborAddress = neighboraddr)
                logger.info("BGP NEIGHBOR OBJECT DETAILS:%s"%(json.loads(response.content)))
                if (str(response)) != "<Response [200]>":
                    StatusList.update({"%s[%s][%s][%s]"%(device,Peer,intfref,neighboraddr) : "FAIL"})
        	else:
                    StatusList.update({"%s[%s][%s][%s]"%(device,Peer,intfref,neighboraddr):"PASS"})
		
	if "FAIL" in StatusList.values():
            logger.info("%s"%StatusList)
            return False
        else:
            return True

    else:
        logger.info("PLEASE PROVIDE DEVICE AND REQUIRED PARAMETERS TO UNCONFIGURE BGP NEIGHBORS")
        sys.exit(1)
  
"""
Procedure   :createPolicyStmt
Description : This procedure creates policy statement. Default values are taken for optional parameters.
Arguments:param string Name : Policy Statement Name Policy Statement Name
         :param string Conditions : List of conditions added to this policy statement List of conditions
          added to this policy statement
         :param string Action : Action for this policy statement Action for this policy statement
         :param string MatchConditions : Specifies whether to match all/any of the conditions of this 
          policy statement Specifies whether to match all/any of the conditions of this policy statement.
Sample input:
args = {
           "DUT1":{      
                 "Name":"s1_permit",
                 "Action":"permit"
                  },
           "DUT2":{      
                 "Name":"s1_permit",
                 "Action":"permit"
                  }
       }
"""
def createPolicyStmt(args = {}):

    name, conditions, action, matchconditions = None,None,'deny','all'
    logger.info("*** CREATING POLICY STATEMENT ***")
    StatusList = {}
    if args:
        for device in args:
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None
            for parameter in args[device].keys():
                 if parameter == "Name":
                     name = args[device][parameter]
                 if parameter == "MatchConditions":
                     matchconditions = args[device][parameter]
                 if parameter == "Action":
                     action = args[device][parameter]
                 if parameter == "Conditions":
                     conditions = args[device][parameter] 
            swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
            response = swtch.createPolicyStmt(Name=name, MatchConditions=matchconditions, Action=action, Conditions=conditions)
            jData = json.loads(response.content)
            logger.info(jData)
	    if jData['Result'] == "Success":
	        logger.info("RESULT:%s"%jData['Result'])
                logger.info("POLICY STATEMENT OBJECT DETAILS")
                logger.info(swtch.getAllPolicyStmts())
                logger.info("Policy Statement Added on %s"%device)
                StatusList.update({device:"PASS"})
            elif jData['Result'] == "Error: Already configured. Delete and Update operations are allowed.":
	        logger.info("RESULT:%s"%jData['Result'])
                logger.info("POLICY STATEMENT OBJECT DETAILS")
                logger.info(swtch.getAllPolicyStmts())
                logger.info("Policy Statement Added on %s"%device)
                StatusList.update({device:"PASS"})
	    else:
	        logger.debug("ERROR :%s"%jData['Result'])
                StatusList.update({device:"FAIL"})

        if "FAIL" in StatusList.values():
            logger.info("%s" %StatusList)
            return False
        else:
            return True

    else:
        logger.info("PLEASE PROVIDE ONE/MORE DEVICE WITH RELATED PARAMETERS TO CONFIGURE POLICY STATEMENT")
        sys.exit(1)
 
"""
Procedure   : createPolicyDefinition
Description : This procedure creates policy definitions. Default values are taken for optional parameters.
Arguments :param string Name    : Policy Name Policy Name
          :param int32 Priority : Priority of the policy w.r.t other policies configured Priority of the policy 
                                  w.r.t other policies configured.
          :param PolicyDefinitionStmtPriority 
                  StatementList : Specifies list of statements along with their 
                                  precedence order. Specifies list of statements along with their precedence order.
          :param string MatchType : Specifies whether to match all/any of the statements within this policy 
                                  Specifies whether to match all/any of the statements within this policy.
          :param string PolicyType : Specifies the intended protocol application for the policy Specifies 
                                  the intended protocol application for the policy
Sample Input:
args ={ 
      "DUT1":{      
           "Name":"p1_match_all",
           "StatementList":[{"Priority":0,"Statement":"s1_permit"}]
             },
      "DUT2":{      
           "Name":"p1_match_all",
           "StatementList":[{"Priority":0,"Statement":"s1_permit"}]
             }
     }
"""
       
def createPolicyDefinition(args = {}):
   
    matchtype, policytype, priority, statementlist = "all","ALL",0,None
    logger.info("*** CREATING POLICY DEFINITION ***")
    StatusList = {}
    if args:
        for device in args:
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None

            for parameter in args[device].keys():
                if parameter == "Name":
                    name = args[device][parameter]
                if parameter == "MatchType":
                    matchtype = args[device][parameter]
                if parameter == "PolicyType":
                    policytype = args[device][parameter]
                if parameter == "Priority":
                    priority = args[device][parameter]
                if parameter == "StatementList":
                    statementlist = args[device][parameter]

            swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
            response = swtch.createPolicyDefinition(Name=name, MatchType=matchtype, PolicyType=policytype, Priority=priority, StatementList=statementlist)
            jData = json.loads(response.content)
            logger.info(jData)
	    if jData['Result'] == "Success":
	        logger.info("RESULT:%s"%jData['Result'])
                logger.info("POLICY DEFINITION OBJECT DETAILS")
                logger.info(swtch.getAllPolicyDefinitions())
                logger.info("Policy Defined on %s"%device)
                StatusList.update({device:"PASS"})
            elif jData['Result'] == "Error: Already configured. Delete and Update operations are allowed.":
	        logger.info("RESULT:%s"%jData['Result'])
                logger.info("POLICY STATEMENT OBJECT DETAILS")
                logger.info(swtch.getAllPolicyStmts())
                logger.info("Policy Statement Added on %s"%device)
                StatusList.update({device:"PASS"})
	    else:
	        logger.debug("ERROR :%s"%jData['Result'])
                StatusList.update({device:"FAIL"})

        if "FAIL" in StatusList.values():
            logger.info("%s" %StatusList)
            return False
        else:
            return True

    else:
        logger.info("PLEASE PROVIDE ONE/MORE DEVICE WITH RELATED PARAMETERS TO CONFIGURE POLICY DEFINITION")
        sys.exit(1)
 
"""
Procedure   : bgpRedistribution.
Description : This procedure redistributes BGP routes. Default values are sent for optional parameters.
Arguments   :{ 
        Vrf                 string             "KEY", ACCESS:"w", MULTIPLICITY:"1", AUTOCREATE: "true", DESCRIPTION: "VRF id for BGP global config", DEFAULT:"default"`
	ASNum               string             "Local AS for BGP global config. Both AsPlain and AsDot formats are supported.", DEFAULT: ""`
	RouterId            string             "Router id for BGP global config", DEFAULT: "0.0.0.0"`
	Disabled            bool               "Enable/Disable BGP globally", DEFAULT: "false"`
	UseMultiplePaths    bool               "Enable/disable ECMP for BGP", DEFAULT: "false"`
	EBGPMaxPaths        uint32             "Max ECMP paths from External BGP neighbors", DEFAULT: "0"`
	EBGPAllowMultipleAS bool               "Enable/diable ECMP paths from multiple ASes", DEFAULT: "false"`
	IBGPMaxPaths        uint32             "Max ECMP paths from Internal BGP neighbors", DEFAULT: "0"`
	Redistribution      []SourcePolicyList "Provide redistribution policies for BGP from different sources", DEFAULT: "[]"`
      }
Sample Input: 
args = {
          "DUT1":{
              "Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]},
          "DUT2":{
              "Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]}
       }
""" 

def bgpRedistribution(args={}):

    vrf,asnum,routerid,usemultiplepaths,ebgpmaxpaths,ebgpallowmultipleas,disabled,ibgpmaxpaths,redistribution = "default", "","0.0.0.0", False, False, 0, False, 0,[]
        
    logger.info("*** REDISTRIBUTING ROUTES INTO BGP ***")
    StatusList = {}
    if args:	
        for device in args:
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
                if parameter == "Disabled":
                    disabled = args[device][parameter]
                if parameter == "EBGPAllowMultipleAS":
                    ebgpallowmultipleas = args[device][parameter]
                if parameter == "EBGPMaxPaths":
                    ebgpmaxpaths = args[device][parameter]
                if parameter == "Redistribution":
                    redistribution = args[device][parameter]
                if parameter == "RouterId":
                    routerid = args[device][parameter]
                if parameter == "UseMultiplePaths":
                    usemultiplepaths = args[device][parameter] 
                if parameter == "ASNum":
                    asnum = args[device][parameter]
                if parameter == "IBGPMaxPaths":
                    ibgpmaxpaths = args[device][parameter]
            logger.info("Redistributing Routes into BGP on device %s"%device)
            swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
            response = swtch.updateBGPGlobal(Vrf = vrf, 
                                             Disabled = disabled, 
                                             EBGPAllowMultipleAS = ebgpallowmultipleas, 
                                             EBGPMaxPaths = ebgpmaxpaths, 
                                             Redistribution = redistribution,  
                                             RouterId = routerid, 
                                             UseMultiplePaths = usemultiplepaths,
                                             ASNum = asnum, 
                                             IBGPMaxPaths = ibgpmaxpaths)
            jData = json.loads(response.content)
            logger.info(jData)
	    if jData['Result'] == "Success":
	        logger.info("RESULT:%s"%jData['Result'])
                logger.info("BGP GLOBAL OBJECT(REDISTRIBUTION) DETAILS")
                logger.info(swtch.getAllBGPGlobals())
                logger.info("BGP Redistribution enabled on %s"%device)
                StatusList.update({device:"PASS"})
	    else:
	        logger.debug("ERROR :%s"%jData['Result'])
                StatusList.update({device:"FAIL"})

        if "FAIL" in StatusList.values():
            logger.info("%s"%StatusList)
            return False
        else:
            return True

    else:
        logger.info("PLEASE PROVIDE DEVICE AND REQUIRED PARAMETERS TO ENABLE BGP REDISTRIBUTION")
        sys.exit(1)



def getAllBGPv4RouteStates(args=[]):

    logger.info("*** CHECKING BGP ROUTE TABLE ***")
    StatusList = {}
    if args:	
        for device in args:
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None

            swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
            logger.info("%s.getAllBGPv4RouteStates()"%device)
            response = swtch.getAllBGPv4RouteStates()
            logger.info("BGP ROUTE OBJECT DETAILS:%s"%(response))
            if response:
                StatusList.update({"%s"%(device) : "PASS"})
            else:
                StatusList.update({"%s"%(device) :"FAIL"})
		
        if "FAIL" in StatusList.values():
            logger.info("%s"%StatusList)
            return False
        else:
            return True

    else:
        logger.info("PLEASE PROVIDE DEVICE AND REQUIRED PARAMETERS TO VERIFY ROUTES IN BGPV4 TABLE ")
        sys.exit(1)
  
            
def getAllIPv4RouteStates(args=[]):

    logger.info("*** CHECKING IP ROUTE TABLE ***")
    StatusList = {}
    if args:	
        for device in args:
            DeviceIP = getMgmtIP(device)
            Username = getUsername(device)
            if Username == "None" or Username == "":
                Username = None
            Password = getPassword(device)
            if Password == "None" or  Password == "":
                Password = None

            swtch = FlexSwitch(DeviceIP,http_port,Username,Password)
            logger.info("%s.getAllIPv4RouteStates()"%device)
            response = swtch.getAllIPv4RouteStates()
            logger.info("IPV4 ROUTE OBJECT DETAILS:%s"%(response))
            if response:
                StatusList.update({"%s"%(device) : "PASS"})
            else:
                StatusList.update({"%s"%(device) :"FAIL"})
		
	if "FAIL" in StatusList.values():
            logger.info("%s"%StatusList)
            return False
        else:
            return True

    else:
        logger.info("PLEASE PROVIDE DEVICE AND REQUIRED PARAMETERS TO VERIFY ROUTES IN IPV4 TABLE")
        sys.exit(1)
  
            







