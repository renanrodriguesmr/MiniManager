class ProvenanceService():
    def getResultContentFromRound(self, roundID, schema):
        from .models import Result
        resultDict = []
        try:
            result = Result.objects.get(round__pk=roundID)
            resultDict = schema.decode(result.xml_content, attr_prefix='')
            return resultDict["radioFrequency"]["instant"], resultDict["performance"]["instance"]

        except:
            resultDict = []

        return resultDict

    def getXML(self, roundID):
        from .models import Result
        result = Result.objects.get(round__pk=roundID)
        enc = '<?xml version="1.0" encoding="utf-8"?>'
        return enc + result.xml_content
