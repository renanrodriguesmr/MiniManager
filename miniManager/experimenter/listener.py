from mininetWifiAdapter import IResultEventListener
from .webSocketServer import WebSocketServer
from asyncio import run

class ExperimentListener(IResultEventListener):
    def update(self, subject):
        run(self.__sendMessage(subject))

    async def __sendMessage(self, subject):
        await WebSocketServer.sendMessageToRoom("1", subject)