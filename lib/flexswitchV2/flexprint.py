import requests
import json
import re
import urllib2
#from datetime import datetime
from flexswitchV2 import FlexSwitch
from flexprintV2 import FlexSwitchShow
from tablePrint import *

def getLagGroups(ip, port):
        currentMarker = 0
        nextMarker = 0
        count = 5
        more = True

        while more == True:
            qry = 'http://%s:%s/public/v1/AggregationLacpStates?CurrentMarker=%d&NextMarker=%d&Count=%d' %(ip, port, currentMarker, nextMarker, count)
            response = requests.get(qry)
            data = response.json()
            if currentMarker == 0: #Print the header only for first iteration
                print 'Name      Ifindex      LagType   Description      Enabled   MinLinks   Interval   Mode          SystemIdMac            SystemPriority    HASH'


            more =  data['MoreExist']
            currentMarker =  data['NextMarker']
            NextMarker    =  data['NextMarker']
            if data['StateObjects']:
                for d in data['StateObjects']:
                    print '%7s  %7s    %7s  %15s    %8s   %2s     %8s      %6s   %20s         %s              %s' %(d['NameKey'],
                                                                    d['Ifindex'],
                                                                    "LACP" if int(d['LagType']) == 0 else "STATIC",
                                                                    d['Description'],
                                                                    "Enabled" if bool(d['Enabled']) else "Disabled",
                                                                    d['MinLinks'],
                                                                    "FAST" if int(d['Interval']) == 0 else "SLOW",
                                                                    "ACTIVE" if int(d['LacpMode']) == 0 else "PASSIVE",
                                                                    d['SystemIdMac'],
                                                                    d['SystemPriority'],
                                                                    d['LagHash'])
            #import ipdb;ipdb.set_trace()



