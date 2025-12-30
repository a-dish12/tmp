from django.db import models
from django.conf import settings

class PlannedDay(models.Model):
    """
    Represents a single calendar day for which a user has planned meals.

    Each PlannedDay belongs to one user and one specific date,
    acting as a container for all meals planned on that day.
    """
    # The user who owns this planned day
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name="planned_days")
    # The calendar date this planning entry refers to
    date = models.DateField()

    class Meta:
        """
        Ensures that each user can only have one PlannedDay
        per calendar date.
        """
        unique_together = ("user", "date")

    def __str__(self):
        """
        Human-readable representation of the planned day,
        useful for admin views and debugging.
        """
        return f"{self.user.username} - {self.date}"


