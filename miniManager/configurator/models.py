from django.db import models

# Create your models here.

#PModelCatalog funciona como catálogo de modelos
class PModelCatalog(models.Model): 
    name = models.CharField(max_length=30)
    displayname = models.CharField(max_length=30)

    class Meta:
        db_table = "PModelCatalog"

class PropagationModel(models.Model):
    model = models.ForeignKey(PModelCatalog, on_delete=models.CASCADE)

    class Meta:
        db_table = "PropagationModel"

class Configuration(models.Model):
    medicao_schema = models.TextField()
    propagationmodel = models.ForeignKey(PropagationModel, on_delete=models.CASCADE, null= True)


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