class FlexPrint( FlexSwitchShow):
    def  __init__ (self, ip, port):
        self.swtch = FlexSwitch(ip, port)

    def printPortState(self, IntfRef):

        port = self.swtch.getPortState(IntfRef).json()
        p = port['Object']
        port_config = self.swtch.getPort(p['IntfRef']).json()
        pc = port_config['Object']
        ipv4_state = self.swtch.getIPv4IntfState(p['IntfRef']).json()
        ipv4 = None
        if ipv4_state.has_key('Object'):
            ipv4 = ipv4_state['Object']

        if not p['LastDownEventTime']:
            lastdown="never"
        else:
            lastdown = p['LastDownEventTime']
        if not p['LastUpEventTime']:
            lastdown="never"
        else:
            lastdown = p['LastDownEventTime']

        print p['Name'], "is", p['OperState'], "Admin State is", pc['AdminState']
        if ipv4 is not None:
            print "  IPv4 Address is", ipv4['IpAddr']
        print "  PresentInHW:", p['PresentInHW']
        print "  Config Mode:", p['ConfigMode']
        print "  PhyType:", pc['PhyIntfType'],",","Media Type:",pc['MediaType'],"," , "Address:", pc['MacAddr']
        print "  MTU",  pc['Mtu'],"Bytes"
        print " ",pc['Duplex'],",",pc['Speed'],"Mb/s"
        print "  Breakout Status:", pc['BreakOutMode']
        print "  Last link down:",p['LastDownEventTime']
        print "  Last link up:",   p['LastUpEventTime']
        print "  Number of Link flaps:", p['NumDownEvents']
        print "  ErrDisableReason:", p['ErrDisableReason']
        print "  RX"
        print "   ",p['IfInUcastPkts'],"unicast packets",p['IfInOctets'],"unicast octets"
        print "   ",p['IfInDiscards'],"input discards", p['IfInErrors'], "input errors"
        print "   ",p['IfInUnknownProtos'],"unknown protocol", p['IfEtherUnderSizePktCnt'], "runts",p['IfEtherOverSizePktCnt'], "giants"
        print "   ",p['IfEtherFragments'],"Fragments",p['IfEtherCRCAlignError'],"CRC",p['IfEtherJabber'], "jabber"
        print "  TX"
        print "   ",p['IfOutUcastPkts'],"unicast packets",p['IfOutOctets'],"unicast octets"
        print "   ",p['IfOutDiscards'],"output discards", p['IfOutErrors'], "output errors"
        print '------------------------------------------------------------------------------'

    def printInterfaceStatuss(self):
        ports = self.swtch.getAllPortStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ports, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)) )
        labels = ('Port','Description','Status','Mtu','Duplex','Speed','AutoNeg', 'Type')
        rows = []
        for port in lines:
            p = port['Object']
            if 'NO' in p['PresentInHW']:
                continue
            port_config = self.swtch.getPort(p['IntfRef']).json()
            pc = port_config['Object']
            rows.append(("%s" %(p['IntfRef']),
                         "%s" %(pc['Description']),
                         "%s" %(p['OperState']),
                         "%s" %(pc['Duplex']),
                         "%s" %(pc['Mtu']),
                         "%s" %(pc['Speed']),
                         "%s" %(pc['Autoneg']),
                         "%s" %(pc['PhyIntfType'])))
        width = 30
        print indent([labels]+rows, hasHeader=True, separateRows=False,
                     prefix=' ', postfix=' ', headerChar= '-', delim='    ',
                     wrapfunc=lambda x: wrap_onspace_strict(x,width))
                     
    def printInterfaces(self):
        self.printPortStates()

    def printPortStates(self):
        ports = self.swtch.getAllPortStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ports, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)) )
        for port in lines:
            p = port['Object']
            if 'NO' in p['PresentInHW']:
                continue

            port_config = self.swtch.getPort(p['IntfRef']).json()
            pc = port_config['Object']
            ipv4_state = self.swtch.getIPv4IntfState(p['IntfRef']).json()
            ipv4 = None
            if ipv4_state.has_key('Object'):
                ipv4 = ipv4_state['Object']

            if not p['LastDownEventTime']:
                lastdown="never"
            else:
                lastdown = p['LastDownEventTime']
            if not p['LastUpEventTime']:
                lastdown="never"
            else:
                lastdown = p['LastDownEventTime']

            print p['Name'], "is", p['OperState'], "Admin State is", pc['AdminState']
            if ipv4 is not None:
                print "  IPv4 Address is", ipv4['IpAddr']
            print "  PresentInHW:", p['PresentInHW']
            print "  Config Mode:", p['ConfigMode']
            print "  PhyType:", pc['PhyIntfType'],",","Media Type:",pc['MediaType'],"," , "Address:", pc['MacAddr']
            print "  MTU",  pc['Mtu'],"Bytes"
            print " ",pc['Duplex'],",",pc['Speed'],"Mb/s"
            print "  Breakout Status:", pc['BreakOutMode']
            print "  Last link down:",p['LastDownEventTime']
            print "  Last link up:",   p['LastUpEventTime']
            print "  Number of Link flaps:", p['NumDownEvents']
            print "  ErrDisableReason:", p['ErrDisableReason']
            print "  RX"
            print "   ",p['IfInUcastPkts'],"unicast packets",p['IfInOctets'],"unicast octets"
            print "   ",p['IfInDiscards'],"input discards", p['IfInErrors'], "input errors"
            print "   ",p['IfInUnknownProtos'],"unknown protocol", p['IfEtherUnderSizePktCnt'], "runts",p['IfEtherOverSizePktCnt'], "giants"
            print "   ",p['IfEtherFragments'],"Fragments",p['IfEtherCRCAlignError'],"CRC",p['IfEtherJabber'], "jabber"
            print "  TX"
            print "   ",p['IfOutUcastPkts'],"unicast packets",p['IfOutOctets'],"unicast octets"
            print "   ",p['IfOutDiscards'],"output discards", p['IfOutErrors'], "output errors"
            print '------------------------------------------------------------------------------'

    def printIPv4RouteStates(self):
        routes = self.swtch.getAllIPv4RouteStates()
        print "IP Route Table"
        print "'[x/y]' denotes [preference/metric]"
        print "\n"  
        lines = sorted(routes, key=lambda k: k['Object'].get('DestinationNw', 0))  	
        for r in lines:
            rt = r['Object']
            rt_spec = self.swtch.getIPv4RouteState(rt['DestinationNw']).json()
            rt_next=rt_spec['Object']
            if rt_next['NextHopList'] is None:
                rt_count = 0
            else:
                rt_count = len(rt_next['NextHopList'])
            route_distance = self.swtch.getRouteDistanceState(rt['Protocol']).json()
            rd = {"Distance": ""}
            if route_distance is not None and len(route_distance):
                rd = route_distance['Object']
            if rt['PolicyList'] is None:
                policy=rt['PolicyList']
            elif type(rt['PolicyList']) is list and len(rt['PolicyList']) == 0:
                policy=rt['PolicyList']
            else:
                policy = str(rt['PolicyList']).split("[")[1].split()[1]
            print rt['DestinationNw'], "ubest/mbest: 1/0"+",", "Policy:", policy
            while rt_count > 0:
                if rt['Protocol'] == "CONNECTED":
                    ip_int = self.swtch.getIPv4IntfState(rt_next['NextHopList'][rt_count-1]['NextHopIntRef']).json()
                    print "   via",ip_int['Object']['IpAddr'].split("/")[0] +", "+rt_next['NextHopList'][rt_count-1]['NextHopIntRef']+", "+"["+str(rd['Distance'])+"/"+str(rt_next['NextHopList'][rt_count-1]['Weight'])+"]"+",",rt['RouteCreatedTime']+",",rt['Protocol']
                else:
                    print "   via", rt_next['NextHopList'][rt_count-1]['NextHopIp']+", "+rt_next['NextHopList'][rt_count-1]['NextHopIntRef']+", "+"["+str(rd['Distance'])+"/"+str(rt_next['NextHopList'][rt_count-1]['Weight'])+"]"+",",rt['RouteCreatedTime']+",",rt['Protocol']
                rt_count-=1


    def printIPv6RouteStates(self):
        routes = self.swtch.getAllIPv6RouteStates()     
        print "IPv6 Route Table"
        print "'[x/y]' denotes [preference/metric]"
        print "\n"   
        lines = sorted(routes, key=lambda k: k['Object'].get('DestinationNw', 0))  	
        for r in lines:
            rt = r['Object']
            rt_spec = self.swtch.getIPv6RouteState(rt['DestinationNw']).json()
            rt_next=rt_spec['Object']    
            if rt_next['NextHopList'] is None:
                rt_count = 0
            else:
                rt_count = len(rt_next['NextHopList'])
            route_distance = self.swtch.getRouteDistanceState(rt['Protocol']).json()
            rd = {"Distance": ""}
            if route_distance is not None and len(route_distance):
                rd = route_distance['Object']
            if rt['PolicyList'] is None or len(rt['PolicyList']) == 0 :
                policy=rt['PolicyList']
            else:
                policy = str(rt['PolicyList']).split("[")[1].split()[1]
            print rt['DestinationNw'], "ubest/mbest: 1/0"+",", "Policy:", policy
            while rt_count > 0:
                if rt['Protocol'] == "CONNECTED":
                    ip_int = self.swtch.getIPv6IntfState(rt_next['NextHopList'][rt_count-1]['NextHopIntRef']).json()
                    print "   via",ip_int['Object']['IpAddr'].split("/")[0] +", "+rt_next['NextHopList'][rt_count-1]['NextHopIntRef']+", "+"["+str(rd['Distance'])+"/"+str(rt_next['NextHopList'][rt_count-1]['Weight'])+"]"+",",rt['RouteCreatedTime']+",",rt['Protocol']
                else:
                    print "   via", rt_next['NextHopList'][rt_count-1]['NextHopIp']+", "+rt_next['NextHopList'][rt_count-1]['NextHopIntRef']+", "+"["+str(rd['Distance'])+"/"+str(rt_next['NextHopList'][rt_count-1]['Weight'])+"]"+",",rt['RouteCreatedTime']+",",rt['Protocol']
                rt_count-=1

    def printVlanState(self, VlanId):

        self.printVlanStates(int(VlanId))

    def printCombinedVlanStates(self, VlanId=None):
        if VlanId is not None:
            vlans = [self.swtch.getVlan(VlanId).json()]
        else:
            vlans = self.swtch.getAllVlans()
        if len(vlans)>=0:
            print '\n'
            labels = ('VLAN','Name','Status','Ports')
            rows=[]
            for v in vlans:
                vl = v['Object']
                if int(vl['VlanId']) == VlanId or VlanId is None:
                    vlan_state = self.swtch.getVlanState(vl['VlanId']).json()
                    vls = vlan_state['Object']
                    operstate = vls['OperState']
                    #operstate = 'UP'
                    if vl['UntagIntfList'] is not None:
                        untag_ports = ', '.join(vl['UntagIntfList'])
                    else:
                        untag_ports = ""
                    if vl['IntfList']is not None:
                        tag_ports = ', '.join(vl['IntfList'])
                    else:
                        tag_ports = ""
                    port = untag_ports + "," + tag_ports
                    name = vls['VlanName']
                    rows.append( (str(vl['VlanId']),
                          "%s" %(name),
                          "%s" %(operstate),
                          "%s" %(str(port))))
            width = 20
            print indent([labels]+rows, hasHeader=True, separateRows=False,
                        prefix=' ', postfix=' ', headerChar= '-', delim='    ',
                        wrapfunc=lambda x: wrap_onspace_strict(x,width))

    def printPolicyDefinitionStates(self) :
        policies = self.swtch.getAllPolicyDefinitions()
        if len(policies) :
            print '\n'       
            for p in policies:
            	plcy = p['Object']
            	print 'route_policy %s %s' %(plcy['Name'],plcy['Priority'])
            	for stmt in plcy['StatementList']:
            		print '	priority_stmt %d'%( stmt['Priority'])
            		print '	 match %s'%(stmt['Statement'])
             	print '\n'
            #width = 20
            #print indent([labels]+rows, hasHeader=True, separateRows=False,
            #            prefix=' ', postfix=' ', headerChar= '-', delim='    ',
            #            wrapfunc=lambda x: wrap_onspace_strict(x,width))
                                
    def printDhcpRelayHostDhcpStates(self) :
        hosts = self.swtch.getAllDhcpRelayHostDhcpStates()
        if len(hosts) :
            print '\n\n---- Hosts ----'
            print 'MacAddress  ServerIP   DiscoverSent@   OfferReceived@  RequestSent@  AckReceived@   OfferedIP   RequestedIP   AcceptedIP    GWIP   ClntTx  ClntRx  SvrRx  SvrTx'
        for host in hosts:
            print '%s   %s  %s   %s     %s   %s  %s   %s     %s   %s  %s   %s   %s  %s' %(
                        host['MacAddr'],
                        host['ServerIp'],
                        host['ClientDiscover'],
                        host['ServerOffer'],
                        host['ClientRequest'],
                        host['ServerAck'],
                        host['OfferedIp'],
                        host['RequestedIp'],
                        host['AcceptedIp'],
                        host['GatewayIp'],
                        host['ClientRequests'],
                        host['ClientResponses'],
                        host['ServerRequests'],
                        host['ServerResponses'])




