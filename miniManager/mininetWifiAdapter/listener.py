from abc import ABC, abstractmethod
from experimenter import ExperimentConsumer
class ResultEventListener(ABC):
    @abstractmethod
    def update(self, subject):
        pass

class WebSocketListener(ResultEventListener):
    async def update(self, subject):
        await ExperimentConsumer.sendUpdate("1", subject)