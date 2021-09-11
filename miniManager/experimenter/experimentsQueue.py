import threading
from queue import Queue
import time

class ExperimentsQueue:

    _instance = None
    POLLING_PERIOD = 2

    def __init__(self):
        self.queue = Queue()
        self._currentExperiment = None

        t = threading.Thread(target=self._consume)
        t.daemon = True
        t.start()


    def add(self, mininetWifiExp):
        self.queue.put(mininetWifiExp)

    def getCurrentExperiment(self):
        return self._currentExperiment


    def _consume(self):
        while True:
            if self.queue.empty():
                self._currentExperiment = None
                time.sleep(self.POLLING_PERIOD)
                continue

            self._currentExperiment = self.queue.get()
            self._currentExperiment.run()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance