import threading
from queue import Queue
import time

class ExperimentsQueue:

    _instance = None
    POLLINGPERIOD = 2

    def __init__(self):
        self.queue = Queue()

        t = threading.Thread(target=self.consume)
        t.daemon = True
        t.start()


    def add(self, mininetWifiExp):
        self.queue.put(mininetWifiExp)

    def consume(self):
        while True:
            if self.queue.empty():
                time.sleep(self.POLLINGPERIOD)
                continue

            mininetWifiExp = self.queue.get()
            mininetWifiExp.run()


    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance