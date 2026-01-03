from django.conf import settings
from django.db import models

class FollowRequest(models.Model):
    # for private accounts - user must approve before following
    # The user who is sending the follow request
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_follow_requests',
        on_delete=models.CASCADE,
    )
    # The user who is receiving the follow request
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_follow_requests',
        on_delete=models.CASCADE,
    )
    # Timestamp automatically set when the follow request is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"
