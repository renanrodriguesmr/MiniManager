from django.db import connection, models

# Create your models here.

class TestPlan(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "TestPlan"


class Network(models.Model):
    fixed = models.BooleanField()
    
    class Meta:
        db_table="Network"

#class NetworkController(models.Model): /vamos usar o Controller do mininet.node
    #protocol = models.CharField(max_length=30)


class Version(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    test_plan = models.ForeignKey(TestPlan, models.CASCADE, blank=True, null=True, unique=False)

    class Meta:
        db_table = "Version"

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



class Measure(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)

    class Meta:
        db_table = "Measures"


class Measurement(models.Model):
    period = models.IntegerField()
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE)
    config = models.ForeignKey(Configuration, on_delete=models.CASCADE)

    class Meta:
        db_table = "Measurement"


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
    fixed = models.BooleanField()
    mac = models.CharField(max_length=30)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


    class Meta:
        db_table = "Node"

class Mobility(models.Model):
    tempo = models.FloatField()
    fixed = models.BooleanField()
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
    fixed = models.BooleanField()
    ip = models.CharField(max_length=30)
    node = models.ForeignKey(Node, on_delete=models.CASCADE) 

    class Meta:
        db_table = "Interface"

class Link(models.Model):
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    connection = models.CharField(max_length=30)
    fixed = models.BooleanField()
    delay = models.CharField(max_length=30)
    loss = models.CharField(max_length=30)
    max_queue_size = models.CharField(max_length=30)
    jitter = models.CharField(max_length=30)
    speedup = models.CharField(max_length=30)

    class Meta:
        db_table="Link"





