from pprint import pprint

class ProvenanceService():
    def getResultContentFromRound(self, roundID, schema):
        from .models import Result
        resultDict = []
        try:
            result = Result.objects.get(round__pk=roundID)
            resultDict = schema.decode(result.xml_content, attr_prefix='')
            return resultDict["instant"]

        except:
            resultDict = []

        return resultDict
