import threading
from queue import Queue
import time
from provenanceCatcher import ProvenanceManager
from .models import Round

class ExperimentsQueue:

    _instance = None
    POLLING_PERIOD = 5

    def __init__(self):
        self.queue = Queue()
        self._currentExperiment = None
        self.__busy = False

        t = threading.Thread(target=self._consume)
        t.daemon = True
        t.start()


    def add(self, mininetWifiExp, roundID, medicao_schema):
        self.queue.put({ "experiment": mininetWifiExp, "round": roundID, "medicao_schema": medicao_schema })

    def getCurrentExperiment(self):
        return self._currentExperiment

    def enable(self):
        self.__busy = False

    def _consume(self):
        while True:
            time.sleep(self.POLLING_PERIOD)
            if self.__busy:
                continue

            if self.queue.empty():
                self._currentExperiment = None
                continue

            self.__busy = True
            element = self.queue.get()
            roundID = element["round"]
            self.__updateRoundStatus(roundID)
            self.__startCapture(roundID, element["medicao_schema"])
            self._currentExperiment = element["experiment"]
            self._currentExperiment.run()

    def __updateRoundStatus(self, roundID):
        round = Round.objects.get(id=roundID)
        round.setToNextStatus()
        round.save()

    def __startCapture(self, roundID, schema):
        provenanceCatcher = ProvenanceManager.instance()
        provenanceCatcher.reset(roundID, schema)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance