from django.db import models
from django.utils.timezone import now

class Round(models.Model):
    name = models.CharField(max_length=50)
    start = models.DateTimeField(default=now)
    end = models.DateTimeField(default=None,blank=True, null=True)
    status = models.CharField(max_length=50, default="STARTING")  #STARTING, IN_PROGRESS, DONE

    STARTING = "STARTING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    class Meta:
        db_table = "Round"
