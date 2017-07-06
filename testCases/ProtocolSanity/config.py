#GLOBAL PARAMETERS #############
	
PortStateDown = "DOWN"
PortStateUP = "UP"


#INTERFACE IP ADDRESSES ########

IntfIP = {
      "DUT1":{
         "fpPort1":"192.168.0.1/24",
	 "fpPort2":"192.168.1.1/24"   
      },
      "DUT2":{
         "fpPort3":"192.168.0.2/24",
         "fpPort7":"192.168.1.2/24"
      },
      "DUT3":{
         "fpPort4":"192.168.2.3/24",
         "fpPort8":"192.168.1.3/24"
      },
      "DUT4":{
         "fpPort5":"192.168.2.4/24",
         "fpPort6":"192.168.1.4/24"
      }
           }

IntfIPState = {
                 "DUT1" :["fpPort1","fpPort2"],
                 "DUT2" :["fpPort3","fpPort7"],
                 "DUT4" :["fpPort5","fpPort6"],
                 "DUT3" :["fpPort4","fpPort8"]
               }

IntfIPDelete = {
                 "DUT1" :["fpPort1","fpPort2"],
                 "DUT2" :["fpPort3","fpPort7"],
                 "DUT4" :["fpPort5","fpPort6"],
                 "DUT3" :["fpPort4","fpPort8"]
               }

#LLDP PARAMETERS ###############
LLDPSleep = 2
LLDPGlobal = {
              "DUT1" : {
                  "Vrf" : "default",    
                  "TxRxMode" : "TxRx",  
                  "Enable" : True,      
                  "TranmitInterval" : 30,
                  "SnoopAndDrop"    : False
                      },
              "DUT2" : {
                  "Vrf" : "default",    
                  "TxRxMode" : "TxRx",  
                  "Enable" : True,      
                  "TranmitInterval" : 30,
                  "SnoopAndDrop"    : False
                      },
              "DUT4" : {
                  "Vrf" : "default",    
                  "TxRxMode" : "TxRx",  
                  "Enable" : True,      
                  "TranmitInterval" : 30,
                  "SnoopAndDrop"    : False
                      },
              "DUT3" : {
                  "Vrf" : "default",    
                  "TxRxMode" : "TxRx",  
                  "Enable" : True,      
                  "TranmitInterval" : 30,
                  "SnoopAndDrop"    : False
                      }
             }

LLDPConnectivity = {
                 "DUT1" : ["fpPort6","fpPort3"],
                 "DUT2" : ["fpPort1","fpPort8"],
                 "DUT4" : ["fpPort4","fpPort2"],
                 "DUT3" : ["fpPort5","fpPort7"]
                 }

#ARP PARAMETERS ################

ArpLinuxEntryStates = ["DUT1","DUT2","DUT4","DUT3"]
ArpLinuxEntryState1 = ["DUT1"]
ARPtestDevice = "DUT1"
ARPtestPort = "fpPort1"
ARPIPAddr = "192.168.0.2"
ARPSleep = 10
"""
ARPtest1 = {
          "DUT1" :
               {
               "fpPort1" : "DOWN",
               "fpPort2" : "DOWN"
                }
           }
ARPtest2 = {
          "DUT1" :
               {
               "fpPort1" : "UP",
               "fpPort2" : "UP"
               }
           } 

"""
#BGP PARAMETERS ################

BGPDevice_List = ["DUT1","DUT2","DUT4","DUT3"]
BGPtestDevice = "DUT1"
BGPtestPort = "fpPort1"
BGPExpectedState = "CONNECT"
BGPConvergenceSleep = 15
BGPConnectRetryTime = 120
BGPGlobal = {
           "DUT1":{      
                 "ASNum":"200",
                 "RouterId":"1.1.1.1"
                   },
           "DUT2":{      
                 "ASNum":"201",
                 "RouterId":"2.2.2.2"
                   },
           "DUT3":{      
                 "ASNum":"202",
                 "RouterId":"3.3.3.3"
                   },
           "DUT4":{      
                 "ASNum":"203",
                 "RouterId":"4.4.4.4"
                   } 
              }

PolicyDefinition ={ 

           "DUT1":{      
                "Name":"p1_match_all",
                "StatementList":[{"Priority":0,"Statement":"s1_permit"}]
                  },
           "DUT2":{      
                "Name":"p1_match_all",
                "StatementList":[{"Priority":0,"Statement":"s1_permit"}]
                   },
           "DUT3":{      
                "Name":"p1_match_all",
                "StatementList":[{"Priority":0,"Statement":"s1_permit"}]
                   },
           "DUT4":{      
                "Name":"p1_match_all",
                "StatementList":[{"Priority":0,"Statement":"s1_permit"}]
                   }
                 }
BGPv4TestDeviceNeighborState = {
        "DUT1":{      
               "Peer1" : {
                        "IntfRef" : "fpPort1",
                        "NeighborAddress" : "192.168.0.2",
                        "CheckParameter":"SessionState",
                        "ExpectedState" : "CONNECT"
                         }
               }
                      }
BGPv4TestDeviceNeighborState1 = {
        "DUT1":{      
               "Peer1" : {
                        "IntfRef" : "fpPort1",
                        "NeighborAddress" : "192.168.0.2",
                        "CheckParameter":"SessionState",
                        "ExpectedState" : "ESTABLISHED"
                         }
               }
                      }

