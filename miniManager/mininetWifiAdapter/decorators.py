from abc import ABC, abstractmethod

from mininet.node import Controller
from mn_wifi.link import wmediumd
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.log import info

class MininetDecorator(ABC):
    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def getNetwork(self):
        pass

class NetworkDecorator(MininetDecorator):
    def __init__(self):
        self.__network = None

    def getNetwork(self):
        return self.__network

    def configure(self):
        info("*** Creating network\n")
        self.__network = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference, noise_th=-91, fading_cof=3)

        info("*** Creating nodes\n")
        ap1 = self.__network.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36', position='15,30,0')
        self.__network.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', min_x=10, max_x=30, min_y=50, max_y=70, min_v=5, max_v=10)
        self.__network.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', min_x=0, max_x=60, min_y=25, max_y=80, min_v=2, max_v=10)
        self.__network.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8', min_x=60, max_x=70, min_y=10, max_y=20, min_v=1, max_v=5)
        c1 = self.__network.addController('c1')

        info("*** Configuring wifi nodes\n")
        self.__network.configureWifiNodes()


class PropagationModelDecorator(MininetDecorator):
    ARGS_MAP = {
        "exponent": "exp"
    }

    def __init__(self, component, propagationModel):
        self.__network = None
        self.__component = component
        self.__propagationModel = propagationModel
        self.__args = {}
        self.__parseArgs()

    def __parseArgs(self):
        self.__args = {}
        for arg in self.__propagationModel["args"]:
            self.__args[self.ARGS_MAP[arg]] = self.__propagationModel["args"][arg]
    
    def getNetwork(self):
        return self.__network

    def configure(self):
        info("***Setting Propagation Model\n")
        self.__component.configure()
        self.__network = self.__component.getNetwork()
        self.__network.setPropagationModel(model=self.__propagationModel["model"], **self.__args)

class MobilityModelDecorator(MininetDecorator):
    ARGS_MAP = {
        "seed": "seed",
        "min_velocidade": "min_v",
        "max_velocidade": "max_v",
        "min_x": "min_x",
        "max_x": "max_x",
        "min_y": "min_y",
        "max_y": "max_y",
        "min_z": "min_z",
        "max_z": "max_z",
    }

    def __init__(self, component, mobilityModel):
        self.__network = None
        self.__component = component
        self.__mobilityModel = mobilityModel
        
        self.__args = {}
        self.__parseArgs()

    def __parseArgs(self):
        self.__args = {}
        for arg in self.__mobilityModel["args"]:
            value = self.__mobilityModel["args"][arg]
            if arg == "seed":
                value = int(value)

            self.__args[self.ARGS_MAP[arg]] = value
    
    def getNetwork(self):
        return self.__network

    def configure(self):
        info("***Setting Mobility Model\n")
        self.__component.configure()
        self.__network = self.__component.getNetwork()
        self.__network.setMobilityModel(time=0, model=self.__mobilityModel["model"], **self.__args)

class NetworkStarterDecorator(MininetDecorator):
    def __init__(self, component):
        self.__network = None
        self.__component = component
    
    def getNetwork(self):
        return self.__network

    def configure(self):
        self.__component.configure()
        self.__network = self.__component.getNetwork()

        info("*** Starting network\n")
        self.__network.build()
        self.__network.get("c1").start()
        self.__network.get("ap1").start([self.__network.get("c1")])
