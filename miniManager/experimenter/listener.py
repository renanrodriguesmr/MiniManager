from asyncio import run
from mininetWifiAdapter import IResultEventListener
from .webSocketServer import WebSocketServer
from .experimentsQueue import ExperimentsQueue


class ExperimentListener(IResultEventListener):
    def __init__(self, roundID):
        self.__roundID = roundID

    def update(self, subject):
        run(self.__sendMessage(subject))

        if subject["type"] == "UPDATE":
            queue = ExperimentsQueue.instance()
            queue.enable()

    async def __sendMessage(self, subject):
        await WebSocketServer.sendMessageToRoom(self.__roundID, subject)