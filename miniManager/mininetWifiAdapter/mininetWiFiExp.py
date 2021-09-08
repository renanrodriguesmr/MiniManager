from pexpect import popen_spawn
from signal import SIGCHLD
from subprocess import run
import json
import threading
import time
import jsonpickle
class MininetWifiExp():
    RUN_CMD = 'sudo python mininetWifiAdapter/MininetScript.py'
    CLEAR_CMD= 'sudo mn -c'
    EXPERIMENT_TIMEOUT = 125


    def __init__(self, notifier, configuration):
        self.__notifier = notifier
        self.__active = False
        self.__process = None
        self.__start = 0
        self._configuration = configuration

    def run(self):
        self.__serializeConfiguration()
        self.__active = True
        self.__process = popen_spawn.PopenSpawn(self.RUN_CMD)
        self.__start = time.time()
        
        while self.__shouldKeepRunning():
            try:
                self.__process.expect(r'(\{\'partialResult\':\s+\[.*\]\})')
            except:
                continue

            if self.__process is None:
                break
            partialResultsB = self.__process.match.groups()[0]
            self.__processPartialResult(partialResultsB)

        self.finish()

    def __serializeConfiguration(self):
        with open('mininetWifiAdapter/config.json', 'w') as outfile:
            jsonString = jsonpickle.encode(self._configuration)
            json.dump(jsonString, outfile)
            outfile.close()

    def __processPartialResult(self, partialResultsB):
        resultsString = partialResultsB.decode('utf-8').replace("\'", "\"")
        results = resultsString.split("\n")

        partialResult = []
        for result in results:
            resultObj = json.loads(result)
            partialResult.extend(resultObj["partialResult"])

        t = threading.Thread(target=self.__notifier.notify, args=(partialResult,))
        t.daemon = True
        t.start()

    def __shouldKeepRunning(self):
        if not self.__active:
            return False

        currentTime = time.time()
        duration = currentTime - self.__start
        return duration < self.EXPERIMENT_TIMEOUT

    def finish(self):
        self.__active = False
        self.__start = 0

        if self.__process:
            self.__process.stdout.close()
            self.__process.kill(SIGCHLD)
            self.__process = None
        
        run(self.CLEAR_CMD, shell=True)