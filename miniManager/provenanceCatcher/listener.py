from mininetWifiAdapter import IResultEventListener
from .provenanceManager import ProvenanceManager

class ProvenanceListener(IResultEventListener):
    def __init__(self):
        self._manager = ProvenanceManager.instance()


    async def update(self, subject):
        if subject["type"] == "FINISH":
            self._finishCapture()

    
    def _finishCapture(self):
        self._manager._saveResults()