BGPv4Neighbor = {

           "DUT1":{      
               "Peer1":{
                 "PeerAS":"201",
                 "NeighborAddress":"192.168.0.2",
                 "IntfRef":"fpPort1"
                        },
               "Peer2":{
                 "PeerAS":"203",
                 "NeighborAddress":"192.168.1.4",
                 "IntfRef":"fpPort2"
                       }
               },
           "DUT4":{      
               "Peer1":{
                 "PeerAS":"200",
                 "NeighborAddress":"192.168.1.1",
                 "IntfRef":"fpPort6"
                        },
               "Peer2":{
                 "PeerAS":"202",
                 "NeighborAddress":"192.168.2.3",
                 "IntfRef":"fpPort5"
                       }
               },
           "DUT2":{      
               "Peer1":{
                 "PeerAS":"200",
                 "NeighborAddress":"192.168.0.1",
                 "IntfRef":"fpPort3"
                        },
               "Peer2":{
                 "PeerAS":"202",
                 "NeighborAddress":"192.168.1.3",
                 "IntfRef":"fpPort7"
                       }
                },
           "DUT3":{      
               "Peer1":{
                 "PeerAS":"203",
                 "NeighborAddress":"192.168.2.4",
                 "IntfRef":"fpPort4"
                        },
               "Peer2":{
                 "PeerAS":"201",
                 "NeighborAddress":"192.168.1.2",
                 "IntfRef":"fpPort8"
                       }
                }
        }

BGPv4NeighborState = {

           "DUT1":{      
               "Peer1":{
                 "NeighborAddress":"192.168.0.2",
                 "IntfRef":"fpPort1",
                 "CheckParameter":"SessionState",
                 "ExpectedState" : "ESTABLISHED"
                        },
               "Peer2":{
                 "NeighborAddress":"192.168.1.4",
                 "IntfRef":"fpPort2",
                 "CheckParameter":"SessionState",
                 "ExpectedState" : "ESTABLISHED"

                       }
               },
           "DUT4":{      
               "Peer1":{
                 "NeighborAddress":"192.168.1.1",
                 "IntfRef":"fpPort6",
                 "CheckParameter":"SessionState",
                 "ExpectedState" : "ESTABLISHED"

                        },
               "Peer2":{
                 "NeighborAddress":"192.168.2.3",
                 "IntfRef":"fpPort5",
                 "CheckParameter":"SessionState",
                 "ExpectedState" : "ESTABLISHED"

                       }
               },
           "DUT2":{      
               "Peer1":{
                 "NeighborAddress":"192.168.0.1",
                 "IntfRef":"fpPort3",
                 "CheckParameter":"SessionState",
                 "ExpectedState" : "ESTABLISHED"

                        },
               "Peer2":{
                 "NeighborAddress":"192.168.1.3",
                 "IntfRef":"fpPort7",
                 "CheckParameter":"SessionState",
                 "ExpectedState" : "ESTABLISHED"

                       }
                },
           "DUT3":{      
               "Peer1":{
                 "NeighborAddress":"192.168.2.4",
                 "IntfRef":"fpPort4",
                 "CheckParameter":"SessionState",
                 "ExpectedState" : "ESTABLISHED"

                        },
               "Peer2":{
                 "NeighborAddress":"192.168.1.2",
                 "IntfRef":"fpPort8",
                 "CheckParameter":"SessionState",
                 "ExpectedState" : "ESTABLISHED"
                       }
                }
        }

BGPv4Delete = { 
        "DUT1":{      
               "Peer1" : {
                        "PeerAS":"201",
                        "IntfRef" : "fpPort1",
                        "NeighborAddress" : "192.168.0.2"
                         },
               "Peer2" : {
                        "PeerAS":"203",
                        "IntfRef" : "fpPort2",
                        "NeighborAddress" : "192.168.1.4"
                         }
                },
        "DUT2":{      
               "Peer1" : {
                        "PeerAS":"200",
                        "IntfRef" : "fpPort3",
                        "NeighborAddress" : "192.168.0.1"
                         },
               "Peer2":{
                 "PeerAS":"202",
                 "NeighborAddress":"192.168.1.3",
                 "IntfRef":"fpPort7"
                       }
               },
        "DUT3":{      
               "Peer1" : {
                        "PeerAS":"203",
                        "IntfRef" : "fpPort3",
                        "NeighborAddress" : "192.168.2.4"
                         },
               "Peer2":{
                         "PeerAS":"201",
                         "NeighborAddress":"192.168.1.2",
                         "IntfRef":"fpPort8"
                       }
               },
        "DUT4":{      
               "Peer1" : {
                        "PeerAS":"200",
                        "IntfRef" : "fpPort5",
                        "NeighborAddress" : "192.168.2.3"
                         },      
               "Peer2" : {
                        "PeerAS":"202",
                        "IntfRef" : "fpPort6",
                        "NeighborAddress" : "192.168.1.1"
                         }
               }
                      }

PolicyStmt = {
           "DUT1":{      
                 "Name":"s1_permit",
                 "Action":"permit"
                  },
           "DUT2":{      
                 "Name":"s1_permit",
                 "Action":"permit"
                  },
           "DUT3":{      
                 "Name":"s1_permit",
                 "Action":"permit"
                  },
           "DUT4":{      
                 "Name":"s1_permit",
                 "Action":"permit"
                  }
            }

BGPRedistribution = {
          "DUT1":{"Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]},
          "DUT2":{"Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]},
          "DUT3":{"Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]},
          "DUT4":{"Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]}
                    }


"""
BGPRoute = {
          "DUT1":{"Nw1": {
                             "CIDRLen": 30,
                             "Network":"192.168.0.0",
                             "CheckParameter" : "NextHop",
                             "ExpectedValue" : ""}]}, 
          "DUT2":{"Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]},
          "DUT3":{"Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]},
          "DUT4":{"Redistribution":[{"policy":"p1_match_all","Sources":"CONNECTED"}]}
                    } 

"""
BGPRoute = ["DUT1","DUT2","DUT4","DUT3"]
BGP_IPV4Route = ["DUT1","DUT2","DUT4","DUT3"]

