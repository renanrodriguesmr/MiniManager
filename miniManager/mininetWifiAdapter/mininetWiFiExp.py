from pexpect import popen_spawn, EOF
from signal import SIGCHLD
import subprocess
import json
import threading
import time
class MininetWifiExp():
    RUN_CMD = 'sudo python3 -u mininetWifiAdapter/MininetScript.py'
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
            if self.__process is None:
                break

            index = self.__process.expect([r'(\{\'partialResult\':\s+\[.*\]\})' , EOF])
            if index == 0:
                partialResultsB = self.__process.after
                self.__processPartialResult(partialResultsB)

        self.finish()

    def __serializeConfiguration(self):
        with open('mininetWifiAdapter/config.json', 'w') as outfile:
            jsonString = json.dumps(self._configuration, default=lambda o: o.__dict__)
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
        
        subprocess.run(self.CLEAR_CMD, shell=True)