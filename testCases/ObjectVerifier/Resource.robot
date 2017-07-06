*** Settings ***
Documentation     Resource file containing all the keyword definition from the TestSuite file.
...                      This file integrates robot testcases and the python API for FlexSwitch.
Library           String
Library           ../../lib/protocol/curlCmdtester.py
Variables         config.py    
 
*** Keywords ***

Execute Curl Command
    [Arguments]    ${Host}    ${objURL}    ${reqMethod}    ${payload}    ${ExpectedResponse} 
    ${result}=    Run Keyword    execCurlCmd    ${Host}    ${objURL}    ${reqMethod}    ${payload}    ${ExpectedResponse}
    ${Object}=   Fetch From Right    ${objURL}    /
    Run Keyword If    ${result}==True    Log    ${reqMethod} request to ${Object} Was Successful
    ...    ELSE    FAIL    ${reqMethod} request to ${Object} Failed

Negative Test check
    [Arguments]    ${result}    ${objURL}    ${reqMethod}
    ${Object}=   Fetch From Right    ${objURL}    /
    Run Keyword If    ${result}==False    Log    ${reqMethod} request to ${Object} Was Successful
    ...    ELSE    FAIL    ${reqMethod} request to ${Object} Failed 

# INTERFACE 

IPv4Intf_IpAddr_TC1
    [Documentation]    This checks response for valid values passed
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${INTF1_objURL}    ${INTF1_reqMethod}    ${INTF1_payload}    ${INTF1_ExpectedResponse}    
    
IPv4Intf_IpAddr_TC2
    [Documentation]    Trying to configure IP on interface that is already configured
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${INTF2_objURL}    ${INTF2_reqMethod}    ${INTF2_payload}    ${INTF2_ExpectedResponse}     
    
IPv4Intf_IpAddr_TC3
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${INTF3_objURL}    ${INTF3_reqMethod}    ${INTF3_payload}    ${INTF3_ExpectedResponse}     
    
IPv4Intf_IpAddr_TC4
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${INTF4_objURL}    ${INTF4_reqMethod}    ${INTF4_payload}    ${INTF4_ExpectedResponse}     
    
IPv4Intf_AdminState_TC5
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${INTF5_objURL}    ${INTF5_reqMethod}    ${INTF5_payload}    ${INTF5_ExpectedResponse}      
    
IPv4Intf_AdminState_TC6
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${INTF6_objURL}    ${INTF6_reqMethod}    ${INTF6_payload}    ${INTF6_ExpectedResponse}          
    
IPv4Intf_IpAddr_TC7
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF7_objURL}    ${INTF7_reqMethod}    ${INTF7_payload}    ${INTF7_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF7_reqMethod}    ${INTF7_objURL}
    
IPv4Intf_IpAddr_TC8
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF8_objURL}    ${INTF8_reqMethod}    ${INTF8_payload}    ${INTF8_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF8_objURL}    ${INTF8_reqMethod}
    
IPv4Intf_IpAddr_TC9
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF9_objURL}    ${INTF9_reqMethod}    ${INTF9_payload}    ${INTF9_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF9_objURL}    ${INTF9_reqMethod}
    
IPv4Intf_IpAddr_TC10
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF10_objURL}    ${INTF10_reqMethod}    ${INTF10_payload}    ${INTF10_ExpectedResponse}    
    Run Keyword If    ${result}==False    Log    Found Expected Response
    ...    ELSE    FAIL    Object does not exist          
    
IPv4Intf_IntfRef_TC11
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF11_objURL}    ${INTF11_reqMethod}    ${INTF11_payload}    ${INTF11_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF11_objURL}    ${INTF11_reqMethod}
    
IPv4Intf_IpAddr_TC12
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF12_objURL}    ${INTF12_reqMethod}    ${INTF12_payload}    ${INTF12_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF12_objURL}    ${INTF12_reqMethod}
    
IPv4Intf_IpAddr_TC13
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF13_objURL}    ${INTF13_reqMethod}    ${INTF13_payload}    ${INTF13_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF13_objURL}    ${INTF13_reqMethod}
    
