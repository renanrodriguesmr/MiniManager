from django.db import models
from django.utils.timezone import now

class Round(models.Model):
    name = models.CharField(max_length=50)
    start = models.DateTimeField(default=now)
    end = models.DateTimeField(default=None,blank=True, null=True)
    status = models.CharField(max_length=50, default="WAITING")  #WAITING, STARTING, IN_PROGRESS, DONE

    WAITING = "WAITING"
    STARTING = "STARTING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    class Meta:
        db_table = "Round"

    def __init__(self, *args, **kwargs):
        super(Round, self).__init__(*args, **kwargs)
        self.old_status = self.status
    
    def save(self, *args, **kwargs):
        if self.status == self.DONE and self.old_status != self.DONE:
            self.end = now()
        super().save(*args, **kwargs)