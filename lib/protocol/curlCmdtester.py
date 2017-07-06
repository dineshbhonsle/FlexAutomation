import json
import subprocess
import re
import sys
from robot.api import logger
from os import path
from os.path import dirname, abspath
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from basic.getTestBed import *
from basic.configVariables import *

def execCURLCmd(device,URL,requestMethod,payload,ExpectedResponse):
    false = False
    true = True
    DeviceIP = getMgmtIP(device)
    Username = getUsername(device)
    Password = getPassword(device)
    if Username == "None" or Username == "":
        Username = None
    if Password == "None" or  Password == "":
        Password = None
    HOST = getMgmtIP(device)
    ports = getPortNames(device)
    try:
	payload_data = eval(payload)
	port = payload_data["IntfRef"]
        portDevice = re.match('(\w+)\_',port)
        portList = getPortNames(portDevice.group(1))
        if port not in portList:
            logger.info("The port %s does not exist for device %s"%(port,portDevice.group(1)))
            return False
	portName = getPortName(portDevice.group(1),port)
	payload = payload.replace(port,portName,1)
    except KeyError:
	pass
    try:
	payload_data = eval(payload)
	intfList = payload_data["IntfList"]
        for intf in intfList:
            portName = getPortName(device,intf)
            payload = payload.replace(intf,portName,1)
    except KeyError:
	pass
		    
    objURL = "%s://%s:%s%s"%(Protocol,HOST,Port,URL)
    if Protocol == "http":
        cmd = "curl -H "+ Headers + " -X " +requestMethod+  " -d " + "\'" + payload +"\'" +" "+ objURL
    else:
        cmd = "curl -k -u " + Username +":" +Password+ " -H "+ Headers + " -X " +requestMethod+  " -d " + "\'" + payload +"\'" +" "+ objURL
    logger.info("GENERATING %s REQUEST..."%requestMethod)
    response = exec_cmd(cmd,payload)
    logger.info("OBJECT DETAILS AFTER %s REQUEST:"%requestMethod)
    logger.info("%s"%response)
    logger.info("RESULT : %s"%response["Result"])
    logger.info("EXPECTED RESPONSE : %s"%ExpectedResponse)
    cleanString = re.sub('\W+',' ', response["Result"])
    res = re.search(ExpectedResponse, cleanString, re.M|re.I|re.X)
    if res:
        logger.info("RECEIVED RESPONSE IS SAME AS EXPECTED RESPONSE")
        logger.info("VALIDATING THE RESPONSE OF %s REQUEST BY ACCESSING GET OBJECT"%requestMethod)
        result = validate(cmd,payload)
        if result:
            return True
        else:
            return False
    else:
        logger.info("RECEIVED RESPONSE IS NOT SAME AS EXPECTED RESPONSE")
        return False
            

def exec_cmd(cmd,ignore_exception=False):
 
    """ execute command and return stdout output - None on error """

    try:
        false = False
        true = True
        logger.info("EXCECUTING COMMAND: %s" % cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        response = process.communicate()
        response = eval(response[0])
        return response 

    except subprocess.CalledProcessError as e:
        # exit code -2 seen on ctrl+c interrupt
        if e.returncode < 0: sys.exit("\nExiting...\n")
        if ignore_exception: 
            logger.debug("error executing cmd: %s" % e)
            logger.debug("stderr: %s" % e.response)
            return None
        logger.warn("error executing cmd: %s" % cmd)
        logger.warn("%s" % e.response)
        raise e

def validate(cmd,payload):

    false = False
    true = True
    cmd = cmd.replace("POST","GET",1)
    cmd = cmd.replace("PATCH","GET",1)
    cmd = cmd.replace("DELETE","GET",1)
    logger.info("GENERATING GET REQUEST...")
    response = exec_cmd(cmd)
    logger.info("OBJECT DETAILS AFTER GET REQUEST:")
    logger.info("%s"%response)
    logger.info("EXPECTED RESPONSE : UPDATION OF FOLLOWING KEY_VALUE PAIRS IN GET OBJECT")
    payload = eval(payload)
    logger.info(payload)
    try:
        for param in payload.keys():
            getObjValue = response["Object"][param]
            payloadValue = payload[param]
            logger.info("COMPARING VALUE OF PARAMETER \"%s\" IN GET OBJECT:\"%s\" AND IN PAYLOAD: \"%s\""%(param,getObjValue,payloadValue))
            if str(payload[param]) == str(getObjValue):
                logger.info("Comparison Passed")
                result = True
            else:
                logger.info("Comparison Failed")
                result = False

    except Exception as ex:
	logger.debug("Object does not exist")
        result = False
    return result
