from django.db import models

# Create your models here.


class Configuration(models.Model):
    medicao_schema = models.TextField()



class Measure(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)


class Measurement(models.Model):
    period = models.IntegerField()
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE)
    config = models.ForeignKey(Configuration, on_delete=models.CASCADE)