IPv4Intf_IpAddr_TC14
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF14_objURL}    ${INTF14_reqMethod}    ${INTF14_payload}    ${INTF14_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF14_objURL}    ${INTF14_reqMethod}
   
IPv4Intf_IpAddr_TC15
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF15_objURL}    ${INTF15_reqMethod}    ${INTF15_payload}    ${INTF15_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF15_objURL}    ${INTF15_reqMethod} 
    
IPv4Intf_IpAddr_TC16
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${INTF16_objURL}    ${INTF16_reqMethod}    ${INTF16_payload}    ${INTF16_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${INTF16_objURL}    ${INTF16_reqMethod}
   
# ARP
ArpGlobal_Timeout_TC1
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${ARP1_objURL}    ${ARP1_reqMethod}    ${ARP1_payload}    ${ARP1_ExpectedResponse}
    
ArpGlobal_Timeout_TC2
    [Tags]    tag1
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${ARP2_objURL}    ${ARP2_reqMethod}    ${ARP2_payload}    ${ARP2_ExpectedResponse}    
    

#LLDP

LLDPGlobal_Vrf_TC1
     Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP1_objURL}    ${LLDP1_reqMethod}    ${LLDP1_payload}    ${LLDP1_ExpectedResponse}    
     
LLDPGlobal_Vrf_TC2
     ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${LLDP2_objURL}    ${LLDP2_reqMethod}    ${LLDP2_payload}    ${LLDP2_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${LLDP2_objURL}    ${LLDP2_reqMethod}
   
LLDPGlobal_TranmitInterval_TC3
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP3_objURL}    ${LLDP3_reqMethod}    ${LLDP3_payload}    ${LLDP3_ExpectedResponse}    
	
LLDPGlobal_TranmitInterval_TC4
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP4_objURL}    ${LLDP4_reqMethod}    ${LLDP4_payload}    ${LLDP4_ExpectedResponse} 

LLDPGlobal_TxRxMode_TC5
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP5_objURL}    ${LLDP5_reqMethod}    ${LLDP5_payload}    ${LLDP5_ExpectedResponse} 

LLDPGlobal_TxRxMode_TC6
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP6_objURL}    ${LLDP6_reqMethod}    ${LLDP6_payload}    ${LLDP6_ExpectedResponse} 

LLDPGlobal_TxRxMode_TC7
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP7_objURL}    ${LLDP7_reqMethod}    ${LLDP7_payload}    ${LLDP7_ExpectedResponse} 

LLDPGlobal_SnoopAndDrop_TC8
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP8_objURL}    ${LLDP8_reqMethod}    ${LLDP8_payload}    ${LLDP8_ExpectedResponse} 

LLDPGlobal_SnoopAndDrop_TC9
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP9_objURL}    ${LLDP9_reqMethod}    ${LLDP9_payload}    ${LLDP9_ExpectedResponse}

LLDPGlobal_Enable_TC10
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP10_objURL}    ${LLDP10_reqMethod}    ${LLDP10_payload}    ${LLDP10_ExpectedResponse}

LLDPGlobal_Enable_TC11
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP11_objURL}    ${LLDP11_reqMethod}    ${LLDP11_payload}    ${LLDP11_ExpectedResponse}

LLDPGlobal_Enable_TC12
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP12_objURL}    ${LLDP12_reqMethod}    ${LLDP12_payload}    ${LLDP12_ExpectedResponse}

LLDPIntf_IntfRef_TC13
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP13_objURL}    ${LLDP13_reqMethod}    ${LLDP13_payload}    ${LLDP13_ExpectedResponse}

LLDPIntf_IntfRef_TC14
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${LLDP14_objURL}    ${LLDP14_reqMethod}    ${LLDP14_payload}    ${LLDP14_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${LLDP14_objURL}    ${LLDP14_reqMethod}

LLDPIntf_TxRxMode_TC15
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP15_objURL}    ${LLDP15_reqMethod}    ${LLDP15_payload}    ${LLDP15_ExpectedResponse}    

LLDPIntf_TxRxMode_TC16
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP16_objURL}    ${LLDP16_reqMethod}    ${LLDP16_payload}    ${LLDP16_ExpectedResponse}    
	
