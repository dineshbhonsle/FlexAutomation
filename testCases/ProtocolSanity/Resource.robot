*** Settings ***
Documentation    Resource file containing all the keyword definition from the TestSuite file.
...              This file integrates robot testcases and the python API for FlexSwitch.

Library		  ../../lib/basic/testBedScan.py
Library		  ../../lib/basic/topoValidation.py
Library           ../../lib/basic/IntfIPv4.py
Library           ../../lib/protocol/ARP.py
Library           ../../lib/protocol/LLDP.py
Library           ../../lib/protocol/BGP.py
Variables         config.py    
 
*** Keywords ***

Initial Setup
    [Documentation]    Initial setup where the testbed file scan is done to check for any errors and to check if the setup satisfies the minimum requirements for the Usecase.
    TestBed Scan
    GLOBAL_PRECHECK
    GLOBAL_PRECONFIG

GLOBAL_PRECHECK
    [Documentation]    Performs various checks to determine if the setup is as per the testbed file.
    Check Device Status 
    Check Port Status 
    Check Admin State Of Interfaces
    Check Link Status 

GLOBAL_PRECONFIG
    [Documentation]    Performs initial configurations.
    Configure IP address
    Validate IP Address configuration
    Check Link Status
    Check Admin State Of Interfaces 

TestBed Scan
    [Documentation]    Scans the testbed file for any syntax errors and also checks if the links and the ports description are defined correctly.
    ...                testbedCheck1:- Checks if the devices mentioned in the links exist in device list
    ...                            ex: Device list= [DUT1,DUT2]. correct: DUT1_DUT2_1 wrong: DUT1_DUT3_1
    ...                testbedCheck2:- Checks if the interface description mentioned for a link is correct.
    ...                            ex: Link = DUT1_DUT2_1.  
    ...                                Correct: DUT1 : {intf:DUT1_P1,speed: 40G}  wrong: DUT1 : {intf:DUT1_P1,speed: 40G}
    ...                                         DUT2 : {intf:DUT2_P1,speed: 40G}         DUT3 : {intf:DUT2_P1,speed: 40G}
    ...                testbedCheck3:- Checks if the management IP mentioned for the devices is a valid IP
    ...                                correct: 10.0.0.1   wrong: 10.0..1
    ...                testbedCheck4:- Checks if duplicate ports are mentioned for same interface in two links
    ...                testbedCheck5:- Checks if duplicate ports are mentioned for interfaces of same device in ports list
    ...                                Ex: correct: "ports"   : {                   wrong: "ports"   : {
    ...                                                    "D1_P1" : "fpPort25",                    "D1_P1" : "fpPort25",
    ...                                                    "D1_P2" : "fpPort65"}                    "D1_P2" : "fpPort25"}
    ${result}=    Run Keyword    testbedCheck1
    Run Keyword If    ${result}==False    FAIL       Devices defined in links do not match with the devices specified.
    ${result}=    Run Keyword     testbedCheck2      
    Run Keyword If    ${result}==False    FAIL       Interface description mentioned for a link is incorrect
    ${result}=    Run Keyword     testbedCheck3       
    Run Keyword If    ${result}==False    FAIL       Management IP mentioned for the devices is invalid 
    ${result}=    Run Keyword     testbedCheck4       
    Run Keyword If    ${result}==False    FAIL       Duplicate ports are mentioned for same interface in two links
    ${result}=    Run Keyword     testbedCheck5
    Run Keyword If    ${result}==False    FAIL       Duplicate ports are mentioned for interfaces of same device in ports list
	   
# GLOBAL_PRECHECK ###########################################################################       

Check Device Status
    [Documentation]    Checks if the devices mentioned in the testbed files are reachable.   

    ${result}=    Run Keyword    deviceStatus    
    Run Keyword If    ${result}==True    Log    All Devices are UP     
    ...    ELSE    ERROR    ${result}    Device does not exist
		
Check Port Status
    [Documentation]    Checks if all the ports mentioned for devices exists in the devices

    ${result}=    Run Keyword    portStatus    
    Run Keyword If    ${result}==True    Log    All ports are existing
    ...    ELSE    ERROR    ${result}     Interface does not exist 

Check Admin State Of Interfaces
    [Documentation]    Checks if the adminstate of interfaces on both the ends of the link is UP and
    ...                the operstate is UP.

    ${result}=    Run Keyword    adminStatus   
    Run Keyword If    ${result}==True    Log    All interfaces are Administratively UP    
    ...    ELSE    ERROR    ${result}    One/More Interface not UP 

Check Link Status
    [Documentation]    Checks if the Operational state of interfaces on both the ends of the link is UP 
    ...                and the operstate is UP.

    ${result}=    Run Keyword    linkStatus    
    Run Keyword If    ${result}==True    Log    All Links are UP    
    ...    ELSE    ERROR    ${result}     One/More Link not UP 

