import math
import time
import json

from mininet.node import Controller
# from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
# from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

import constants

class MininetScript():
    ERROR_CONFIG = "error opening configurations"
    DELAY = 1

    def __init__(self):
        self._configuration = self._loadConfiguration()

    def _loadConfiguration(self):
        try:
            outfile = open(constants.MininetConstants.CONFIG_FILE_PATH, 'r')
            data = outfile.read()
            outfile.close()

            jsonParsed = json.loads(data)
            return json.loads(jsonParsed)
        except:
            print({constants.MininetConstants.ERROR_KEY: self.ERROR_CONFIG})

    def run(self):
        self.__start = time.time()
        nodes = self._topology()
        self._analyse(nodes)

    def _topology(self):
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

        return nodes

    def _analyse(self, nodes):
        while True:
            time.sleep(self.DELAY)
            
            currentTime = math.floor(time.time() - self.__start)
            measurements = self._getValidMeasurements(currentTime)
            if len(measurements) == 0:
                continue

            measurements.add("name")

            self._collectMetrics(measurements, nodes, currentTime)

    def _getValidMeasurements(self, currentTime):
            measurements = set()
            for measurement in self._configuration["measurements"]:
                if (currentTime % measurement["period"]) == 0:
                    measurements.add(measurement["measure"]["name"])

            return measurements

    def _collectMetrics(self, measurements, nodes, currentTime):
            partialResult = []
            for eachNode in nodes:
                measObj = {}
                measObj["time"] = currentTime

                for measurement in measurements:
                    measObj[measurement] = self._getMetricFromNode(measurement, eachNode)

                partialResult.append(measObj)

            print({constants.MininetConstants.PARTIAL_RESULT_KEY: partialResult})


    def _getMetricFromNode(self, measureName, node):
        attrList={'name', 'rssi','channel','band','ssid','txpower','ip'}

        if measureName in attrList:
            return getattr(node.wintfs[0],measureName)

        if measureName == "position":
            return list(node.position)

        #associatedTo
        if node.wintfs[0].associatedTo:
            return node.wintfs[0].associatedTo.node.wintfs[0].name

        return "None"


if __name__ == '__main__':
    script = MininetScript()
    script.run()