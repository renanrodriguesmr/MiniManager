from django.db import models

# Create your models here.


class Network(models.Model):
    fix = models.BooleanField()



class Configuration(models.Model):
    medicao_schema = models.TextField()
    network = models.ForeignKey(Network, on_delete=models.CASCADE)

class Measure(models.Model):
    name = models.CharField(max_length=20)

class Measurement(models.Model):
    freq = models.IntegerField()
    fix = models.BooleanField()
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE)
    config = models.ForeignKey(Configuration, on_delete=models.CASCADE)



