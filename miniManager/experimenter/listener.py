from asyncio import run
from mininetWifiAdapter import IResultEventListener
from .webSocketServer import WebSocketServer
from .experimentsQueue import ExperimentsQueue
from .models import Round


class ExperimentListener(IResultEventListener):
    def __init__(self, roundID):
        self.__roundID = roundID
        self.__started = False

    def update(self, subject):
        run(self.__sendMessage(subject))

        if subject["type"] == "UPDATE" and self.__started == False:
            ExperimentsQueue.instance().enable()
            self.__started = True
            self.__updateStatus()

        if subject["type"] == "FINISH":
            self.__updateStatus()

    def __updateStatus(self):
        round = Round.objects.get(id=self.__roundID)
        round.setToNextStatus()
        round.save()


    async def __sendMessage(self, subject):
        await WebSocketServer.sendMessageToRoom(self.__roundID, subject)