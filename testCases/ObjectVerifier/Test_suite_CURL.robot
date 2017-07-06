*** Settings ***

Documentation	        A test suite with tests to verify object model implementation on Flexswitch
Metadata 		Version          	 1.0
...	         	More Info         	 For more information about Robot Framework see http://robotframework.org
...               	Author            	
...               	Date             	   
...	                Executed At  	         ${HOST}
...		        Test Framework           Robot Framework Python

Resource          	Resource.robot
Suite Teardown     Clean up

*** Test Cases ***

Interface Configuration Tests
  
    IPv4Intf_IpAddr_TC1
    IPv4Intf_IpAddr_TC2
    IPv4Intf_IpAddr_TC3
    IPv4Intf_IpAddr_TC4
    IPv4Intf_AdminState_TC5
    IPv4Intf_AdminState_TC6
    IPv4Intf_IpAddr_TC7
    IPv4Intf_IpAddr_TC8
    IPv4Intf_IpAddr_TC9
    IPv4Intf_IpAddr_TC10
    IPv4Intf_IntfRef_TC11
    IPv4Intf_IpAddr_TC12
    IPv4Intf_IpAddr_TC13
    IPv4Intf_IpAddr_TC14
    IPv4Intf_IpAddr_TC15
    IPv4Intf_IpAddr_TC16

ARP Configuration Tests

    ArpGlobal_Timeout_TC1
    ArpGlobal_Timeout_TC2

LLDP Configuration Tests
   
    LLDPGlobal_Vrf_TC1
    LLDPGlobal_Vrf_TC2
    LLDPGlobal_TranmitInterval_TC3
    LLDPGlobal_TranmitInterval_TC4
    LLDPGlobal_TxRxMode_TC5
    LLDPGlobal_TxRxMode_TC6
    LLDPGlobal_TxRxMode_TC7
    LLDPGlobal_SnoopAndDrop_TC8
    LLDPGlobal_SnoopAndDrop_TC9
    LLDPGlobal_Enable_TC10
    LLDPGlobal_Enable_TC11
    LLDPGlobal_Enable_TC12
    LLDPIntf_IntfRef_TC13
    LLDPIntf_IntfRef_TC14
    LLDPIntf_TxRxMode_TC15
    LLDPIntf_TxRxMode_TC16
    LLDPIntf_TxRxMode_TC17
    LLDPIntf_Enable_TC18
    LLDPIntf_Enable_TC19
    

Loopback Configuration Tests
    LogicalIntf_Name_TC1
    LogicalIntf_Name_TC2
    LogicalIntf_Name_TC3
    LogicalIntf_Name_TC4

VLAN Configuration Tests
    Vlan_VlanId_TC1
    Vlan_IntfList_TC2
    Vlan_IntfList_TC3
    Vlan_Description_TC4
    Vlan_AdminState_TC5
    Vlan_AdminState_TC6
    Vlan_VlanId_TC7


BGP Configuration Tests
     
    BGPGlobal_Vrf_TC1
    BGPGlobal_Vrf_TC2
    BGPGlobal_ASNum_TC3
    BGPGlobal_RouterId_TC4
    BGPGlobal_RouterId_TC5
    BGPGlobal_EBGPAllowMultipleAS_TC6
    BGPGlobal_EBGPAllowMultipleAS_TC7
    BGPGlobal_EBGPAllowMultipleAS_TC8
    BGPGlobal_UseMultiplePaths_TC9
    BGPGlobal_UseMultiplePaths_TC10
    BGPGlobal_UseMultiplePaths_TC11
    BGPGlobal_IBGPMaxPaths_TC12
    BGPGlobal_IBGPMaxPaths_TC13
    BGPGlobal_IBGPMaxPaths_TC14
    BGPGlobal_EBGPMaxPaths_TC15
    BGPGlobal_EBGPMaxPaths_TC16
    BGPGlobal_EBGPMaxPaths_TC17
    BGPGlobal_Disabled_TC18
    BGPGlobal_Disabled_TC19
    BGPGlobal_Disabled_TC20
    BGPv4Neighbor_NeighborAddress_TC21
    BGPv4Neighbor_NeighborAddress_TC22
    BGPv4Neighbor_NeighborAddress_TC23
    BGPv4Neighbor_NeighborAddress_TC24
    BGPv4Neighbor_NeighborAddress_TC25
    BGPv4Neighbor_NeighborAddress_TC26
    BGPv4Neighbor_IntfRef_TC27
    BGPv4Neighbor_PeerAS_TC28
    BGPv4Neighbor_AuthPassword _TC29
    BGPv4Neighbor_MaxPrefixesDisconnect _TC30
    BGPv4Neighbor_MaxPrefixesDisconnect _TC31
    BGPv4Neighbor_MaxPrefixesDisconnect _TC32
    BGPv4Neighbor_LocalAS _TC33
    BGPv4Neighbor_MaxPrefixesThresholdPct _TC34
    BGPv4Neighbor_MaxPrefixesThresholdPct _TC35
    BGPv4Neighbor_MaxPrefixesThresholdPct _TC36
    BGPv4Neighbor_PeerGroup_TC37
    BGPv4Neighbor_Description_TC38
    BGPv4Neighbor_MultiHopEnable_TC39
    BGPv4Neighbor_MultiHopEnable_TC40
    BGPv4Neighbor_MultiHopEnable_TC41
    BGPv4Neighbor_RouteReflectorClient_TC42
    BGPv4Neighbor_RouteReflectorClient_TC43
    BGPv4Neighbor_RouteReflectorClient_TC44
    BGPv4Neighbor_NextHopSelf_TC45
    BGPv4Neighbor_NextHopSelf_TC46
    BGPv4Neighbor_NextHopSelf_TC47
    BGPv4Neighbor_Disabled_TC48
    BGPv4Neighbor_Disabled_TC49
    BGPv4Neighbor_Disabled_TC50
    BGPv4Neighbor_NeighborAddress_TC51
    BGPv4Neighbor_NeighborAddress_TC52
    BGPv4Neighbor_NeighborAddress_TC53
    BGPv4Neighbor_NeighborAddress_TC54