#    def printVlanStates (self):
#        vlans = self.swtch.getAllVlanStates()
#        if len(vlans):
#            print '\n\n---- Vlans ----'
#            print 'VlanId  Name   IfIndex   TaggedPorts     UntaggedPorts       Status'
#        for vlan in vlans:
#            print '%s   %s  %s  %s   %s  %s' %(vlan ['VlanId'],
#                                               vlan ['VlanName'],
#                                               vlan ['IfIndex'],
#                                               vlan ['IfIndexList'],
#                                               vlan ['UntagIfIndexList'],
#                                               vlan ['OperState'])

    def printVrrpIntfState (self):
        vrids = self.swtch.getAllVrrpIntfStates()
        '''
	entry.IfIndex = gblInfo.IntfConfig.IfIndex
	entry.VRID = gblInfo.IntfConfig.VRID
	entry.IntfIpAddr = gblInfo.IpAddr
	entry.Priority = gblInfo.IntfConfig.Priority
	entry.VirtualIPv4Addr = gblInfo.IntfConfig.VirtualIPv4Addr
	entry.AdvertisementInterval = gblInfo.IntfConfig.AdvertisementInterval
	entry.PreemptMode = gblInfo.IntfConfig.PreemptMode
	entry.VirtualRouterMACAddress = gblInfo.IntfConfig.VirtualRouterMACAddress
	entry.SkewTime = gblInfo.SkewTime
	entry.MasterDownInterval = gblInfo.MasterDownInterval
        '''
        if len(vrids):
            print ''
            print 'IfIndex   VRID    Vip     Priority   State     ViMac              IntfIp      Preempt  Advertise    Skew  Master_Down'
            print '================================================================================================================'
            for fObject in vrids:
                entry = fObject['Object']
                print '%s   %s  %s     %s   %s   %s      %s   %s    %s            %s      %s' %(entry ['IfIndex'],
                                                                   entry ['VRID'],
                                                                   entry ['VirtualIPv4Addr'],
                                                                   entry ['Priority'],
                                                                   entry ['VrrpState'],
                                                                   entry ['VirtualRouterMACAddress'],
                                                                   entry ['IntfIpAddr'],
                                                                   entry ['PreemptMode'],
                                                                   entry ['AdvertisementInterval'],
                                                                   entry ['SkewTime'],
                                                                   entry ['MasterDownTimer'])
            print ''

    def printOspfLsdbEntryStates(self) :
        lsas = self.swtch.getAllOspfLsdbEntryStates()
        if len(lsas) :
            print '\n\n---- Link State DB----'
            print 'LSA Type LS Checksum     LS Age      LS AreaId       LS ID       LS Sequence     LS RouterId     LS Advertisement'
        count = 0
        for lsa in lsas:
            count = count + 1
            print 'LS Database Entry Number:', count
            #print '%s           %s          %s          %s      %s      %s      %s      %s' %(lsa ['LsdbType'],
             #                                                               lsa ['LsdbChecksum'],
             #                                                               lsa ['LsdbAge'],
             #                                                               lsa ['LsdbAreaId'],
             #                                                               lsa ['LsdbLsid'],
             #                                                               lsa ['LsdbSequence'],
             #                                                               lsa ['LsdbRouterId'],
              #                                                              lsa ['LsdbAdvertisement'])
            adv = lsa['LsdbAdvertisement'].split(':')
            #print adv
            if lsa['LsdbType'] == 1 :
                print "LS Type: Router LSA"
            elif lsa['LsdbType'] == 2 :
                print "LS Type: Network LSA"
            elif lsa['LsdbType'] == 3 :
                print "LS Type: Summary Type 3 LSA"
            elif lsa['LsdbType'] == 4 :
                print "LS Type: Summary Type 4 LSA"
            elif lsa['LsdbType'] == 5 :
                print "LS Type: AS External LSA"

            print 'LS Age:', lsa ['LsdbAge']
            print 'Link State Id:', lsa ['LsdbLsid']
            print 'Advertising Router:', lsa ['LsdbRouterId']
            print 'LS Sequence Number:', lsa ['LsdbSequence']
            print 'LS Checksum:', lsa ['LsdbChecksum']
            if lsa['LsdbType'] == 1 :
                options = int(adv[0])
                if options & 0x1 :
                    print 'Bit B : true'
                else :
                    print 'Bit B : false'
                if options & 0x2 :
                    print 'Bit E : true'
                else :
                    print 'Bit E : false'
                if options & 0x4 :
                    print 'Bit V : true'
                else :
                    print 'Bit V : false'
                numOfLinks = int(adv[2]) << 8 | int(adv[3])
                print 'Number of Links:', numOfLinks
                for i in range(0, numOfLinks) :
                    print '         Link Number:', i+1
                    linkId = adv[4 + (i * 12)] + '.' + adv[4 + (i * 12) + 1] + '.' + adv[4 + (i * 12) + 2] + '.' + adv[4 + (i * 12) + 3]
                    print '         Link ID:', linkId
                    linkData = adv[4 + (i * 12) + 4] + '.' + adv[4 + (i * 12) + 5] + '.' + adv[4 + (i * 12) + 6] + '.' + adv[4 + (i * 12) + 7]
                    print '         Link Data:', linkData
                    linkType = ""
                    lType = adv[4 + (i * 12) + 8]
                    if lType == '1' :
                        linkType = "Point-to-Point Connection"
                    elif lType == '2' :
                        linkType = "Transit Link" 
                    elif lType == '3' :
                        linkType = "Stub Link" 
                    elif lType == '4' :
                        linkType = "Virtual Link" 
                    print '         Link Type:', linkType
                    numOfTOS = int(adv[4 + (i * 12) + 9])
                    print '         Number of TOS:', numOfTOS
                    metric = int(adv[4 + (i * 12) + 10]) << 8 | int(adv[4 + (i * 12) + 11])
                    print '         Metric:', metric
                    print ''
            elif lsa['LsdbType'] == 2 :
                netmask = adv[0] + '.' + adv[1] + '.' + adv[2] + '.' + adv[3]
                print 'Netmask:', netmask
                for i in range(0, (len(adv) - 4) / 4) :
                    attachedRtr = adv[4 + i * 4] + '.' + adv[5 + i * 4] + '.' + adv[6 + i * 4] + '.' + adv[3 + i * 4]
                    print '         Attached Router:', attachedRtr
                    
            print ''

    def printStpBridgeInstanceState(self, Vlan, addHeader=True, brief=None):

        rawobj = self.swtch.getStpBridgeInstanceState(Vlan)
        if rawobj.status_code in self.httpSuccessCodes:
            dataobj = rawobj.json()
            obj = dataobj['Object']
            print "BrgIfIndex: ", obj["IfIndex"]
            print "Bridge Id: ", obj["Address"]
            print "Bridge Hello time: ", obj["BridgeHelloTime"]
            print "Bridge TxHold: ", obj["TxHoldCount"]
            print "Bridge Forwarding Delay: ", obj["BridgeForwardDelay"]
            print "Bridge Max Age: ", obj["BridgeMaxAge"]
            print "Bridge Priority: ", obj["Priority"]
            print "Time Since Topology Change: UNSUPPORTED" #nextStpBridgeState.Dot1dStpTimeSinceTopologyChange uint32 //The time (in hundredths of a second) since the last time a topology change was detected by the bridge entity. For RSTP, this reports the time since the tcWhile timer for any port on this Bridge was nonzero.
            print "Topology Changes: UNSUPPORTED" #nextStpBridgeState.Dot1dStpTopChanges              uint32 //The total number of topology changes detected by this bridge since the management entity was last reset or initialized.
            print "Root Bridge Id: ", obj["DesignatedRoot"]
            print "Root Cost: ", obj["RootCost"]
            print "Root Port: ", obj["RootPort"]
            print "Max Age: ", obj["MaxAge"]
            print "Hello Time: ", obj["HelloTime"]
            print "Hold Time: UNSUPPORTED" #Dot1dStpHoldTime = int32(b.TxHoldCount)
            print "Forwarding Delay: ", obj["ForwardDelay"]
            print "Bridge Vlan: ", obj["Vlan"] if obj["Vlan"] not in (0, 4095) else "rstp"


    def printStpBridgeInstanceStates(self):

        brgs = self.swtch.getAllStpBridgeInstanceStates()

        print '\n\n---- STP Bridge DB----'
        if len(brgs):

            count = 0
            for data in brgs:
                obj = data['Object']
                print "BrgIfIndex: ", obj["IfIndex"]
                #print "Version: ", obj["ForceVersion"]
                print "Bridge Id: ", obj["Address"]
                print "Bridge Hello time: ", obj["BridgeHelloTime"]
                print "Bridge TxHold: ", obj["TxHoldCount"]
                print "Bridge Forwarding Delay: ", obj["BridgeForwardDelay"]
                print "Bridge Max Age: ", obj["BridgeMaxAge"]
                print "Bridge Priority: ", obj["Priority"]
                print "Time Since Topology Change: UNSUPPORTED" #nextStpBridgeState.Dot1dStpTimeSinceTopologyChange uint32 //The time (in hundredths of a second) since the last time a topology change was detected by the bridge entity. For RSTP, this reports the time since the tcWhile timer for any port on this Bridge was nonzero.
                print "Topology Changes: UNSUPPORTED" #nextStpBridgeState.Dot1dStpTopChanges              uint32 //The total number of topology changes detected by this bridge since the management entity was last reset or initialized.
                print "Root Bridge Id: ", obj["DesignatedRoot"]
                print "Root Cost: ", obj["RootCost"]
                print "Root Port: ", obj["RootPort"]
                print "Max Age: ", obj["MaxAge"]
                print "Hello Time: ", obj["HelloTime"]
                print "Hold Time: UNSUPPORTED" #Dot1dStpHoldTime = int32(b.TxHoldCount)
                print "Forwarding Delay: ", obj["ForwardDelay"]
                print "Bridge Vlan: ", obj["Vlan"] if obj["Vlan"] not in (0, 4095) else "rstp"
                print "=====================================================================================\n\n"




        else:
            print 'No Spanning Tree Instances provisioned\n'

    def printStpPortState(self, IntfRef, Vlan, addHeader=True, brief=None):
        stateDict = {
            1 : "Disabled",
            2 : "Blocked",
            3 : "Listening",
            4 : "Learning",
            5 : "Forwarding",
            6 : "Broken",
        }
        linkTypeDict = {
            0 : "LAN",
            1 : "P2P",
        }


        rawobj = self.swtch.getStpPortState(IntfRef, Vlan)
        if rawobj.status_code in self.httpSuccessCodes:
            dataobj = rawobj.json()
            obj = dataobj['Object']
            bainconsistant = "(inconsistant)" if obj["BridgeAssuranceInconsistant"] else ""
            print "IntfRef %s of Vlan %s is %s %s" %(obj["IntfRef"], obj["Vlan"], stateDict[obj["State"]], bainconsistant)
            #print "Enabled %s, Protocol Migration %s" %(obj["Enable"], obj["ProtocolMigration"])
            print "Enabled %s" %(obj["Enable"] == 1,)
            print "Port path cost %s, Port priority %s, Port Identifier %s" %(obj["PathCost32"], obj["Priority"], obj["IntfRef"])
            print "Designated root has bridge id %s" %(obj["DesignatedRoot"])
            print "Designated bridge has bridge id %s" %(obj["DesignatedBridge"])
            print "Designated port id %s, designated path cost %s admin path cost %s" %(obj["DesignatedPort"], obj["DesignatedCost"], obj["AdminPathCost"])
            print "Root Timers: max age %s, forward delay %s, hello %s" %(obj["MaxAge"],obj["ForwardDelay"],obj["HelloTime"],)
            print "Number of transitions to forwarding state: %s" %(obj["ForwardTransitions"],)
            print "AdminEdge %s OperEdge %s" %(obj["AdminEdgePort"] == 1, obj["OperEdgePort"] == 1)
            print "Bridge Assurance %s Bpdu Guard %s" %(obj["BridgeAssurance"] == 1, obj["BpduGuard"] == 1)
            print "Link Type %s" %("UNSUPPORTED",)
            print "\nPort Timers: (current tick(seconds) count)"
            print "EdgeDelayWhile:\t", obj["EdgeDelayWhile"]
            print "FdWhile:       \t", obj["FdWhile"]
            print "HelloWhen:     \t", obj["HelloWhen"]
            print "MdelayWhile:   \t", obj["MdelayWhile"]
            print "RbWhile:       \t", obj["RbWhile"]
            print "RcvdInfoWhile  \t", obj["RcvdInfoWhile"]
            print "RrWhile:       \t", obj["RrWhile"]
            print "TcWhile:       \t", obj["TcWhile"]
            print "\nCounters:"
            print "        %13s%13s" %("RX", "TX")
            print "BPDU    %13s%13s" %(obj["BpduInPkts"], obj["BpduOutPkts"])
            print "STP     %13s%13s" %(obj["StpInPkts"], obj["StpOutPkts"])
            print "TC      %13s%13s" %(obj["TcInPkts"], obj["TcOutPkts"])
            print "TC ACK  %13s%13s" %(obj["TcAckInPkts"], obj["TcAckOutPkts"])
            print "RSTP    %13s%13s" %(obj["RstpInPkts"], obj["RstpOutPkts"])
            print "PVST    %13s%13s" %(obj["PvstInPkts"], obj["PvstOutPkts"])
            print "\nFSM States:"
            print "PIM - Port Information, PRTM - Port Role Transition, PRXM - Port Receive"
            print "PSTM - Port State Transition, PPM - Port Protocol Migration, PTXM - Port Transmit"
            print "PTIM - Port Timer, BDM - Bridge Detection, TCM - Topology Change"
            print "MACHINE       %20s%20s" %("CURRENT", "PREVIOUS")
            print "PIM           %20s%20s" %(obj["PimCurrState"], obj["PimPrevState"])
            print "PRTM          %20s%20s" %(obj["PrtmCurrState"], obj["PrtmPrevState"])
            print "PRXM          %20s%20s" %(obj["PrxmCurrState"], obj["PrxmPrevState"])
            print "PSTM          %20s%20s" %(obj["PstmCurrState"], obj["PstmPrevState"])
            print "PPM           %20s%20s" %(obj["PpmCurrState"], obj["PpmPrevState"])
            print "PTXM          %20s%20s" %(obj["PtxmCurrState"], obj["PtxmPrevState"])
            print "PTIM          %20s%20s" %(obj["PtimCurrState"], obj["PtimPrevState"])
            print "BDM           %20s%20s" %(obj["BdmCurrState"], obj["BdmPrevState"])
            print "TCM           %20s%20s" %(obj["TcmCurrState"], obj["TcmPrevState"])


    def printStpPortStates(self):
        stateDict = {
            1 : "Disabled",
            2 : "Blocked",
            3 : "Listening",
            4 : "Learning",
            5 : "Forwarding",
            6 : "Broken",
        }
        linkTypeDict = {
            0 : "LAN",
            1 : "P2P",
        }

        ports = self.swtch.getAllStpPortStates()

        if len(ports):
            print '\n\n---- STP PORT DB----'
            for data in ports:
                obj = data['Object']
                bainconsistant = "(inconsistant)" if obj["BridgeAssuranceInconsistant"] == 1 else ""
                print "IntfRef %s of Vlan %s is %s %s" %(obj["IntfRef"], obj["Vlan"], stateDict[obj["State"]], bainconsistant)
                #print "Enabled %s, Protocol Migration %s" %(obj["Enable"], obj["ProtocolMigration"])
                print "Enabled %s" %(obj["Enable"],)
                print "Port path cost %s, Port priority %s, Port Identifier %s" %(obj["PathCost32"], obj["Priority"], obj["IntfRef"])
                print "Designated root has bridge id %s" %(obj["DesignatedRoot"])
                print "Designated bridge has bridge id %s" %(obj["DesignatedBridge"])
                print "Designated port id %s, designated path cost %s admin path cost %s" %(obj["DesignatedPort"], obj["DesignatedCost"], obj["AdminPathCost"])
                print "Root Timers: max age %s, forward delay %s, hello %s" %(obj["MaxAge"],obj["ForwardDelay"],obj["HelloTime"],)
                print "Number of transitions to forwarding state: %s" %(obj["ForwardTransitions"],)
                print "AdminEdge %s OperEdge %s" %(obj["AdminEdgePort"], obj["OperEdgePort"])
                print "Bridge Assurance %s Bpdu Guard %s" %(obj["BridgeAssurance"], obj["BpduGuard"])
                print "Link Type %s" %("UNSUPPORTED",)
                print "\nPort Timers: (current tick(seconds) count)"
                print "EdgeDelayWhile:\t", obj["EdgeDelayWhile"]
                print "FdWhile:       \t", obj["FdWhile"]
                print "HelloWhen:     \t", obj["HelloWhen"]
                print "MdelayWhile:   \t", obj["MdelayWhile"]
                print "RbWhile:       \t", obj["RbWhile"]
                print "RcvdInfoWhile  \t", obj["RcvdInfoWhile"]
                print "RrWhile:       \t", obj["RrWhile"]
                print "TcWhile:       \t", obj["TcWhile"]
                print "\nCounters:"
                print "        %13s%13s" %("RX", "TX")
                print "BPDU    %13s%13s" %(obj["BpduInPkts"], obj["BpduOutPkts"])
                print "STP     %13s%13s" %(obj["StpInPkts"], obj["StpOutPkts"])
                print "TC      %13s%13s" %(obj["TcInPkts"], obj["TcOutPkts"])
                print "TC ACK  %13s%13s" %(obj["TcAckInPkts"], obj["TcAckOutPkts"])
                print "RSTP    %13s%13s" %(obj["RstpInPkts"], obj["RstpOutPkts"])
                print "PVST    %13s%13s" %(obj["PvstInPkts"], obj["PvstOutPkts"])
                print "\nFSM States:"
                print "PIM - Port Information, PRTM - Port Role Transition, PRXM - Port Receive"
                print "PSTM - Port State Transition, PPM - Port Protocol Migration, PTXM - Port Transmit"
                print "PTIM - Port Timer, BDM - Bridge Detection, TCM - Topology Change"
                print "MACHINE       %20s%20s" %("CURRENT", "PREVIOUS")
                print "PIM           %20s%20s" %(obj["PimCurrState"], obj["PimPrevState"])
                print "PRTM          %20s%20s" %(obj["PrtmCurrState"], obj["PrtmPrevState"])
                print "PRXM          %20s%20s" %(obj["PrxmCurrState"], obj["PrxmPrevState"])
                print "PSTM          %20s%20s" %(obj["PstmCurrState"], obj["PstmPrevState"])
                print "PPM           %20s%20s" %(obj["PpmCurrState"], obj["PpmPrevState"])
                print "PTXM          %20s%20s" %(obj["PtxmCurrState"], obj["PtxmPrevState"])
                print "PTIM          %20s%20s" %(obj["PtimCurrState"], obj["PtimPrevState"])
                print "BDM           %20s%20s" %(obj["BdmCurrState"], obj["BdmPrevState"])
                print "TCM           %20s%20s" %(obj["TcmCurrState"], obj["TcmPrevState"])
                print "====================================================================="
        else:
            print 'No Data To Display for %s' %('StpPortStates')

    def printLaPortChannelStates(self, brief=False):

        # YANG MODEL REPRESENTATION
        RxMachineStateDict = {
            0 : "RX_CURRENT",
            1 : "RX_EXPIRED",
            2 : "RX_DEFAULTED",
            3 : "RX_INITIALIZE",
            4 : "RX_LACP_DISABLED",
            5 : "RX_PORT_DISABLE",
        }

        MuxMachineStateDict = {
            0 : "MUX_DETACHED",
            1 : "MUX_WAITING",
            2 : "MUX_ATTACHED",
            3 : "MUX_COLLECTING",
            4 : "MUX_DISTRIBUTING",
            5 : "MUX_COLLECTING_DISTRIBUTING",
        }

        ChurnMachineStateDict = {
            0 : "CDM_NO_CHURN",
            1 : "CDM_CHURN",
        }

        '''
        //Collecting bool
        // parent leaf
        //OperKey uint16
        // parent leaf
        //PartnerId string
        // parent leaf
        //Interface string
        // parent leaf
        //Synchronization int32
        // parent leaf
        //Aggregatable bool
        // parent leaf
        Mtu uint16
        // parent leaf
        //LacpMode int32
        // parent leaf
        //PartnerKey uint16
        // parent leaf
        Description string
        // parent leaf
        //SystemIdMac string
        // parent leaf
        //LagType int32
        // parent leaf
        //SystemId string
        // parent leaf
        //Interval int32
        // parent leaf
        //Enabled bool
        // parent leaf
        //NameKey string `SNAPROUTE: KEY`
        // parent leaf
        //Distributing bool
        // parent leaf
        //Timeout int32
        // parent leaf
        //Activity int32
        // parent leaf
        //SystemPriority uint16
        // parent leaf
        Type string
        // parent leaf
        MinLinks uint16
        //yang_name: lacp-in-pkts class: leaf
        //LacpInPkts uint64
        //yang_name: lacp-out-pkts class: leaf
        //LacpOutPkts uint64
        //yang_name: lacp-rx-errors class: leaf
        //LacpRxErrors uint64
        //yang_name: lacp-tx-errors class: leaf
        //LacpTxErrors uint64
        //yang_name: lacp-unknown-errors class: leaf
        //LacpUnknownErrors uint64
        //yang_name: lacp-errors class: leaf
        //LacpErrors uint64
        '''

        portchannels = self.swtch.getAllLaPortChannelStates()
        members = self.swtch.getAllLaPortChannelIntfRefListStates()

        if not portchannels:
            print 'No Data To Display for %s' %('LaPortChannelState')

        for portchannel in portchannels:
            lag = portchannel['Object']
            print 'IntfRef: %s' %(lag['IntfRef']) + ' IfIndex: %s' %(lag['IfIndex']) 
            labels = ('LagType','Interval','Mode','System Id', 'System Priority', 'Hash Mode', 'OperState', 'Members', 'Members Up in Bundle')
            rows=[]

            rows.append(("LACP" if int(lag['LagType']) == 0 else "STATIC",
                         "FAST" if int(lag['Interval']) == 0 else "SLOW",
                         "ACTIVE" if int(lag['LacpMode']) == 0 else "PASSIVE",
                         "%s" %(lag['SystemIdMac']),
                         "%s" %(lag["SystemPriority"]),
                         "%s" %(lag['LagHash']),
                         "%s" %(lag['OperState']),
                         "%s" %(lag['IntfRefList']),
                         "%s" %(lag['IntfRefListUpInBundle'])))
            width = 20
            print indent([labels]+rows, hasHeader=False, separateRows=True,
                 prefix='| ', postfix=' |',
                 wrapfunc=lambda x: wrap_onspace_strict(x,width))

            # TODO dump the LAG group info
            if not brief:
                if not members:
                    print 'No Data To Display for %s' %('LaPortChannelIntfRefListState')

                for d in [m['Object'] for m in members if m['Object']['LagIntfRef'] == lag['IntfRef']]:

                    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                    print 'IfIndex: ' + "%s" % d['IfIndex'] + 'Name: ' + "%s" %d['IntfRef'] + ' LagIntfRef: ' + "%s" %d['LagIntfRef']
                    print 'OperState: ' + d['OperState']
                    #print 'lagtype: ' + ('LACP' if not d['LagType'] else 'STATIC')
                    print 'operkey: %s' % d['OperKey']
                    #print 'mode: ' + ('ACTIVE' if not d['LacpMode'] else 'PASSIVE')
                    #print 'interval: %s' % (('SLOW' if d['Interval'] else 'FAST'))
                    #print 'system:\n'
                    #print '\tsystemmac: %s' % d['SystemIdMac']
                    #print '\tsysteprio: %s' % d['SystemPriority']
                    #print '\tsystemId: %s' % d['SystemId']
                    print 'actor:'
                    stateStr = '\tstate: '
                    for s in ('Activity', 'Timeout', 'Aggregatable', 'Synchronization', 'Collecting', 'Distributing', 'Defaulted'):
                        if s == 'Synchronization' and not d[s]:
                            stateStr += s + ', '
                        elif s == 'Activity' and not d[s]:
                            stateStr += s + ', '
                        elif s in ('Activity', 'Synchronization'):
                            continue
                        elif d[s]:
                            stateStr += s + ', '
                    print stateStr.rstrip(',')

                    print '\tstats:'
                    for s in ('LacpInPkts', 'LacpOutPkts', 'LacpRxErrors', 'LacpTxErrors', 'LacpUnknownErrors', 'LacpErrors', 'LampInPdu', 'LampOutPdu', 'LampInResponsePdu', 'LampOutResponsePdu'):
                        print '\t' + s, ': ', d[s]

                    print 'partner:\n'
                    print '\t' + 'key: %s' % d['PartnerKey']
                    print '\t' + 'partnerid: ' + d['PartnerId']

                    print 'debug:\n'
                    try:
                        print '\t' + 'debugId: %s' % d['DebugId']
                        print '\t' + 'RxMachineState: %s' % RxMachineStateDict[d['RxMachine']]
                        print '\t' + 'RxTime (rx pkt rcv): %s' % d['RxTime']
                        print '\t' + 'MuxMachineState: %s' % MuxMachineStateDict[d['MuxMachine']]
                        print '\t' + 'MuxReason: %s' % d['MuxReason']
                        print '\t' + 'Actor Churn State: %s' % ChurnMachineStateDict[d['ActorChurnMachine']]
                        print '\t' + 'Partner Churn State: %s' % ChurnMachineStateDict[d['PartnerChurnMachine']]
                        print '\t' + 'Actor Churn Count: %s' % d['ActorChurnCount']
                        print '\t' + 'Partner Churn Count: %s' % d['PartnerChurnCount']
                        print '\t' + 'Actor Sync Transition Count: %s' % d['ActorSyncTransitionCount']
                        print '\t' + 'Partner Sync Transition Count: %s' % d['PartnerSyncTransitionCount']
                        print '\t' + 'Actor LAG ID change Count: %s' % d['ActorChangeCount']
                        print '\t' + 'Partner LAG ID change Count: %s' % d['PartnerChangeCount']
                    except Exception as e:
                        print e


    def printBGPv4RouteStates(self, ):
        routes = self.swtch.getAllBGPv4RouteStates()
        #bgpglobal = self.swtch.getAllBGPGlobals()
        labels = ('Network', 'NextHop','BP', 'MP', 'Metric', 'LocalPref', 'Updated', 'Path')
        rows = []
        lines = sorted(routes, key=lambda k: k['Object'].get('Network', 0))  	
        for r in lines:
            rt = r['Object']
            if rt['Paths'] is None:
                continue
            for p in rt['Paths']:
                if p['Path'] is None:
                    bgp_path = p['Path']
                else:
                    bgp_path = [x.encode('utf-8') for x in p['Path']]

                rows.append((rt['Network']+"/"+str(rt['CIDRLen']),
                            "%s" %(p['NextHop']),
                            "%s" %(p['BestPath']),
                            "%s" %(p['MultiPath']),
                            "%s" %(p['Metric']),
                            "%s" %(p['LocalPref']),
                            "%s" %(p['UpdatedTime'].split(".")[0]),
                            "%s" %(bgp_path)))
        width = 30
        print indent([labels]+rows, hasHeader=True, separateRows=False,
                     prefix=' ', postfix=' ', headerChar= '-', delim='    ',
                     wrapfunc=lambda x: wrap_onspace_strict(x,width))

    def printBGPv6RouteStates(self, ):
        routes = self.swtch.getAllBGPv6RouteStates()
        bgpglobal = self.swtch.getAllBGPGlobals()
        labels = ('Network', 'NextHop','BP', 'MP', 'Metric', 'LocalPref', 'Updated', 'Path')
        rows = []
        lines = sorted(routes, key=lambda k: k['Object'].get('Network', 0))  	
        for r in lines:
            rt = r['Object']
            if rt['Paths'] is None:
                continue
            for p in rt['Paths']:
                if p['Path'] is None:
                    bgp_path = p['Path']
                else:
                    bgp_path = [x.encode('utf-8') for x in p['Path']]

                rows.append((rt['Network']+"/"+str(rt['CIDRLen']),
                            "%s" %(p['NextHop']),
                            "%s" %(p['BestPath']),
                            "%s" %(p['MultiPath']),
                            "%s" %(p['Metric']),
                            "%s" %(p['LocalPref']),
                            "%s" %(p['UpdatedTime'].split(".")[0]),
                            "%s" %(bgp_path)))
        width = 30
        print indent([labels]+rows, hasHeader=True, separateRows=False,
                     prefix=' ', postfix=' ', headerChar= '-', delim='    ',
                     wrapfunc=lambda x: wrap_onspace_strict(x,width))

    def printIPv4IntfStates(self,):
    	ipintfs = self.swtch.getAllIPv4IntfStates()
    	r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
    	print '\n'
    	labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
    	rows =[]
    	for i in lines:
            ip = i['Object']    
            rows.append((ip['IntfRef'],
                        "%s" %(ip['IpAddr']),
                        "%s" %(ip['OperState']),
                        "%s" %(ip['NumDownEvents']),
                        "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('IPv6IntfStates',
                            labels,
                            rows)

    def printEthIPv4IntfStates(self,):
        ipintfs = self.swtch.getAllIPv4IntfStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
        print '\n'
        labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
        rows = []
        for i in lines:
            ip = i['Object']
            if ip['L2IntfType'] == 'Port':
                rows.append((ip['IntfRef'],
                        "%s" %(ip['IpAddr']),
                        "%s" %(ip['OperState']),
                        "%s" %(ip['NumDownEvents']),
                        "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('EthIPv4IntfStates',
                            labels,
                            rows)

    def printSviIPv4IntfStates(self,):
        ipintfs = self.swtch.getAllIPv4IntfStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
        print '\n'
        labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
        rows = []
        for i in lines:
            ip = i['Object']
            if ip['L2IntfType'] == 'Vlan':
                rows.append((ip['IntfRef'],
                        "%s" %(ip['IpAddr']),
                        "%s" %(ip['OperState']),
                        "%s" %(ip['NumDownEvents']),
                        "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('SviIPv4IntfStates',
                            labels,
                            rows)

    def printLagIPv4IntfStates(self,):
        ipintfs = self.swtch.getAllIPv4IntfStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
        print '\n'
        labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
        rows = []
        for i in lines:
            ip = i['Object']
            if ip['L2IntfType'] == 'Lag':
                rows.append((ip['IntfRef'],
                            "%s" %(ip['IpAddr']),
                            "%s" %(ip['OperState']),
                            "%s" %(ip['NumDownEvents']),
                            "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('LagIPv4IntfStates',
                            labels,
                            rows)

    def printLoIPv4IntfStates(self,):
    	ipintfs = self.swtch.getAllLogicalIntfStates()
    	r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
    	print '\n'
    	labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
        rows = []
        for i in lines:
            ip = i['Object']
            if ip['L2IntfType'] == 'Loopback':
                rows.append((ip['IntfRef'],
                            "%s" %(ip['IpAddr']),
                            "%s" %(ip['OperState']),
                            "%s" %(ip['NumDownEvents']),
                            "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('LagIPv4IntfStates',
                            labels,
                            rows)
                            
    def printIPv6IntfStates(self,):
		ipintfs = self.swtch.getAllIPv6IntfStates()
		r = re.compile("([a-zA-Z]+)([0-9]+)")
		lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
		print '\n'
		labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
		rows=[]
		for i in lines:
			ip = i['Object']    
			rows.append((ip['IntfRef'],
                        "%s" %(ip['IpAddr']),
                        "%s" %(ip['OperState']),
                        "%s" %(ip['NumDownEvents']),
                        "%s" %(ip['LastDownEventTime'])))
		self.tblPrintObject('IPv6IntfStates',
                            labels,
                            rows)
       
        
        
    def printEthIPv6IntfStates(self,):
        ipintfs = self.swtch.getAllIPv6IntfStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
        print '\n'
        labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
        rows = []
        for i in lines:
            ip = i['Object']
            if ip['L2IntfType'] == 'Port':
                rows.append((ip['IntfRef'],
                        "%s" %(ip['IpAddr']),
                        "%s" %(ip['OperState']),
                        "%s" %(ip['NumDownEvents']),
                        "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('EthIPv6IntfStates',
                            labels,
                            rows)

    def printSviIPv6IntfStates(self,):
        ipintfs = self.swtch.getAllIPv6IntfStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
        print '\n'
        labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
        rows = []
        for i in lines:
            ip = i['Object']
            if ip['L2IntfType'] == 'Vlan':
                rows.append((ip['IntfRef'],
                        "%s" %(ip['IpAddr']),
                        "%s" %(ip['OperState']),
                        "%s" %(ip['NumDownEvents']),
                        "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('SviIPv6IntfStates',
                            labels,
                            rows)

    def printLagIPv6IntfStates(self,):
        ipintfs = self.swtch.getAllIPv6IntfStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
        print '\n'
        labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
        rows = []
        for i in lines:
            ip = i['Object']
            if ip['L2IntfType'] == 'Lag':
                rows.append((ip['IntfRef'],
                            "%s" %(ip['IpAddr']),
                            "%s" %(ip['OperState']),
                            "%s" %(ip['NumDownEvents']),
                            "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('LagIPv6IntfStates',
                            labels,
                            rows)

    def printLoIPv6IntfStates(self,):
        ipintfs = self.swtch.getAllLogicalIntfStates()
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        lines = sorted(ipintfs, key=lambda k: int(r.match(k['Object'].get('IntfRef', 0)).group(2)))
        print '\n'
        labels = ('Interface', 'IP Address', 'OperState', 'DownEvents','Last Flap')
        rows = []
        for i in lines:
            ip = i['Object']
            if ip['L2IntfType'] == 'Loopback':
                rows.append((ip['IntfRef'],
                            "%s" %(ip['IpAddr']),
                            "%s" %(ip['OperState']),
                            "%s" %(ip['NumDownEvents']),
                            "%s" %(ip['LastDownEventTime'])))

        self.tblPrintObject('LagIPv4IntfStates',
                            labels,
                            rows)

    def printBGPv4NeighborStates(self):	   
       sessionState=  {  0: "Resolving Peer", 1: "Idle",
                 2: "Connect",
                 3: "Active",
                 4: "OpenSent",
                 5: "OpenConfirm",
                 6: "Established"
               }

       peers = self.swtch.getAllBGPv4NeighborStates()
 	
       if len(peers)>=0:
           print '\n'
           labels = ('Neighbor','LocalAS','PeerAS','State','RxMsg','TxMsg','Description','Prefixes_Rcvd', 'ElapsedTime')
           rows=[]
           lines = sorted(peers, key=lambda k: k['Object'].get('NeighborAddress', 0)) 
           for p in lines:
               pr = p['Object']
               RXmsg = (pr['Messages']['Received']['Notification']) + (pr['Messages']['Received']['Update'])
               TXmsg = (pr['Messages']['Sent']['Notification']) + (pr['Messages']['Sent']['Update'])
               StartTime = pr.get('SessionStateUpdatedTime',  pr.get('SessionStateDuration', 0))
               #"2016-09-20 11:42:01.290081007 -0700 PDT"
               #start = datetime.strptime(StartTime, '%Y-%m-%d %I:%M:%S.%f %z %Z')
               #UpTime = datetime.datetime.now() - start 
               rows.append( (pr['NeighborAddress'],
                     "%s" %(pr['LocalAS']),
                     "%s" %(pr['PeerAS']),
                     "%s" %(sessionState[pr['SessionState']]),
                     "%s" %(RXmsg),
                     "%s" %(TXmsg),
                     "%s" %(pr['Description']),
                     "%s" %(pr['TotalPrefixes']), 
                     "%s" %(StartTime) ))


           self.tblPrintObject('BGPNeighborStates',
                            labels,
                            rows)

    def printBGPv6NeighborStates(self):	   
       sessionState=  {  0: "Resolving Peer", 1: "Idle",
                 2: "Connect",
                 3: "Active",
                 4: "OpenSent",
                 5: "OpenConfirm",
                 6: "Established"
               }

       peers = self.swtch.getAllBGPv6NeighborStates()
       if len(peers)>=0:
           print '\n'
           labels = ('Neighbor','LocalAS','PeerAS','State','RxMsg','TxMsg','Description','Prefixes_Rcvd')
           rows=[]
           lines = sorted(peers, key=lambda k: k['Object'].get('NeighborAddress', 0)) 
           for p in lines:
               pr = p['Object']
               RXmsg = (pr['Messages']['Received']['Notification']) + (pr['Messages']['Received']['Update'])
               TXmsg = (pr['Messages']['Sent']['Notification']) + (pr['Messages']['Sent']['Update'])
               rows.append( (pr['NeighborAddress'],
                     "%s" %(pr['LocalAS']),
                     "%s" %(pr['PeerAS']),
                     "%s" %(sessionState[pr['SessionState']]),
                     "%s" %(RXmsg),
                     "%s" %(TXmsg),
                     "%s" %(pr['Description']),
                     "%s" %(pr['TotalPrefixes'])))


           self.tblPrintObject('BGPNeighborStates',
                            labels,
                            rows)



    def printBfdSessionStates(self):
        peers = self.swtch.getAllBfdSessionStates()
        if len(peers)>=0:
            print '\n'
            labels = ('NeighAddr','LD/RD','Protocols','Multi','TxInt','RxInt','State','Int','TxPkts','RxPkts','Uptime')
            rows=[]
            lines = sorted(peers, key=lambda k: k['Object'].get('IpAddr', 0))
            for p in lines:
                pr = p['Object']
                desc = str(pr['LocalDiscriminator'])+"/"+str(pr['RemoteDiscriminator'])
                multi = pr['DetectionMultiplier']
                rows.append( (pr['IpAddr'],
                      "%s" %(desc),
                      "%s" %(pr['RegisteredProtocols']),
                      "%s" %(pr['DetectionMultiplier']),
                      "%s" %(pr['DesiredMinTxInterval']),
                      "%s" %(pr['RequiredMinRxInterval']),
                      "%s" %(pr['RemoteSessionState']),
                      "%s" %(pr['IntfRef']),
                      "%s" %(pr['NumTxPackets']),
                      "%s" %(pr['NumRxPackets']),
                      "%s" %(pr['UpDuration'])))

            self.tblPrintObject('BfdSessionStates',
                            labels,
                            rows)

            #width = 20
            #print indent([labels]+rows, hasHeader=True, separateRows=False,
            #            prefix=' ', postfix=' ', headerChar= '-', delim='    ',
            #            wrapfunc=lambda x: wrap_onspace_strict(x,width))

   # def printInterfaces(self):

    #    print "CODE NEEDED FOR printInterfaces in flexprint.py"

    def printSystemSwVersionStates(self):

        httpSuccessCodes = [200, 201, 202, 204]

        r = self.swtch.getSystemSwVersionState("")
        if r.status_code in httpSuccessCodes:
            obj = r.json()
            o = obj['Object']
            print "flexswitch version: %s\n" %(o['FlexswitchVersion'])
            print "git repo details:\n"
            labels = ('Repo Name','Git Commit Sha1','Branch Name','Build Time')
            rows=[]
            for repo in o['Repos']:
                rows.append( (repo['Name'],
                         "%s" %(repo['Sha1']),
                         "%s" %(repo['Branch']),
                         "%s" %(repo['Time'])) )

            self.tblPrintObject('SystemSwVersionState',
                            labels,
                            rows)

            #width = 20
            #print indent([labels]+rows, hasHeader=True, separateRows=True,
            #     prefix='| ', postfix=' |',
            #     wrapfunc=lambda x: wrap_onspace_strict(x,width))

    def printSystemStatusStates(self):
        header = []; rows = []
        header.append('Name')
        header.append('Ready')
        header.append('Reason')
        header.append('UpTime')
        header.append('NumCreateCalls')
        header.append('NumDeleteCalls')
        header.append('NumUpdateCalls')
        header.append('NumGetCalls')
        header.append('NumActionCalls')

        r = self.swtch.getSystemStatusState("")
        obj = r.json()
        o = obj['Object']
        values = []
        values.append('%s' % o['Name'])
        values.append('%s' % o['Ready'])
        values.append('%s' % o['Reason'])
        values.append('%s' % o['UpTime'])
        values.append('%s' % o['NumCreateCalls'])
        values.append('%s' % o['NumDeleteCalls'])
        values.append('%s' % o['NumUpdateCalls'])
        values.append('%s' % o['NumGetCalls'])
        values.append('%s' % o['NumActionCalls'])
        rows.append(values)
        self.tblPrintObject('SystemStatusState', header, rows)

if __name__=='__main__':
    pass