LLDPIntf_TxRxMode_TC17
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP17_objURL}    ${LLDP17_reqMethod}    ${LLDP17_payload}    ${LLDP17_ExpectedResponse}    
	
LLDPIntf_Enable_TC18
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP18_objURL}    ${LLDP18_reqMethod}    ${LLDP18_payload}    ${LLDP18_ExpectedResponse}    
	
LLDPIntf_Enable_TC19
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LLDP19_objURL}    ${LLDP19_reqMethod}    ${LLDP19_payload}    ${LLDP19_ExpectedResponse}    
	



# Loopback
LogicalIntf_Name_TC1
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LO1_objURL}    ${LO1_reqMethod}    ${LO1_payload}    ${LO1_ExpectedResponse}    
	
LogicalIntf_Name_TC2
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${LO2_objURL}    ${LO2_reqMethod}    ${LO2_payload}    ${LO2_ExpectedResponse}   
	
LogicalIntf_Name_TC3
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${LO3_objURL}    ${LO3_reqMethod}    ${LO3_payload}    ${LO3_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${LO3_objURL}    ${LO3_reqMethod}    

LogicalIntf_Name_TC4
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${LO4_objURL}    ${LO4_reqMethod}    ${LO4_payload}    ${LO4_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${LO4_objURL}    ${LO4_reqMethod}

# VLAN
Vlan_VlanId_TC1
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${VLAN1_objURL}    ${VLAN1_reqMethod}    ${VLAN1_payload}    ${VLAN1_ExpectedResponse}  

Vlan_IntfList_TC2
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}    ${VLAN2_objURL}    ${VLAN2_reqMethod}    ${VLAN2_payload}    ${VLAN2_ExpectedResponse}    
    
Vlan_IntfList_TC3
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${VLAN3_objURL}    ${VLAN3_reqMethod}    ${VLAN3_payload}    ${VLAN3_ExpectedResponse}

Vlan_Description_TC4
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${VLAN4_objURL}    ${VLAN4_reqMethod}    ${VLAN4_payload}    ${VLAN4_ExpectedResponse}

Vlan_AdminState_TC5
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${VLAN5_objURL}    ${VLAN5_reqMethod}    ${VLAN5_payload}    ${VLAN5_ExpectedResponse}

Vlan_AdminState_TC6
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${VLAN6_objURL}    ${VLAN6_reqMethod}    ${VLAN6_payload}    ${VLAN6_ExpectedResponse}

Vlan_VlanId_TC7
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${VLAN7_objURL}    ${VLAN7_reqMethod}    ${VLAN7_payload}    ${VLAN7_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${VLAN7_objURL}    ${VLAN7_reqMethod}

# BGP CONFIGURATION ######################################################

BGPGlobal_Vrf_TC1
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP1_objURL}    ${BGP1_reqMethod}    ${BGP1_payload}    ${BGP1_ExpectedResponse}    
    
BGPGlobal_Vrf_TC2
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP2_objURL}    ${BGP2_reqMethod}    ${BGP2_payload}    ${BGP2_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP2_objURL}    ${BGP2_reqMethod}
BGPGlobal_ASNum_TC3
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP3_objURL}    ${BGP3_reqMethod}    ${BGP3_payload}    ${BGP3_ExpectedResponse}    
    
BGPGlobal_RouterId_TC4
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP4_objURL}    ${BGP4_reqMethod}    ${BGP4_payload}    ${BGP4_ExpectedResponse}    
   
BGPGlobal_RouterId_TC5
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP5_objURL}    ${BGP5_reqMethod}    ${BGP5_payload}    ${BGP5_ExpectedResponse}    
   
BGPGlobal_EBGPAllowMultipleAS_TC6
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP6_objURL}    ${BGP6_reqMethod}    ${BGP6_payload}    ${BGP6_ExpectedResponse}    
    
BGPGlobal_EBGPAllowMultipleAS_TC7
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP7_objURL}    ${BGP7_reqMethod}    ${BGP7_payload}    ${BGP7_ExpectedResponse}    
    
