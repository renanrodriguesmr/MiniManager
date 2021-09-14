import xml.etree.ElementTree as ET

class ProvenanceManager:

    __instance = None

    def __init__(self):
        self.__roundID = 0
        self.__schema = None
        #self.__resultsBuffer = []
        self.__xml = ET.Element("result")
        self.__xml.set('roundID', str(0))

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def reset(self, roundID, schema):
        self.__roundID = roundID
        #self.__resultsBuffer = []
        self.__xml = ET.Element("result")
        self.__xml.set('roundID', str(roundID))
        self.__schema = schema


    def addResult(self, content):
        #self.__resultsBuffer.append(content)

        instant = ET.Element("instant")
        instant.set('time', str(content["time"]))
        self.__xml.append(instant)

        partialResult = content["partialResult"]
        for row in partialResult:
            station = ET.Element("station")
            station.set('name', row["name"])
            instant.append(station)

            for key in row:
                if key == "time" or key == "name":
                    continue

                element = ET.SubElement(station, key)
                element.text = str(row[key])


    def saveResults(self):
        from .models import Result #TODO: fix it

        tree = ET.ElementTree(self.__xml)
        if not self.__schema.is_valid(tree):
            return

        xml = ET.tostring(tree.getroot()).decode('utf-8')

        result = Result(round_id = self.__roundID, xml_content=xml)
        result.save()