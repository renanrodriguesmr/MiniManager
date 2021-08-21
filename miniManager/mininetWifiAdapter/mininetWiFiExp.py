import time
import math

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

class MininetWifiExp():

    DELAY = 2

    def __init__(self, notifier):
        self.__notifier = notifier
        self.__active = False
        self.__start = None

    def run(self):
        # mockResult = MininetWifiExp._getMockResult()
        self.__active = True
        self.__start = time.time()


        self.topology()

        #while self.__active:
        #    for key in mockResult:
        #        self.__notifier.notify(mockResult[key])
        #    time.sleep(MininetWifiExp.DELAY)        

    def finish(self):
        self.__active = False

    def _getMockResultLine(time,position,name,rssi,channel,band,ssid,txpower,associatedTo,ip):
        return { "time": time, "name": name, "position": position, "rssi": rssi, "channel": channel, "band": band, "ssid": ssid, "txpower": txpower, "associatedTo": associatedTo, "ip": ip }

    def _getMockResult():
        l1 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:37 2021', (12.44, 58.0, 0.0), 'sta1-wlan0', -79.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
        l2 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:37 2021', (59.24, 60.16, 0.0), 'sta2-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.2')
        l3 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:37 2021', (68.27, 11.02, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
        l4 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:38 2021', (28.79, 57.54, 0.0), 'sta1-wlan0', -81.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
        l5 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:38 2021', (43.83, 40.01, 0.0), 'sta2-wlan0', -81.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
        l6 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:38 2021', (66.74, 11.1, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
        l7 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:39 2021', (10.49, 56.88, 0.0), 'sta1-wlan0', -79.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
        l8 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:39 2021', (33.21, 66.45, 0.0), 'sta2-wlan0', -86.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
        l9 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:39 2021', (63.88, 11.9, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
        l10 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:40 2021', (24.26, 61.75, 0.0), 'sta1-wlan0', -82.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
        l11 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:40 2021', (27.06, 55.15, 0.0), 'sta2-wlan0', -79.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
        l12 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:40 2021', (67.56, 14.09, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
        l13 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:41 2021', (15.76, 52.93, 0.0), 'sta1-wlan0', -76.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
        l14 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:41 2021', (31.23, 66.51, 0.0), 'sta2-wlan0', -86.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
        l15 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:41 2021', (68.88, 16.26, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
        l16 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:42 2021', (27.42, 53.61, 0.0), 'sta1-wlan0', -79.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
        l17 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:42 2021', (29.02, 75.3, 0.0), 'sta2-wlan0', -89.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
        l18 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:42 2021', (66.73, 16.24, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
        l19 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:43 2021', (10.56, 69.96, 0.0), 'sta1-wlan0', -85.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
        l20 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:43 2021', (11.43, 60.52, 0.0), 'sta2-wlan0', -81.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
        l21 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:43 2021', (60.4, 17.13, 0.0), 'sta3-wlan0', -88.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.3')
        l22 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:44 2021', (12.67, 67.57, 0.0), 'sta1-wlan0', -85.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
        l23 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:44 2021', (8.48, 59.23, 0.0), 'sta2-wlan0', -81.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
        l24 = MininetWifiExp._getMockResultLine('Mon Aug  9 22:24:44 2021', (65.33, 12.52, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')

        result = {
            1: [l1,l2,l3],
            2: [l4,l5,l6],
            3: [l7,l8,l9],
            4: [l10,l11,l12],
            5: [l13,l14,l15],
            6: [l16,l17,l18],
            7: [l19,l20,l21],
            8: [l22,l23,l24],
        }

        return result

    def topology(self):
        net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference, noise_th=-91, fading_cof=3)

        ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36', position='15,30,0')
        net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', min_x=10, max_x=30, min_y=50, max_y=70, min_v=5, max_v=10)
        net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', min_x=0, max_x=60, min_y=25, max_y=80, min_v=2, max_v=10)
        net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8', min_x=60, max_x=70, min_y=10, max_y=20, min_v=1, max_v=5)
        c1 = net.addController('c1')

        net.setPropagationModel(model="logDistance", exp=4)
        net.configureWifiNodes()

        nodes = net.stations

        net.setMobilityModel(time=0, model='RandomDirection',max_x=90, max_y=90, seed=20)
        net.build()
        c1.start()
        ap1.start([c1])
    
        while self.__active:
            self.monNode(nodes)
            time.sleep(1)

        net.stop()

    def monNode(self, nwnode):
        attrList=['name','rssi','channel','band','ssid','txpower','ip']
        partialResult = []
        for eachNode in nwnode:
            measObj = {}
            measObj["time"] = math.floor(time.time() - self.__start)
            measObj["position"] = eachNode.position
            measObj["associatedTo"] = None
            if eachNode.wintfs[0].associatedTo:
                    measObj["associatedTo"] = eachNode.wintfs[0].associatedTo.node.wintfs[0].name

            for eachAttr in attrList:
                var=getattr(eachNode.wintfs[0],eachAttr)
                measObj[eachAttr] = var

            partialResult.append(measObj)

        self.__notifier.notify(partialResult)