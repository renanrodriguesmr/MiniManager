from abc import ABC, abstractmethod

from mininet.node import Controller
from mn_wifi.link import wmediumd
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.log import info

class MininetDecoratorComponent(ABC):
    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def getNetwork(self):
        pass

class MininetNetwork(MininetDecoratorComponent):
    def __init__(self, nodes):
        self.__network = None
        self.__nodes = nodes

    def getNetwork(self):
        return self.__network

    def configure(self):
        info("*** Creating network\n")
        self.__network = Mininet_wifi(controller=Controller, noise_th=-91, fading_cof=3)

        nodeTypeToAdder = {
            "station": self.__network.addStation,
            "accesspoint": self.__network.addAccessPoint,
            "host": self.__network.addHost,
            "switch": self.__network.addSwitch
        }

        info("*** Creating nodes\n")
        for node in self.__nodes:
            nodeTypeToAdder[node["type"]](node["name"], **node["args"], **node["interface"]["args"])

        c1 = self.__network.addController('c1')

        info("*** Configuring wifi nodes\n")
        self.__network.configureWifiNodes()

class MininetBaseDecorator(MininetDecoratorComponent):
    def __init__(self, component):
        self.__network = None
        self.__component = component

    def getNetwork(self):
        return self.__network

    def configure(self):
        self.__component.configure()
        self.__network = self.__component.getNetwork()

class PropagationModelDecorator(MininetBaseDecorator):
    ARGS_MAP = {
        "exponent": "exp"
    }

    def __init__(self, component, propagationModel):
        super().__init__(component)
        self.__propagationModel = propagationModel
        self.__args = {}
        self.__parseArgs()

    def __parseArgs(self):
        self.__args = {}
        for arg in self.__propagationModel["args"]:
            self.__args[self.ARGS_MAP[arg]] = self.__propagationModel["args"][arg]

    def configure(self):
        info("***Setting Propagation Model\n")
        super().configure()
        self.getNetwork().setPropagationModel(model=self.__propagationModel["model"], **self.__args)

class MobilityModelDecorator(MininetBaseDecorator):
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
        super().__init__(component)
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

    def configure(self):
        info("***Setting Mobility Model\n")
        super().configure()
        self.getNetwork().setMobilityModel(time=0, model=self.__mobilityModel["model"], **self.__args)

class NetworkStarterDecorator(MininetBaseDecorator):
    def __init__(self, component, links):
        super().__init__(component)
        self.__links = links
    
    def configure(self):
        super().configure()
        info("*** Starting network\n")
        network = self.getNetwork()

        for link in self.__links:
            network.addLink(link["node1"], link["node2"], **link["args"])


        network.build()
        network.get("c1").start()
        network.get("ap1").start([network.get("c1")])
