from mininetWifiAdapter import IResultEventListener
from .webSocketServer import WebSocketServer

class ExperimentListener(IResultEventListener):
    async def update(self, subject):
        await WebSocketServer.sendMessageToRoom("1", subject)