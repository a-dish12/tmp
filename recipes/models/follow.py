from django.db import models
from django.conf import settings

class Follow(models.Model):
    
    # user who follows
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "following_relations"
    )

    # user being followed
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name= "follower_relations"
    )

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"