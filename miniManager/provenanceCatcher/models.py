from django.db import models
from experimenter.models import Round

class Result(models.Model):
    xml_content = models.CharField(max_length=50, blank=True, null=True)
    round = models.OneToOneField(Round, models.CASCADE, unique=True)
    class Meta:
        db_table = "Result"