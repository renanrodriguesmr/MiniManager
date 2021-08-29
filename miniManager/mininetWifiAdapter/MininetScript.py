import math
import time

from mininet.node import Controller
# from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
# from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


class MininetScript():
    def __init__(self):
        self.__delay = 1

    def run(self):
        self.__start = time.time()
        self._topology()

    def _topology(self):
        print(1)
        net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference, noise_th=-91, fading_cof=3)
        print(2)
        ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36', position='15,30,0')
        print(3)
        net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', min_x=10, max_x=30, min_y=50, max_y=70, min_v=5, max_v=10)
        print(4)
        net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', min_x=0, max_x=60, min_y=25, max_y=80, min_v=2, max_v=10)
        print(5)
        net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8', min_x=60, max_x=70, min_y=10, max_y=20, min_v=1, max_v=5)
        c1 = net.addController('c1')
        net.setPropagationModel(model="logDistance", exp=4)
        net.configureWifiNodes()
        nodes = net.stations
        net.setMobilityModel(time=0, model='RandomDirection',max_x=90, max_y=90, seed=20)
        net.build()
        c1.start()
        ap1.start([c1])

        while True:
            self._monNode(nodes)
            time.sleep(self.__delay)

        net.stop()

    def _monNode(self, nwnode):
        attrList=['name','rssi','channel','band','ssid','txpower','ip']
        partialResult = []
        for eachNode in nwnode:
            measObj = {}
            measObj["time"] = math.floor(time.time() - self.__start)
            measObj["position"] = list(eachNode.position)
            measObj["associatedTo"] = "None"
            if eachNode.wintfs[0].associatedTo:
                    measObj["associatedTo"] = eachNode.wintfs[0].associatedTo.node.wintfs[0].name

            for eachAttr in attrList:
                var=getattr(eachNode.wintfs[0],eachAttr)
                measObj[eachAttr] = var

            partialResult.append(measObj)

        print({"partialResult" : partialResult})


if __name__ == '__main__':
    script = MininetScript()
    print("run")
    script.run()