class ProvenanceService():
    def getResultContentFromRound(self, roundID, schema):
        from .models import Result
        result = Result.objects.get(round__pk=roundID)
        return result.xml_content
