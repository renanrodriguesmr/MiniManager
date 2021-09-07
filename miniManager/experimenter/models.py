from django.db import models
from django.utils.timezone import now

class Round(models.Model):
    name = models.CharField(max_length=50)
    start = models.DateTimeField(default=now)
    end = models.DateTimeField(default=None,blank=True, null=True)

    class Meta:
        db_table = "Round"
