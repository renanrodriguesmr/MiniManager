from threading import Thread
import json
from .constants import MininetConstants

class OutputHandler:
    def __init__(self, content, notifier):
        self.notifier = notifier
        self.eventType = "default"
        self.formattedContent(content)

    def process(self):
        self.notifier.notify({"type": self.eventType, "value": self.content})

    def formattedContent(self, content):
        content = content.decode('utf-8').replace("\'", "\"")
        self.content = json.loads(content)


class EOFHandler(OutputHandler):
    def process(self):
        pass

class PartialResultHandler(OutputHandler):
    def __init__(self, content, notifier):
      super().__init__(content, notifier)
      self.eventType = MininetConstants.UPDATE


class ErrorHandler(OutputHandler):
    def __init__(self, content, notifier):
      super().__init__(content, notifier)
      self.eventType = MininetConstants.ERROR