BGPGlobal_EBGPAllowMultipleAS_TC8
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP8_objURL}    ${BGP8_reqMethod}    ${BGP8_payload}    ${BGP8_ExpectedResponse} 
    
BGPGlobal_UseMultiplePaths_TC9
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP9_objURL}    ${BGP9_reqMethod}    ${BGP9_payload}    ${BGP9_ExpectedResponse}    
    
BGPGlobal_UseMultiplePaths_TC10
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP10_objURL}    ${BGP10_reqMethod}    ${BGP10_payload}    ${BGP10_ExpectedResponse}    
    
BGPGlobal_UseMultiplePaths_TC11
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP11_objURL}    ${BGP11_reqMethod}    ${BGP11_payload}    ${BGP11_ExpectedResponse}    
    
BGPGlobal_IBGPMaxPaths_TC12
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP12_objURL}    ${BGP12_reqMethod}    ${BGP12_payload}    ${BGP12_ExpectedResponse}    
    
BGPGlobal_IBGPMaxPaths_TC13
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP13_objURL}    ${BGP13_reqMethod}    ${BGP13_payload}    ${BGP13_ExpectedResponse}    
    
BGPGlobal_IBGPMaxPaths_TC14
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP14_objURL}    ${BGP14_reqMethod}    ${BGP14_payload}    ${BGP14_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP14_objURL}    ${BGP14_reqMethod}
   
BGPGlobal_EBGPMaxPaths_TC15
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP15_objURL}    ${BGP15_reqMethod}    ${BGP15_payload}    ${BGP15_ExpectedResponse}    
    
BGPGlobal_EBGPMaxPaths_TC16
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP16_objURL}    ${BGP16_reqMethod}    ${BGP16_payload}    ${BGP16_ExpectedResponse}    
    
BGPGlobal_EBGPMaxPaths_TC17
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP17_objURL}    ${BGP17_reqMethod}    ${BGP17_payload}    ${BGP17_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP17_objURL}    ${BGP17_reqMethod}
    
BGPGlobal_Disabled_TC18
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP18_objURL}    ${BGP18_reqMethod}    ${BGP18_payload}    ${BGP18_ExpectedResponse}    
    
BGPGlobal_Disabled_TC19
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP19_objURL}    ${BGP19_reqMethod}    ${BGP19_payload}    ${BGP19_ExpectedResponse}    
    
BGPGlobal_Disabled_TC20
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${BGP20_objURL}    ${BGP20_reqMethod}    ${BGP20_payload}    ${BGP20_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${BGP20_objURL}    ${BGP20_reqMethod}
    
BGPv4Neighbor_NeighborAddress_TC21
    Run Keyword and continue on Failure    Execute Curl Command       ${DUT1}    ${BGP21_objURL}    ${BGP21_reqMethod}    ${BGP21_payload}    ${BGP21_ExpectedResponse}    
    
BGPv4Neighbor_NeighborAddress_TC22
    Run Keyword and continue on Failure    Execute Curl Command       ${DUT1}    ${BGP22_objURL}    ${BGP22_reqMethod}    ${BGP22_payload}    ${BGP22_ExpectedResponse}
    
BGPv4Neighbor_NeighborAddress_TC23
     ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}       ${BGP23_objURL}    ${BGP23_reqMethod}    ${BGP23_payload}    ${BGP23_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}       ${BGP23_objURL}    ${BGP23_reqMethod}
    
BGPv4Neighbor_NeighborAddress_TC24
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP24_objURL}    ${BGP24_reqMethod}    ${BGP24_payload}    ${BGP24_ExpectedResponse} 
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP24_objURL}    ${BGP24_reqMethod}
     
BGPv4Neighbor_NeighborAddress_TC25
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP25_objURL}    ${BGP25_reqMethod}    ${BGP25_payload}    ${BGP25_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP25_objURL}    ${BGP25_reqMethod}
  
BGPv4Neighbor_NeighborAddress_TC26
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP26_objURL}    ${BGP26_reqMethod}    ${BGP26_payload}    ${BGP26_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP26_objURL}    ${BGP26_reqMethod}
  
