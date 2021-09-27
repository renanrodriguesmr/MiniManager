from django.db import models

# Create your models here.

class TestPlan(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "TestPlan"


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










