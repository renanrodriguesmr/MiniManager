from django.db import models

# Create your models here.


class Configuration(models.Model):
    medicao_schema = models.TextField()

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





