class ProvenanceManager:

    __instance = None

    def __init__(self):
        self.__roundID = 0
        self.__resultsBuffer = {}

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def reset(self, roundID):
        self.__roundID = roundID
        self.__resultsBuffer = {}

    def saveResults(self):
        from .models import Result #TODO: fix it
        result = Result(round_id = self.__roundID)
        result.save()