# GLOBAL_PRECONFIG ##########################################################################

Configure IP address
    [Documentation]    Configures IP address on the interfaces. 
    ...                Takes dictionary of device and ports as input.
    ${result}=    Run Keyword    createIPv4Intf      ${IntfIP}
    Run Keyword If    ${result}==True    Log    IP address Configured on given Interfaces     
    ...    ELSE    ERROR    ${result}    IP Address Configuration Failed 
 
Validate IP Address configuration
    [Documentation]    Checks if the interface is configures with IP and admistate is UP

    ${result}=    Run Keyword    getIPv4IntfState   ${IntfIPState}
    Run Keyword If    ${result}==True    Log    All interfaces are UP
    ...    ELSE    Notify    ${result}   One/More Interface Down  
    
# ARP ########################################################################################

Get ARP Entry Table
    [Documentation]    Displays all the connected devices learnt through ARP.

    ${result}=    Run Keyword    getAllArpLinuxEntryStates   ${ArpLinuxEntryStates}
    Log    ${result}

Verify ARP Entry Status After Link Is DOWN
    [Documentation]    Sets a port DOWN and checks if the entry was removed from ARP table.
 
    Set Port State    ${ARPtestDevice}    ${ARPtestPort}    ${PortStateDown}
    Check ARP Entry Is Removed    ${ARPtestDevice}    ${ARPIPAddr}
    Set Port State    ${ARPtestDevice}    ${ARPtestPort}    ${PortStateUp}
#   Sleep   ${ARPSleep}
#    ${result}=    Run Keyword    executeArpRefreshByIfName   ${ARPtestDevice}    ${ARPtestPort}
#   Run Keyword If    ${result}==True    Log    ARP Table Refreshed
# ...    ELSE    ERROR    ${result}   ARP Table was not Refreshed
#    Check ARP Entry Is Populated    ${ARPtestDevice}    ${ARPIPAddr} 

Check ARP Entry Is Removed
    [Arguments]    ${ARPtestDevice}    ${ARPIPAddr}
    ${result}=    Run Keyword    getArpLinuxEntryState   ${ARPtestDevice}  ${ARPIPAddr}    
    Run Keyword If    ${result}==False    Log    ARP Entry Deleted
    ...    ELSE    ERROR    ${result}   ARP Entry was not deleted
 
Check ARP Entry Is Populated
    [Arguments]    ${ARPtestDevice}    ${ARPIPAddr}
    ${result}=    Run Keyword    getAllArpLinuxEntryStates   ${ArpLinuxEntryState1}   
    Run Keyword If    ${result}==True    Log    ARP Entry Populated
    ...    ELSE    ERROR    ${result}   ARP Entry was not populated

# LLDP ########################################################################################

Configure LLDP Global
    [Documentation]    Configures LLDP Global

    ${result}=    Run Keyword    updateLLDPGlobal    ${LLDPGlobal}       
    Run Keyword If    ${result}==True    Log    LLDP Enabled on all devices   
    ...    ELSE    Notify    ${result}    One/more device is not enabled with LLDP 
    Sleep   ${LLDPSleep}

verify L1 connectivity
    [Documentation]    Sets one port down and checks if the connected device
    ...                does not exist in the LLDP learnt devices

    ${result}=    Run Keyword    verifyConnectivity    ${LLDPConnectivity}   
    Run Keyword If    ${result}==True    Log    LLDP Enabled on devices   
    ...    ELSE    Notify    ${result}    One/more device is not enabled with LLDP 

# BGP #########################################################################################
     
Configure BGP Global
    [Documentation]    Configures BGP Global
       
    ${result}=    Run Keyword    updateBGPGlobal    ${BGPGlobal}   
    Run Keyword If    ${result}==True    Log    BGP Global Configured     
    ...    ELSE    ERROR    ${result}    BGP Global Configuration Failed   

Configure BGPv4 Neighbors
    [Documentation]    Configures BGP neighbor. Takes input as dictionary of
    ...                devices and their peer's details.
       
    ${result}=    Run Keyword     createBGPv4Neighbor    ${BGPv4Neighbor}  
    Run Keyword If    ${result}==True    Log    BGP Neighbor configured on given devices    
    ...    ELSE    ERROR    ${result}    BGP Neighbors Configuration Failed
    Sleep   ${BGPConvergenceSleep}

Validate BGPv4 Neighbor configuration
    [Documentation]    Checks if all the neighbor state are in Expected state
       
    ${result}=    Run Keyword     getBGPv4NeighborState    ${BGPv4NeighborState}  
    Run Keyword If    ${result}==True    Log    All BGP Neighbors are UP    
    ...    ELSE    Notify    ${result}    BGP Neighbors Not UP 

