from django.db import models

class TestPlan(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null = True)
    author = models.CharField(max_length=50, null = True)

    class Meta:
        db_table = "TestPlan"


class Network(models.Model):
    fixed = models.BooleanField(default=True)
    
    class Meta:
        db_table="Network"

#class NetworkController(models.Model): /vamos usar o Controller do mininet.node
    #protocol = models.CharField(max_length=30)


#PModelCatalog works as a catalog of propagation models
class PModelCatalog(models.Model): 
    name = models.CharField(max_length=30)
    displayname = models.CharField(max_length=30)

    class Meta:
        db_table = "PModelCatalog"

class MModelCatalog(models.Model): 
    name = models.CharField(max_length=30)
    displayname = models.CharField(max_length=30)

    class Meta:
        db_table = "MModelCatalog"

class PropagationModel(models.Model):
    model = models.ForeignKey(PModelCatalog, on_delete=models.CASCADE)

    class Meta:
        db_table = "PropagationModel"


class MobilityModel(models.Model):
    model = models.ForeignKey(MModelCatalog, on_delete=models.CASCADE)

    class Meta:
        db_table = "MobilityModel"

class Configuration(models.Model):
    medicao_schema = models.TextField()
    propagationmodel = models.ForeignKey(PropagationModel, on_delete=models.CASCADE, null= True)
    mobilitymodel = models.ForeignKey(MobilityModel, on_delete = models.CASCADE, null=True)
    stop_time = models.IntegerField(null=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = "Configuration"

    def getMeasurements(self):
        result = []
        measurements = Measurement.objects.filter(config_id = self.id)
        for measurement in measurements:
            result.append({"period": measurement.period, "measure": {"name": measurement.measure.name}})

        return result

    def getPerformanceMeasurements(self):
        result = []
        measurements = PerformanceMeasurement.objects.filter(config_id = self.id)
        for measurement in measurements:
            result.append({"period": measurement.period, "source": measurement.source, "destination": measurement.destination, "measure": {"name": measurement.measure.name}})

        return result

    def getPropagationModel(self):
        propagationmodel = self.propagationmodel
        args = {}
        params = PropagationParam.objects.filter(propagationmodel_id = propagationmodel.id)
        for param in params:
            args[param.name] = param.value

        return {"model": propagationmodel.model.name, "args": args}

    def getMobilityModel(self):
        mobilitymodel = self.mobilitymodel
        args = {}
        params = MobilityParam.objects.filter(mobilitymodel_id = mobilitymodel.id)
        for param in params:
            args[param.name] = param.value

        return {"model": mobilitymodel.model.name, "args": args}

    def getConfigurationObj(self):
        return {
            "radioFrequencyMeasurements": self.getMeasurements(),
            "performanceMeasurements": self.getPerformanceMeasurements(),
            "propagationModel": self.getPropagationModel(),
            "mobilityModel": self.getMobilityModel()
        }

class Measure(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)

    class Meta:
        db_table = "Measures"

class PerformanceMeasure(models.Model):
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=10)

    class Meta:
        db_table = "PerformanceMeasure"

class Measurement(models.Model):
    period = models.IntegerField()
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE)
    config = models.ForeignKey(Configuration, on_delete=models.CASCADE)

    class Meta:
        db_table = "Measurement"

class PerformanceMeasurement(models.Model):
    period = models.IntegerField()
    measure = models.ForeignKey(PerformanceMeasure, on_delete=models.CASCADE)
    config = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)

    class Meta:
        db_table = "PerformanceMeasurement"


class PropagationParam(models.Model):
    name = models.CharField(max_length=30)
    value = models.FloatField()
    propagationmodel = models.ForeignKey(PropagationModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "PropagationParam"

class MobilityParam(models.Model):
    name = models.CharField(max_length=30)
    value = models.FloatField()
    mobilitymodel = models.ForeignKey(MobilityModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "MobilityParam"



class Node(models.Model):
    name = models.CharField(max_length=30)
    mac = models.CharField(max_length=30)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


    class Meta:
        db_table = "Node"

class Mobility(models.Model):
    tempo = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    class Meta:
        db_table = "Mobility"

class Position(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
   
    class Meta:
        db_table = "Position"

class Station(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    class Meta:
        db_table = "Station"

class Host(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    class Meta:
        db_table = "Host"


class Switch(models.Model):
    type = models.CharField(max_length=30)
    node = models.ForeignKey(Node,on_delete=models.CASCADE)
    
    class Meta:
        db_table="Switch"

class AccessPoint(models.Model):
    ssid = models.CharField(max_length=30)
    mode = models.CharField(max_length=30)
    channel = models.CharField(max_length=30)
    node = models.ForeignKey(Node,on_delete=models.CASCADE)

    class Meta:
        db_table = "AccessPoint"

class Interface(models.Model):
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    node = models.ForeignKey(Node, on_delete=models.CASCADE) 

    class Meta:
        db_table = "Interface"

class Link(models.Model):
    int1 = models.ForeignKey(Interface, related_name='int1', on_delete=models.CASCADE, null=True)
    int2 = models.ForeignKey(Interface, related_name='int2', on_delete=models.CASCADE, null=True)
    connection = models.CharField(max_length=30)
    delay = models.CharField(max_length=30)
    loss = models.CharField(max_length=30)
    maxqueue = models.CharField(max_length=30)
    jitter = models.CharField(max_length=30)
    speedup = models.CharField(max_length=30)

    class Meta:
        db_table="Link"

class Version(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    test_plan = models.ForeignKey(TestPlan, models.CASCADE, blank=True, null=True, unique=False)
    configuration = models.OneToOneField(Configuration, models.CASCADE, unique=True, blank=True, null=True)

    class Meta:
        db_table = "Version"