BGPv4Neighbor_IntfRef_TC27
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP27_objURL}    ${BGP27_reqMethod}    ${BGP27_payload}    ${BGP27_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP27_objURL}    ${BGP27_reqMethod}

BGPv4Neighbor_PeerAS_TC28
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP28_objURL}    ${BGP28_reqMethod}    ${BGP28_payload}    ${BGP28_ExpectedResponse}   

BGPv4Neighbor_AuthPassword _TC29
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP29_objURL}    ${BGP29_reqMethod}    ${BGP29_payload}    ${BGP29_ExpectedResponse}   

BGPv4Neighbor_MaxPrefixesDisconnect _TC30
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP30_objURL}    ${BGP30_reqMethod}    ${BGP30_payload}    ${BGP30_ExpectedResponse}   

BGPv4Neighbor_MaxPrefixesDisconnect _TC31
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP31_objURL}    ${BGP31_reqMethod}    ${BGP31_payload}    ${BGP31_ExpectedResponse}   

BGPv4Neighbor_MaxPrefixesDisconnect _TC32
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP32_objURL}    ${BGP32_reqMethod}    ${BGP32_payload}    ${BGP32_ExpectedResponse}   

BGPv4Neighbor_LocalAS _TC33
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP33_objURL}    ${BGP33_reqMethod}    ${BGP33_payload}    ${BGP33_ExpectedResponse}   

BGPv4Neighbor_MaxPrefixesThresholdPct _TC34
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP34_objURL}    ${BGP34_reqMethod}    ${BGP34_payload}    ${BGP34_ExpectedResponse}   

BGPv4Neighbor_MaxPrefixesThresholdPct _TC35
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP35_objURL}    ${BGP35_reqMethod}    ${BGP35_payload}    ${BGP35_ExpectedResponse}   

BGPv4Neighbor_MaxPrefixesThresholdPct _TC36
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}       ${BGP36_objURL}    ${BGP36_reqMethod}    ${BGP36_payload}    ${BGP36_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}       ${BGP36_objURL}    ${BGP36_reqMethod}

BGPv4Neighbor_PeerGroup_TC37
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}       ${BGP37_objURL}    ${BGP37_reqMethod}    ${BGP37_payload}    ${BGP37_ExpectedResponse}   

BGPv4Neighbor_Description_TC38
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP38_objURL}    ${BGP38_reqMethod}    ${BGP38_payload}    ${BGP38_ExpectedResponse}   

BGPv4Neighbor_MultiHopEnable_TC39
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP39_objURL}    ${BGP39_reqMethod}    ${BGP39_payload}    ${BGP39_ExpectedResponse}   

BGPv4Neighbor_MultiHopEnable_TC40
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP40_objURL}    ${BGP40_reqMethod}    ${BGP40_payload}    ${BGP40_ExpectedResponse}   

BGPv4Neighbor_MultiHopEnable_TC41
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP41_objURL}    ${BGP41_reqMethod}    ${BGP41_payload}    ${BGP41_ExpectedResponse}   

BGPv4Neighbor_RouteReflectorClient_TC42
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP42_objURL}    ${BGP42_reqMethod}    ${BGP42_payload}    ${BGP42_ExpectedResponse}   

BGPv4Neighbor_RouteReflectorClient_TC43
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP43_objURL}    ${BGP43_reqMethod}    ${BGP43_payload}    ${BGP43_ExpectedResponse}   

BGPv4Neighbor_RouteReflectorClient_TC44
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP44_objURL}    ${BGP44_reqMethod}    ${BGP44_payload}    ${BGP44_ExpectedResponse}   

BGPv4Neighbor_NextHopSelf_TC45
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP45_objURL}    ${BGP45_reqMethod}    ${BGP45_payload}    ${BGP45_ExpectedResponse}   

BGPv4Neighbor_NextHopSelf_TC46
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP46_objURL}    ${BGP46_reqMethod}    ${BGP46_payload}    ${BGP46_ExpectedResponse}   

BGPv4Neighbor_NextHopSelf_TC47
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP47_objURL}    ${BGP47_reqMethod}    ${BGP47_payload}    ${BGP47_ExpectedResponse}   

