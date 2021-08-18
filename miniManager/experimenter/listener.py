from mininetWifiAdapter import IResultEventListener
from .webSocketServer import WebSocketServer

class Listener(IResultEventListener):
    async def update(self, subject):
        await WebSocketServer.sendUpdate("1", subject)