Verify BGP Neighbor state after link flap
    [Documentation]    Checks if the neighbor state changes after link is set DOWN.

    Set Port State    ${BGPtestDevice}    ${BGPtestPort}    ${PortStateDown}
    Sleep   ${BGPConnectRetryTime}          
    Verify BGP Neighbor Session State    ${BGPv4TestDeviceNeighborState}
    Set Port State    ${BGPtestDevice}    ${BGPtestPort}    ${PortStateUp} 
    Sleep   ${BGPConvergenceSleep}
    Verify BGP Neighbor Session State    ${BGPv4TestDeviceNeighborState1}

Verify BGP Neighbor Session State
    [Documentation]    Checks if the neighbor state is as expected.
    [Arguments]    ${BGPv4NeighborState}
       
    ${result}=    Run Keyword and Continue on Failure     getBGPv4NeighborState    ${BGPv4NeighborState}  
    Run Keyword If    ${result}==True    Log    BGP Neighbor in expected state     
    ...    ELSE    Notify    ${result}    BGP Neighbor not in expected state
   
Redistribute connected interfaces
    [Documentation]    Creates policy statement and definition to apply redistribute
    ...                of connected routes.

    Create a Policy Stmt 
    Create a Policy Definition
    Update the BGPGlobal Object to redistribute CONNECTED routes using the PolicyDefinition

Create a Policy Definition
    [Documentation]    Creates Policy Definition.
  
    ${result}=    Run Keyword     createPolicyDefinition    ${PolicyDefinition}  
    Run Keyword If    ${result}==True    Log    Policy Definition Defined     
    ...    ELSE    ERROR    ${result}    Policy Definition Creation Error  

Create a Policy Stmt
    [Documentation]    Creates policy statement.

    ${result}=    Run Keyword     createPolicyStmt    ${PolicyStmt}  
    Run Keyword If    ${result}==True    Log    Policy Statement Defined     
    ...    ELSE    ERROR    ${result}    Policy Statement Creation Error
        
Update the BGPGlobal Object to redistribute CONNECTED routes using the PolicyDefinition
    [Documentation]    Redistribute CONNECTED routes using the PolicyDefinition

    ${result}=    Run Keyword     bgpRedistribution    ${BGPRedistribution}  
    Run Keyword If    ${result}==True    Log    BGPGlobal Object updated to redistribute CONNECTED routes using the PolicyDefinition 
    ...    ELSE    ERROR    ${result}    BGPGlobal(Redistribution) Object Updation Error

Verify routes in BGPv4 Route Table
    [Documentation]    Verify the routes are present in BGP Route Table
   
    ${result}=    Run Keyword     getAllBGPv4RouteStates    ${BGPRoute}
    Run Keyword If    ${result}==True    Log    Route to all desired destinations present
    ...    ELSE    ERROR    ${result}    Route to some destination not present                       

Verify routes in IPv4 Route Table
    [Documentation]    Verify the routes are present in BGP Route Table
    
    ${result}=    Run Keyword     getAllIPv4RouteStates    ${BGP_IPV4Route}
    Run Keyword If    ${result}==True    Log    Route to all desired destinations present
    ...    ELSE    ERROR    ${result}    Route to some destination not present          

CleanUp 
    Unconfigure BGP Neighbors
    UnConfigure IP address 

# CLEANUP #####################################################################################
UnConfigure IP address
    [Documentation]    Unconfigure IP address on interfaces

    ${result}=    Run Keyword and Continue on failure    deleteIPv4Intf    ${IntfIPDelete}   
    Run Keyword If    ${result}==True    Log    All devices have successfully unconfigured IP     
    ...    ELSE    Notify    ${result}    Unconfiguration of IP Failed   

Unconfigure BGP Neighbors
    [Documentation]    Unconfigure BGP Neighbors

    ${result}=    Run Keyword    updateBGPGlobal    ${BGPGlobal}   
    Run Keyword If    ${result}==True    Log    BGP Global Configured     
    ...    ELSE    ERROR    ${result}    BGP Global Configuration Failed 

    ${result}=    Run Keyword and Continue on failure   deleteBGPv4Neighbor    ${BGPv4Delete}      
    Run Keyword If    ${result}==True    Log    All devices have successfully unconfigured BGP Neighbors    
    ...    ELSE    Notify    ${result}    Unconfiguration of BGP Neighbors Failed  

# GLOBAL KEYWORDS #############################################################################

Notify
    [Arguments]    ${result}     ${msg}
    FAIL     ${msg}  

ERROR
    [Arguments]    ${result}     ${msg}
    FATAL ERROR     ${msg}  

Set Port State
        
    [Arguments]    ${testDevice}    ${testPort}    ${PortState} 
    ${result}=    Run Keyword    updatePort   ${testDevice}    ${testPort}    ${PortState} 
    Run Keyword If    ${result} == True     Log    Setting Port State Passed 
    ...    ELSE    Notify    ${result}    Setting Port State Failed  

