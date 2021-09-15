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

    def setToNextStatus(self):
        statusToNextMapping = {
            self.WAITING: self.STARTING,
            self.STARTING: self.IN_PROGRESS,
            self.IN_PROGRESS: self.DONE,
            self.DONE: self.DONE,
        }

        currentStatus = self.status
        if currentStatus == self.IN_PROGRESS:
            self.end = now()
        
        self.status = statusToNextMapping[currentStatus]