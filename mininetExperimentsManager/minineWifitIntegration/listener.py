from abc import ABC, abstractmethod

class ResultEventListener(ABC):
    @abstractmethod
    def update(self, subject):
        pass

class WebSocketListener(ResultEventListener):
    def update(self, subject):
        print(subject)