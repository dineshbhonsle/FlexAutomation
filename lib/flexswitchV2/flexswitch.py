#!/usr/bin/python
import requests
import json
import urllib2

SUCCESS_STATUS_CODE = 201

headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
class FlexSwitch( object):
    def  __init__ (self, ip, port):
        self.ip    = ip
        self.port  = port 
        self.urlBase = 'http://%s:%s/public/v1/'%(ip,str(port))

    def createVlanInterface( self, intfIp, vlanId) :
        obj =  { 'IpAddr'   : intfIp,
                 'IfIndex' : self.getVlanInfo(vlanId),
               }
        reqUrl =  self.urlBase+'IPv4Intf'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def createPhyInterface( self, intfIp, ifindex) :
        obj =  { 'IpAddr'   : intfIp,
                 'IfIndex' : ifindex,
               }
        reqUrl =  self.urlBase+'IPv4Intf'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def createVlan (self, vlanId, ports, taggedports):
        obj =  { 'VlanId': int(vlanId),
                 'IfIndexList' : ports,
                 'UntagIfIndexList': taggedports 
               }
        reqUrl =  self.urlBase+'Vlan'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        print obj["VlanId"], r.__dict__
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None


    def deleteVlanByUuid(self, uuid):
        reqUrl =  self.urlBase+'Vlan'+'/'+ uuid
        r = requests.delete(reqUrl, headers=headers)

    def createBgpGlobal(self, asnum, rtrid, usemp=False, ebgpmp=1, ibgpmp=1):
        return r.json()

    def createBfdGlobal(self, bfd_type, bfd_enable):
    	obj =  {
        		'Bfd': bfd_type, 
        		'Enable': bfd_enable
        		}
        reqUrl =  self.urlBase+'BfdGlobal'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json()    
        		
    def createBfdintf(self, ifindex, multiplier, mintx_int, minrx_int, minrx_echo, demand, auth, auth_type, auth_key, auth_data):
    	obj =  {
        		'IfIndex': ifindex,
    			'LocalMultiplier': multiplier, 
    			'DesiredMinTxInterval': mintx_int, 
    			'RequiredMinRxInterval': minrx_int, 
    			'RequiredMinEchoRxInterval': minrx_echo, 
    			'DemandEnabled': demand, 
    			'AuthenticationEnabled': auth, 
    			'AuthenticationType': auth_type, 
    			'AuthenticationKeyId': auth_key, 
    			'AuthenticationData': auth_data
    			}
        reqUrl =  self.urlBase+'BfdInterface'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() 

    def createBfdSession(self, ipaddr, perlink, owner):
    	obj =  {
 				'IpAddr': ipaddr, 
 				'PerLink': perlink, 
 				'Owner': owner, 
    			}
        reqUrl =  self.urlBase+'BfdSession'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() 

      
    def createBgpGlobal(self, asnum, rtrid, usemp, ebgpmp, ibgpmp):
        obj =  { 
                'ASNum'         : asnum,
                'RouterId'   : rtrid,  
                'UseMultiplePaths': usemp, 
				'EBGPMaxPaths': ebgpmp, 
				'IBGPMaxPaths': ibgpmp  
               }
 
        reqUrl =  self.urlBase+'BGPGlobal'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def createBgpPeerGroup(self, name, desc, CRT, HT, KpAT, RRClustID=0, RRClient=False, APRx=False, APTxMax=0):
        obj =  { 
        		'Name' : name,
                'ConnectRetryTime': CRT, 
                'HoldTime'         : HT,
                'KeepaliveTime'    : KpAT,
                'Description'      : desc,
                'RouteReflectorClusterId' : RRClustID,
                'RouteReflectorClient': RRClient,
                'AddPathsRx' : APRx,
                'AddPathsMaxTx': APTxMax,                
               }
        reqUrl =  self.urlBase+'BGPPeerGroup'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def createBgpPeer(self, nbrIp, peeras, localas, peergroup=None, desc=''):
        return r.json()

    def createBgpPeer(self, nbrIp, peeras, peergroup, desc, bfd):
        obj =  { 
                'PeerAS'         : peeras,
                'AuthPassword'   : '',
                'Description'      : desc ,
                'PeerGroup'		: peergroup,
                'NeighborAddress' : nbrIp,
                'BfdEnable'	: bfd
               }
        reqUrl =  self.urlBase+'BGPNeighbor'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json()

    def createBgpPeerLocAs(self, nbrIp, peeras, localas, peergroup, desc, bfd):
        obj =  { 
                'PeerAS'         : peeras,
                'LocalAS'        : localas,
                'AuthPassword'   : '',
                'Description'      : desc ,
                'PeerGroup'		: peergroup,
                'NeighborAddress' : nbrIp,
                'BfdEnable'	: bfd
               }
        reqUrl =  self.urlBase+'BGPNeighbor'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def createOspfGlobal(self, rtrid='10.0.1.1'):
        obj =  { 
                'RouterIdKey' : rtrid,
               }
        reqUrl =  self.urlBase+'OspfGlobal'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def createPolicyCondition(self, condition ):
        obj = condition 
        reqUrl =  self.urlBase+'PolicyCondition'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def createPolicyAction (self, action):
        obj = action
        reqUrl =  self.urlBase+'PolicyAction'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def createPolicyStatement (self, stmt):
        obj = stmt 
        reqUrl =  self.urlBase+'PolicyStmt'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def createPolicy(self, policy ):
        obj = policy 
        reqUrl =  self.urlBase+'PolicyDefinition'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        print r.__dict__
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def createVrrpIntfConfig(self, 
			     vlanId, 
                             priority, 
                             vrid, 
                             virturalIp, 
                             advertime, 
                             preempt, 
                             accept):
        IfIndex = self.getVlanInfo(vlanId)
        if virturalIp == "":
            obj = {
                'IfIndex': IfIndex,
                'VRID': vrid,
                'Priority':priority,
                'AdvertisementInterval': advertime,
                'PreemptMode': preempt,
                'AcceptMode':accept
            }
        elif virturalIp != "":
            obj = {
                'IfIndex': IfIndex,
                'VRID': vrid,
                'Priority':priority,
                'AdvertisementInterval': advertime,
                'PreemptMode': preempt,
                'AcceptMode':accept,
                'VirtualIPv4Addr':virturalIp
            }

        #print obj
        reqUrl = self.urlBase+'VrrpIntf'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def updateVrrpIntfConfig(self, priority, vlanId, uuid):
        IfIndex = self.getVlanInfo(vlanId)
        obj = {
                'Priority':priority
              }
        reqUrl = self.urlBase+'VrrpIntf/' + uuid
        r = requests.patch(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def createOspfIntf(self, 
                       ipaddr, 
                       ifIndex = 0,
                       areaId = '0', 
                       ifType = 1,
                       priority = 1,
                       helloIntvl = 10,
                       authKey ='',
                       authType =0
                       ):
        obj =  { 
                'IfIpAddressKey' : ipaddr,
                'AddressLessIfKey' : ifIndex,
                'IfAreaId' : areaId, 
                'IfType' :  ifType, 
                'IfAdminStat' :   1,
                'IfRtrPriority' : priority,
                'IfTransitDelay' : 0,
                'IfRetransInterval' : helloIntvl,
                'IfHelloInterval' :   helloIntvl,
                'IfRtrDeadInterval' : 4*helloIntvl, 
                'IfPollInterval' : 0, 
                'IfAuthKey' : authKey ,
                'IfAuthType' : authType
               }
        reqUrl =  self.urlBase+'OspfIfEntry'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
    
    def createRedistributionPolicy(self):
        obj = {'Name'           :'RedistributeConnectedToBGP', 
          'MatchPrefixSet': {'PrefixSet' :'', 'MatchSetOptions' : 0}, 
          'InstallProtocolEq':'Connected', 
          'RouteDisposition': '', 
          'Redistribute':True, 
          'RedistributeTargetProtocol':'BGP'}

        reqUrl =  self.urlBase+'PolicyDefinitionStmt'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def enableGlobalDHCPRelay (self) :
        obj =  { 
        		'DhcpRelay': 'Test',
                'Enable' : True
               }
        reqUrl =  self.urlBase+'DhcpRelayGlobal'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
        
    def enableIntfDHCPRelay (self, ifIndex, svrIp ):
        obj =  {  
                'IfIndex' : ifIndex,
                'Enable' : True,
                'ServerIp': svrIp
                }

        reqUrl =  self.urlBase+'DhcpRelayIntf'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    # configure lag group
    # id - lag id # will be converted to aggId-<id>
    # type - 0 == LACP, 1 == STATIC
    # mode - 0 == ACTIVE, 1 == PASSIVE
    # period - 0 == SLOW, 1 == FAST
    # sysmac - format 'XX:XX:XX:XX:XX:XX'

    def createLag(self, lagId, lagType, sysmac, sysprio, mode, period, hashmode):
        obj = {
            'NameKey' : "aggId-%s" %lagId,
            'LagType' : lagType,
            'Type'    : "ETH",
            'Description' : "Test lag creation",
            'Enabled' : True,
            'Interval' : period,
            'LacpMode' : mode,
            'SystemIdMac' : sysmac,
            'SystemPriority' : sysprio,
            'MinLinks' : 1,
            'LagHash' : hashmode,
            'Mtu' : 1518
        }
        reqUrl =  self.urlBase+'AggregationLacpConfig'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
    
    # id - port number will be conververt to fpPort-<id>
    def addPortToLag(self, id, lagid):
        obj = {
            'NameKey' : 'fpPort-%s' % id,
	        'Enabled' : True,
            'Description' : "Test lag port",
            'Mtu' : 1518,
	        'Type' : 'ETH',
	        'MacAddress' : '00:11:22:33:44:55',
	        'DuplexMode' : 0,
	        'Auto'       : True,
	        'Speed'      : 'SPEED_1Gb',
	        'EnableFlowControl' : True,
            'AggregateId' : 'aggId-%s' % lagid
        }
        reqUrl =  self.urlBase+'EthernetConfig'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        print obj["NameKey"], r.__dict__
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def delPortFromLag(self, id, lagid):
        obj = {
            'NameKey' : 'fpPort-%s' % id,
            'Enabled' : True,
            'Description' : "Test lag port",
            'Mtu' : 1518,
            'Type' : 'ETH',
            'MacAddress' : '00:11:22:33:44:55',
            'DuplexMode' : 0,
            'Auto'       : True,
            'Speed'      : 'SPEED_1Gb',
            'EnableFlowControl' : True,
            'AggregateId' : 'aggId-%s' % lagid
        }

    def createStpBridge(self, vlan, mac, prio, age, hellotime, forwarddelay):
        obj = {
            "Address" : mac, #string `SNAPROUTE: KEY`
            "Priority": prio,  #int32 `SNAPROUTE: KEY`
            "MaxAge": age, # int32
            "HelloTime": hellotime, # int32
            "ForwardDelay": forwarddelay, # int32
            "ForceVersion": 2, # int32 0 STP compatibility, 2 default mode
            "TxHoldCount": 6, # int32 valid values 1-10s
            "Vlan": vlan,
        }
        reqUrl =  self.urlBase+'StpBridgeInstance'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def deleteStpBridge(self, vlan, mac, prio, age, hellotime, forwarddelay):
        obj = {
            "Address" : mac,
            "Priority": prio,
            "MaxAge": age, # int32
            "HelloTime": hellotime, # int32
            "ForwardDelay": forwarddelay, # int32
            "ForceVersion": 2, # int32 0 STP compatibility, 2 default mode
            "TxHoldCount": 6, # int32 valid values 1-10s
            "Vlan": vlan, # SNAPROUTE KEY
        }

    def deleteStpBridgeByUuid(self, uuid):
        reqUrl =  self.urlBase+'StpBridgeInstance'+'/'+uuid
        r = requests.delete(reqUrl, headers=headers)

    def createStpPortEntry(self, port, brg, prio, ena, pathcost, protomigra, adminp2p, adminedge, adminpathcost, brgassurance):

        obj = {
            "IfIndex": port, # int32 `SNAPROUTE: KEY`
            "Priority": prio, # int32
            "Enable": ena, # int32
            "PathCost": pathcost, # int32
            "PathCost32": pathcost, # int32
            "ProtocolMigration": protomigra, # int32
            "PointToPoint": adminp2p, # int32
            "AdminEdgePort": adminedge, # int32
            "AdminPathCost": adminpathcost, # int32
            "BrgIfIndex": brg, # int32
            "BridgeAssurance":brgassurance, #int32
            "BpduGuard": 1 if adminedge else 0,
        }
        reqUrl =  self.urlBase+'StpPort'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None


    def deleteStpPortEntry(self, port, brg, prio, ena, pathcost, protomigra, adminp2p, adminedge, adminpathcost, brgassurance):

        obj = {
            "IfIndex": port, # int32 `SNAPROUTE: KEY`
            "Priority": prio, # int32
            "Enable": ena, # int32
            "PathCost": pathcost, # int32
            "PathCost32": pathcost, # int32
            "ProtocolMigration": protomigra, # int32
            "AdminPointToPoint": adminp2p, # int32
            "AdminEdgePort": adminedge, # int32
            "AdminPathCost": adminpathcost, # int32
            "BrgIfIndex": brg, # int32
            "BridgeAssurance":brgassurance, #int32
            "BpduGuard": 1 if adminedge else 0,
        }


    def deleteStpPortEntryByUuid(self, uuid):
        reqUrl =  self.urlBase+'StpPort'+'/'+uuid
        r = requests.delete(reqUrl, headers=headers)

    def createVxlanEntry(self, vni, vlanId, GroupIp, MTU):
        obj = {
            "VxlanId" :  vni, # key
	        "Group" : "", # UNSUPPORTED
	        "VlanId" : vlanId,
            "Mtu" : MTU,
        }
        reqUrl =  self.urlBase+'VxlanInstance'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        print obj, r.__dict__
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def deleteVxlanEntryByUuid(self, uuid):
        reqUrl =  self.urlBase+'VxlanInstance'+'/'+uuid
        r = requests.delete(reqUrl, headers=headers)

    def createVtepEntry(self, vtepId, vxlanId, srcifindex, udp, srcmac, tunnelsrcip, tunneldstip, ttl, tos):
        obj = {
           "VtepId" : vtepId, #key
           "VtepName" : "vtep%s" %(vtepId),
	       "VxlanId" : vxlanId, # key
	       "SrcIfIndex" : srcifindex,
	       "UDP" : udp,
	       "TTL" : ttl,
	       "TOS" : tos,
	       "TunnelSourceIp" : tunnelsrcip,
	       "TunnelDestinationIp" : tunneldstip,
	       "SrcMac" : srcmac,
        }
        reqUrl =  self.urlBase+'VxlanVtepInstances'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        print obj, r.__dict__
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def deleteVtepEntryByUuid(self, uuid):
        reqUrl =  self.urlBase+'VxlanVtepInstances'+'/'+uuid
        r = requests.delete(reqUrl, headers=headers)

    def createLogicalIntf(self, name, type):
        obj = {
            "Name" : name,
	        "Type" : type,
        }
        reqUrl =  self.urlBase+'LogicalIntfConfig'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        print obj, r.__dict__
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def deleteLogicalIntf(self, uuid):
        reqUrl =  self.urlBase+'LogicalIntfConfig'+'/'+uuid
        r = requests.delete(reqUrl, headers=headers)

    def createIpV4Intf(self, ip, ifindex):
        obj = {
            "IpAddr" : ip,
	        "IfIndex" : ifindex,
        }
        reqUrl =  self.urlBase+'IPv4Intf'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers)
        print obj, r.__dict__
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def deleteIpV4Intf(self, uuid):
        reqUrl =  self.urlBase+'IPv4Intf'+'/'+uuid
        r = requests.delete(reqUrl, headers=headers)

    def portAdminStateSet(self, uuid, enable):
        obj = {
            	'AdminState' : "ON" if enable else "OFF"
        }
        reqUrl =  self.urlBase+'PortConfig' + '/' + ouid
        r = requests.patch(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None

    def portSpeedSet(self, ouid, speed):
        obj = {
            'Speed' : speed
        }
        reqUrl =  self.urlBase+'PortConfig' + '/' + ouid
        r = requests.patch(reqUrl, data=json.dumps(obj), headers=headers)
        return r.json() if r.status_code == SUCCESS_STATUS_CODE else None
    
    def getObjects(self, objName):
        currentMarker = 0
        nextMarker = 0
        count = 10
        more = True
        entries = []
        while more == True:
            qry = 'http://%s:8080/public/v1/%s?CurrentMarker=%d&NextMarker=%d&Count=%d' %(self.ip, objName, currentMarker, nextMarker, count)
            response = requests.get(qry)
            data = response.json()
            more =  data['MoreExist']
            currentMarker =  data['NextMarker']
            NextMarker    =  data['NextMarker']
            if data['StateObjects'] != None:
                entries.extend(data['StateObjects'])
        return entries 
		
    def getVlanInfo (self, vlanId) :
        for vlan in self.getObjects('Vlans'):
            #print vlan
            if vlan['ConfigObj']['VlanId'] == vlanId:
                return int(vlan['ConfigObj']['IfIndex'])
                
####################################################################               
#################### DELETE OPERATIONS #############################
####################################################################               

    def deleteIPv4Address( self, uuid) :
        reqUrl =  self.urlBase+'IPv4Intf/'+ uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
      
    def deleteVlan (self, uuid):
        reqUrl =  self.urlBase+'Vlan/' + uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
    
    def deleteBfdGlobal(self, uuid):
        reqUrl =  self.urlBase+'BfdGlobalConfig/' + uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()    
        
    def deleteBfdintf(self, uuid):
        reqUrl =  self.urlBase+'BfdIntfConfig/' + uuid
        r = requests.post(reqUrl,  headers=headers)
        return r.json() 
    
    def deleteBfdSession(self, uuid):
        reqUrl =  self.urlBase+'BfdSessionConfig/' + uuid
        r = requests.post(reqUrl,  headers=headers)
        return r.json() 
      
    def deleteBgpGlobal(self, uuid):
        reqUrl =  self.urlBase+'BGPGlobalConfig/' + uuid
        r = requests.post(reqUrl,  headers=headers)
        return r.json()
        
    def deleteBgpPeerGroup(self, uuid):
        reqUrl =  self.urlBase+'BGPPeerGroup/' + uuid
        r = requests.post(reqUrl,  headers=headers)
        return r.json()
    
    def deleteBgpPeer(self, uuid):
        reqUrl =  self.urlBase+'BGPNeighborConfig/' + uuid
        r = requests.post(reqUrl,  headers=headers)
        return r.json()
    
    def deleteOspfGlobal(self, uuid):
        reqUrl =  self.urlBase+'OspfGlobalConfig/'+ uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
        
    def deletePolicyCondition(self, uuid ):
        reqUrl =  self.urlBase+'PolicyConditionConfig/'+ uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
        
    def deletePolicyAction (self, uuid):
        reqUrl =  self.urlBase+'PolicyActionConfig/'+ uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
        
    def deletePolicyStatement (self, uuid):
        reqUrl =  self.urlBase+'PolicyStmtConfig/'+ uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
        
    def deletePolicy(self, uuid ):
        reqUrl =  self.urlBase+'PolicyDefinitionConfig/'+ uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
    
    def deleteOspfIntf(self, uuid):
        reqUrl =  self.urlBase+'OspfIfEntryConfig/' + uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
    	
        
    def deleteGlobalDHCPRelay (self, uuid):
        reqUrl =  self.urlBase+'DhcpRelayGlobal/' + uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()
        
    def deleteIntfDHCPRelay (self, uuid):
        reqUrl =  self.urlBase+'DhcpRelayIntf/' + uuid
        r = requests.delete(reqUrl,  headers=headers)
        return r.json()      
			

if __name__=='__main__':
    pass
