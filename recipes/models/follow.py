from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

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

    User = get_user_model()
    
    def get_followers(user):
        return User.objects.filter(
            id__in=Follow.objects.filter(following=user).values('follower_id')
        )

    def get_following(user):
        return User.objects.filter(
            id__in=Follow.objects.filter(follower=user).values('following_id')
        )


    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"