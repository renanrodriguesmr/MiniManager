def myFunc1(e):
    return int(e[0])

def myFunc2(e):
    return e[1]

def myFunc(e):
    return (int(e[0]), e[1])

class ProvenanceService():
    def getResultContentFromRound(self, roundID, schema):
        from .models import Result
        try:
            result = Result.objects.get(round__pk=roundID)
            resultDict = schema.decode(result.xml_content, attr_prefix='')
            return resultDict["radioFrequency"]["instant"], resultDict["performance"]["instance"]

        except:
            return [], []

        

    def getResultRowsFromRound(self, roundID, schema, radioFrequencyMeasures):
        PERFORMANCE_KEYS = ["time", "source", "destination", "name", "value"]
        radioFrequencyObj, performanceObj = self.getResultContentFromRound(roundID, schema)

        radioFrequency = []
        for resultInstance in radioFrequencyObj:
            for result in resultInstance["station"]:
                row = []
                for measure in radioFrequencyMeasures:
                    value = ""
                    if measure == "time":
                        value = resultInstance["time"]
                    elif measure in result:
                        value = result[measure]

                    row.append(value)
                
                radioFrequency.append(row)
        radioFrequency.sort(key=myFunc)

        
        performance = []
        for resultInstance in performanceObj:
            row = []
            for key in PERFORMANCE_KEYS:
                row.append(resultInstance[key])

            performance.append(row)

        performance.sort(key=myFunc)

        return radioFrequency, performance

    def getXML(self, roundID, encoding = True):
        from .models import Result
        result = Result.objects.get(round__pk=roundID)

        enc = ''
        if encoding:
            enc = '<?xml version="1.0" encoding="utf-8"?>'

        return enc + result.xml_content

    def isGreaterThan(self, e1, e2):
        if myFunc1(e1) == myFunc1(e2):
            return myFunc2(e1) > myFunc2(e2)

        return myFunc1(e1) > myFunc1(e2)

    def isEqual(self, e1, e2):
        if myFunc1(e1) == myFunc1(e2):
            return myFunc2(e1) == myFunc2(e2)

        return False

    def getDiff(self, radioFrequency1, radioFrequency2):
        len1 = len(radioFrequency1)
        len2 = len(radioFrequency2)

        index1 = 0
        index2 = 0

        diff = []
        while index1 < len1 and index2 < len2:
            if radioFrequency1[index1] == radioFrequency2[index2]:
                diff.append({"type": "KEEP", "value": radioFrequency1[index1]})
                index1 = index1 + 1
                index2 = index2 + 1
                continue

            if self.isEqual(radioFrequency1[index1], radioFrequency2[index2]):
                diff.append({"type": "REMOVE", "value": radioFrequency1[index1]})
                diff.append({"type": "ADD", "value": radioFrequency2[index2]})
                index1 = index1 + 1
                index2 = index2 + 1
                continue

            if self.isGreaterThan(radioFrequency1[index1], radioFrequency2[index2]):
                diff.append({"type": "ADD", "value": radioFrequency2[index2]})
                index2 = index2 + 1
                continue

            if self.isGreaterThan(radioFrequency2[index2], radioFrequency1[index1]):
                diff.append({"type": "REMOVE", "value": radioFrequency1[index1]})
                index1 = index1 + 1
                continue

        while index1 < len1:
            diff.append({"type": "REMOVE", "value": radioFrequency1[index1]})
            index1 = index1 + 1

        while index2 < len2:
            diff.append({"type": "ADD", "value": radioFrequency2[index2]})
            index2 = index2 + 1

        return diff



    def diffResults(self, roundID1, roundID2, schema1, schema2, measurements):
        radioFrequency1, performance1 = self.getResultRowsFromRound(roundID1, schema1, measurements)
        radioFrequency2, performance2 = self.getResultRowsFromRound(roundID2, schema2, measurements)

        diff1 = self.getDiff(radioFrequency1, radioFrequency2)
        diff2 = self.getDiff(performance1, performance2)

        return diff1, diff2