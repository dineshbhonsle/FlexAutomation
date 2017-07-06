#This file scans the testbed file for any syntax errors and also checks if the links and the ports description
#are defined correctly. It performs different checks on the testbed.json file.
import json
import re
import ipaddress
import sys
import os
from robot.api import logger

"""
Loads the testbed file from the env varaible.
"""
def load_testbed():
    try:
        json_data=open(os.environ["TESTBED"],"r")
	data=json.load(json_data)
        return data
    except IOError:
        sys.exit("Testbed file does not exist")
    except ValueError:
	sys.exit("Syntax_Error in Json File")
"""
Checks if the devices mentioned in the links exist in device list.
"""
def testbedCheck1():
    status = True
    data=load_testbed()
    Device_list=data["Device"].keys()
    Links_list=data["Links"].keys()
    for links in Links_list:
	SearchObj=re.search("(\w+)_(\w+)_",links)
	if SearchObj:
	    if (SearchObj.group(1) in Device_list) and (SearchObj.group(2) in Device_list):
                logger.info("Link %s is correctly defined." %(links))
	        continue
	    else:
                status = False
		logger.info("Link %s is not correctly defined as %s and/or %s do not exist in the device list %s." %(links,SearchObj.group(1),SearchObj.group(2),str(Device_list)))
	else:
            status = False
	    logger.info("Link %s is not defined correctly"%links)
    if status == False: 
        return False
    else:
        return True   
"""
Checks if the interface description mentioned for a link is correct.
"""
def testbedCheck2():
    status = True
    data=load_testbed()
    for link in data["Links"].keys():
        SearchObj=re.search("(\w+)_(\w+)_",link)
        link_list = [SearchObj.group(1),SearchObj.group(2)]
	intfs_list = data["Links"][link].keys()
        if (link_list[0] in intfs_list) and (link_list[1] in intfs_list):
            logger.info("Interfaces %s defined for link %s is correct"%(intfs_list, link))
            continue
        else:
            status = False
            logger.info("Interfaces %s defined for link %s is incorrect"%(intfs_list, link))
    if status == False: 
        return False
    else:
        return True   
"""
Checks if the management IP mentioned for the devices is a valid IP.
"""        
def testbedCheck3():
    status = True
    data=load_testbed()
    Links=data["Device"].keys()
    Links.sort()
    for devices in Links:
        link_list=data["Device"][devices]["mgmtIP"]
	try:
	    ipaddress.ip_network (unicode(link_list),strict=False)
            logger.info("Valid Management IP Address On %s :- %s"%(devices,link_list))
	except ValueError:
            status = False
	    logger.info("Invalid Management IP Address On %s :- %s"%(devices,link_list))
    if status == False: 
        return False
    else:
        return True   
"""
Checks if duplicate ports are mentioned for same interface in two links.
"""
def testbedCheck4():
    status = True
    data=load_testbed()
    devices = []
    Instance_PortList = []
    for link in data["Links"].keys():
	for device in data["Links"][link].keys():
	    devices.append(device)
	    Instance_PortList.append(data["Links"][link][device]["Intf"])
    x=zip(devices,Instance_PortList)
    for i in range(len(x)):
	for j in range(i+1, len(x)):
	    if x[i]==x[j]:
                status = False
	        logger.info("Duplicate port detected in the links for device %s for the link %s"%(x[j][0],x[j][1]))
            else:
                logger.info("No duplicate port detected in the links for device %s for the link %s"%(x[j][0],x[j][1]))
    if status == False: 
        return False
    else:
        return True   
"""
Checks if duplicate ports are mentioned for interfaces of same device in ports list.
"""
def testbedCheck5():
    status = True
    data=load_testbed()
    for device in data["Device"].keys():
	port_list=data["Device"][device]["ports"].values()
        for port in port_list:
	    count = port_list.count(port)  
	    if count > 1:
                status = False
	    	logger.info("Port %s is defined multiple times on device %s."%(port,device))
            else:
                logger.info("No duplicate for port %s found on device %s."%(port,device))
    if status == False: 
        return False
    else:
        return True   
               