BGPv4Neighbor_Disabled_TC48
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP48_objURL}    ${BGP48_reqMethod}    ${BGP48_payload}    ${BGP48_ExpectedResponse}   

BGPv4Neighbor_Disabled_TC49
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP49_objURL}    ${BGP49_reqMethod}    ${BGP49_payload}    ${BGP49_ExpectedResponse}   

BGPv4Neighbor_Disabled_TC50
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP50_objURL}    ${BGP50_reqMethod}    ${BGP50_payload}    ${BGP50_ExpectedResponse}   

BGPv4Neighbor_NeighborAddress_TC51
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP51_objURL}    ${BGP51_reqMethod}    ${BGP51_payload}    ${BGP51_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP51_objURL}    ${BGP51_reqMethod}

BGPv4Neighbor_NeighborAddress_TC52
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}        ${BGP52_objURL}    ${BGP52_reqMethod}    ${BGP52_payload}    ${BGP52_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}        ${BGP52_objURL}    ${BGP52_reqMethod} 


BGPv4Neighbor_NeighborAddress_TC53
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP53_objURL}    ${BGP53_reqMethod}    ${BGP53_payload}    ${BGP53_ExpectedResponse}  
    
BGPv4Neighbor_NeighborAddress_TC54
    Run Keyword and continue on Failure    Execute Curl Command    ${DUT1}        ${BGP54_objURL}    ${BGP54_reqMethod}    ${BGP54_payload}    ${BGP54_ExpectedResponse}   

#Clean UP ##################################################################

Clean UP 
 
   IPv4Intf_CLEAN_TC1
   IPv4Intf_CLEAN_TC2
   BGPGlobal_CLEAN_TC3
   BGPGlobal_CLEAN_TC4
   BGPv4Neighbor_CLEAN_TC5
   LLDPGlobal_CLEAN_TC6
   LLDPIntf_CLEAN_TC7
   ArpGlobal_CLEAN_TC8

IPv4Intf_CLEAN_TC1
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${CP1_objURL}    ${CP1_reqMethod}    ${CP1_payload}    ${CP1_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${CP1_objURL}    ${CP1_reqMethod}
    
IPv4Intf_CLEAN_TC2
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${CP2_objURL}    ${CP2_reqMethod}    ${CP2_payload}    ${CP2_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${CP2_objURL}    ${CP2_reqMethod} 
    
BGPGlobal_CLEAN_TC3
    Run Keyword and continue on Failure    Execute Curl Command     ${DUT1}        ${CP3_objURL}    ${CP3_reqMethod}    ${CP3_payload}    ${CP3_ExpectedResponse}    
    
BGPGlobal_CLEAN_TC4
    Run Keyword and continue on Failure    Execute Curl Command     ${DUT1}        ${CP4_objURL}    ${CP4_reqMethod}    ${CP4_payload}    ${CP4_ExpectedResponse}   

BGPv4Neighbor_CLEAN_TC5
    ${result}=    Run Keyword and continue on Failure    execCurlCmd    ${DUT1}    ${CP5_objURL}    ${CP5_reqMethod}    ${CP5_payload}    ${CP5_ExpectedResponse}
    Run Keyword and continue on Failure    Negative Test check     ${result}    ${CP5_objURL}    ${CP5_reqMethod}
 
LLDPGlobal_CLEAN_TC6
    Run Keyword and continue on Failure    Execute Curl Command     ${DUT1}        ${CP6_objURL}    ${CP6_reqMethod}    ${CP6_payload}    ${CP6_ExpectedResponse}  

LLDPIntf_CLEAN_TC7
    Run Keyword and continue on Failure    Execute Curl Command     ${DUT1}        ${CP7_objURL}    ${CP7_reqMethod}    ${CP7_payload}    ${CP7_ExpectedResponse}  

ArpGlobal_CLEAN_TC8
    Run Keyword and continue on Failure    Execute Curl Command     ${DUT1}        ${CP8_objURL}    ${CP8_reqMethod}    ${CP8_payload}    ${CP8_ExpectedResponse}  
