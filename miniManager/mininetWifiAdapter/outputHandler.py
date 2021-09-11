from threading import Thread
import json

class OutputHandler:
    def __init__(self, content, notifier):
        self.notifier = notifier
        self.content = content

    def process(self):
        pass

    def generateNotification(self, message):
        thread = Thread(target=self.notifier.notify, args=(message,))
        thread.daemon = True
        thread.start()

    def formattedContent(self):
        self.content = self.content.decode('utf-8').replace("\'", "\"")


class PartialResultHandler(OutputHandler):
    def __init__(self, content, notifier):
      super().__init__(content, notifier)
      self.formattedContent()

    def process(self):
        partialResult = []

        results = self.content.split("\n")
        for result in results:
            resultObj = json.loads(result)
            partialResult.extend(resultObj["partialResult"])

        self.notifier.notify({"type": "UPDATE", "value": partialResult})

class ErrorHandler(OutputHandler):
    def __init__(self, content, notifier):
      super().__init__(content, notifier)
      self.formattedContent()

    def process(self):
        resultObj = json.loads(self.content)
        print(resultObj)

        self.notifier.notify({"type": "ERROR", "value": resultObj})