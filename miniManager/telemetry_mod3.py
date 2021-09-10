#!/usr/bin/python

'This uses telemetry() to enable a graph with live statistics'
import time

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference,
                       noise_th=-91, fading_cof=3)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36',
                             position='15,30,0')
    net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
                   min_x=10, max_x=30, min_y=50, max_y=70, min_v=5, max_v=10)
    net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8',
                   min_x=0, max_x=60, min_y=25, max_y=80, min_v=2, max_v=10)
    net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8',
                   min_x=60, max_x=70, min_y=10, max_y=20, min_v=1, max_v=5)
    c1 = net.addController('c1')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    nodes = net.stations

    net.plotGraph(max_x=100, max_y=100)
    net.setMobilityModel(time=0, model='RandomDirection',
                         max_x=90, max_y=90, seed=20)
    #net.stopMobility(time=120)


    #net.telemetry(nodes=nodes, single=True )
    #net.telemetry(nodes=nodes, single=True, data_type='position')

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
 
    for i in range (1,119):
        #net.iperf([nodes[0],nodes[1]])
        #print(time.ctime(time.time()), nodes[0].wintfs[0].rssi,nodes[0].wintfs[0].channel)
        monNode(nodes)
        time.sleep(1)

    info("*** Running CLI - my message\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

def monNode(nwnode):
    attrList=['name','rssi','channel','band','ssid','txpower','associatedTo','ip']
    #
    for eachNode in nwnode:
        measList=[]
        measList.append(time.ctime(time.time()))
        measList.append(eachNode.position)
        for eachAttr in attrList:
            var=getattr(eachNode.wintfs[0],eachAttr)
            measList.append(var)
        print(measList)


if __name__ == '__main__':
    setLogLevel('info')
    topology()


