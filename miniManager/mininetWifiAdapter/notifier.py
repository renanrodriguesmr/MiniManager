import asyncio
from abc import ABC, abstractmethod

class IResultEventListener(ABC):
    @abstractmethod
    def update(self, subject):
        pass
class ResultNotifier():
    _observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, subject):
        for observer in self._observers:
            asyncio.run(observer.update(subject))