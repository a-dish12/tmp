from django.db import models
from django.conf import settings

class PlannedDay(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name="planned_days")
    date = models.DateField()

    class Meta:
        unique_together = ("user", "date")


