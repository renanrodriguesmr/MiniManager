from abc import ABC, abstractmethod
import time
import math

import constants
import threading

class IMeasurer(ABC):
    @abstractmethod
    def run(self):
        pass

class PositionMeasurer(IMeasurer):
    def __init__(self, start, nodes):
        self.__start = start
        self.__nodes = nodes

    def run(self):
        while True:
            time.sleep(constants.MininetConstants.DELAY)
            currentTime = math.floor(time.time() - self.__start)

            positions = {}
            for key in self.__nodes:
                for node in self.__nodes[key]:
                    name = getattr(node.wintfs[0],"name")
                    positions[name] = {"type": key, "position": list(node.position)}

            print({
                constants.MininetConstants.TIME_KEY: currentTime,
                constants.MininetConstants.POSITIONS_KEY: positions
            })

class RadioFrequencyMeasurer(IMeasurer):
    def __init__(self, start, stations, measurements):
        self.__start = start
        self.__stations = stations
        self.__measurements = measurements

    def run(self):
        while True:
            time.sleep(constants.MininetConstants.DELAY)
            currentTime = math.floor(time.time() - self.__start)

            measures = self.__getValidMeasures(currentTime)
            if measures == []:
                continue

            radioFrequency = []
            for eachNode in self.__stations:
                measObj = {}
                measObj["time"] = currentTime

                for measure in measures:
                    measureName = measure['name']
                    measObj[measureName] = self.__getMetricFromNode(measureName, eachNode)

                radioFrequency.append(measObj)

            print({
                constants.MininetConstants.TIME_KEY: currentTime,
                constants.MininetConstants.RADIO_FREQUENCY_KEY: radioFrequency
            })

    def __getValidMeasures(self, currentTime):
        radioFrequencyMeasures = []
        for measurement in self.__measurements:
            if (currentTime % measurement["period"]) == 0:
                measure = measurement["measure"]
                radioFrequencyMeasures.append(measure)
        
        if len(radioFrequencyMeasures) != 0:
            radioFrequencyMeasures.append({ "name": "name" })

        return radioFrequencyMeasures

    def __getMetricFromNode(self, measureName, node):
        if measureName == "position":
            return list(node.position)

        
        if measureName == "associatedto":
            if node.wintfs[0].associatedTo:
                return node.wintfs[0].associatedTo.node.wintfs[0].name
            return "None"

        return getattr(node.wintfs[0],measureName)

class PerformanceMeasurer(IMeasurer):
    def __init__(self, start, net, measurements):
        self.__start = start
        self.__net = net
        self.__measurements = measurements

    def run(self):
        threads = []
        for measurement in self.__measurements:
            t = threading.Thread(target=self.__collectMeasurement, args=(measurement,))
            t.daemon = True
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def __collectMeasurement(self, measurement):
        while True:
            result = self.__getMeasure(measurement["measure"])
            currentTime = math.floor(time.time() - self.__start)
            print({
                constants.MininetConstants.TIME_KEY: currentTime,
                constants.MininetConstants.PERFORMANCE_KEY: result
            })
            time.sleep(measurement["period"])

    def __getMeasure(self, measure):
        name = measure["name"]
        sourceName = measure["source"]
        destinationName = measure["destination"]

        value = []
        if name == "ping":
            source = self.__net.get(sourceName)
            destination = self.__net.get(destinationName)
            value = self.__ping(source, destination)

        return {"name": name, "source": sourceName, "destination": destinationName, "value": value}

    def __ping(self, source, destination):
        pingResult = source.cmd('ping', '-c 10 -q', '-I ' + source.wintfs[0].ip, destination.wintfs[0].ip)
        splittedResult = pingResult.split('\r\n')
        return [splittedResult[3], splittedResult[4]]
            
