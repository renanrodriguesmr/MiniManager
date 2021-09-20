import math
import time
import json
import threading

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

import constants
import measurers as meas

class MininetScript():
    ERROR_CONFIG = "error opening configurations"
    DELAY = 1

    def __init__(self):
        self.__configuration = self.__loadConfiguration()
        self.__radioFrequencyMeasurements, self.__performanceMeasurements = self.__segmentMeasurements()
        self.__net = None

    def __segmentMeasurements(self):
        radioFrequencyMeasures = []
        performanceMeasures = []
        
        for measurement in self.__configuration["measurements"]:
            name = measurement["measure"]["name"]
            if name in constants.MininetConstants.RADIO_FREQUENCY_MEASURES:
                radioFrequencyMeasures.append(measurement)

            if name in constants.MininetConstants.PERFORMANCE_MEASURES:
                performanceMeasures.append(measurement)

        return radioFrequencyMeasures, performanceMeasures

    def __loadConfiguration(self):
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
        self.__topology()
        self.__analyse()

    def __topology(self):
        info("*** Creating nodes\n")
        self.__net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference, noise_th=-91, fading_cof=3)
        ap1 = self.__net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36', position='15,30,0')
        self.__net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', min_x=10, max_x=30, min_y=50, max_y=70, min_v=5, max_v=10)
        self.__net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', min_x=0, max_x=60, min_y=25, max_y=80, min_v=2, max_v=10)
        self.__net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8', min_x=60, max_x=70, min_y=10, max_y=20, min_v=1, max_v=5)
        c1 = self.__net.addController('c1')

        info("*** Configuring Propagation Model\n")
        self.__net.setPropagationModel(model="logDistance", exp=4)

        info("*** Configuring wifi nodes\n")
        self.__net.configureWifiNodes()
        #nodes = self.__net.stations
        self.__net.setMobilityModel(time=0, model='RandomDirection',max_x=90, max_y=90, seed=20)
        
        info("*** Starting network\n")
        self.__net.build()
        c1.start()
        ap1.start([c1])

    def __analyse(self):
        nodes = { "station": self.__net.stations, "accessPoint": self.__net.aps }
        positionMeasurer = meas.PositionMeasurer(self.__start, nodes)
        radioFrequencyMeasurer = meas.RadioFrequencyMeasurer(self.__start, self.__net.stations, self.__radioFrequencyMeasurements)
        performanceMeasurer = meas.PerformanceMeasurer(self.__start, self.__net, self.__performanceMeasurements)

        measurers = [positionMeasurer, radioFrequencyMeasurer, performanceMeasurer]

        threads = []
        for measurer in measurers:
            t = threading.Thread(target=measurer.run)
            t.daemon = True
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

if __name__ == '__main__':
    setLogLevel('info')
    script = MininetScript()
    script.run()