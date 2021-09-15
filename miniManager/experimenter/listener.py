from asyncio import run
from django.utils.timezone import now
from mininetWifiAdapter import IResultEventListener
from .webSocketServer import WebSocketServer
from .experimentsQueue import ExperimentsQueue
from .models import Round


class ExperimentListener(IResultEventListener):
    def __init__(self, roundID):
        self.__roundID = roundID

    def update(self, subject):
        run(self.__sendMessage(subject))

        if subject["type"] == "UPDATE":
            ExperimentsQueue.instance().enable()

        if subject["type"] == "FINISH":
            round = Round.objects.get(id=self.__roundID)
            round.end = now()
            round.status = Round.DONE
            round.save()

    async def __sendMessage(self, subject):
        await WebSocketServer.sendMessageToRoom(self.__roundID, subject)