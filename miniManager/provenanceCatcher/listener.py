from mininetWifiAdapter import IResultEventListener
from .provenanceManager import ProvenanceManager

class ProvenanceListener(IResultEventListener):
    def __init__(self):
        self.__manager = ProvenanceManager.instance()

    def update(self, subject):
        if subject["type"] == "FINISH":
            self.__finishCapture()
    
    def __finishCapture(self):
        self.__manager.saveResults()