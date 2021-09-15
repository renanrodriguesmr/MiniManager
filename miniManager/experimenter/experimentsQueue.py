import threading
from queue import Queue
import time
from provenanceCatcher import ProvenanceManager

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
            self._currentExperiment = element["experiment"]
            self.__startCapture(element["round"], element["medicao_schema"])
            self._currentExperiment.run()

    def __startCapture(self, roundID, schema):
        provenanceCatcher = ProvenanceManager.instance()
        provenanceCatcher.reset(roundID, schema)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance