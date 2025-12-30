from django.db import models
from django.conf import settings

class Follow(models.Model):
    """
    Represents a follow relationship between two users.

    Each instance indicates that one user (the follower) is following
    another user (the following).
    """


    # The user who initiates the follow
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "following_relations"
    )

    # The user who is being followed
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name= "follower_relations"
    )

    # Timestamp automatically set when the follow relationship is created
    created_at = models.DateTimeField(auto_now_add = True)

    
    def get_followers(user):
        """
        Returns all users who are following the given user.

        Note: This method queries the Follow model to find all follow
        relationships where the given user is the 'following'.
        """
        return user.objects.filter(
            id__in=Follow.objects.filter(following=user).values('follower_id')
        )

    def get_following(user):
        """
        Returns all users that the given user is following.

        Note: This method queries the Follow model to find all follow
        relationships where the given user is the 'follower'.
        """
        return user.objects.filter(
            id__in=Follow.objects.filter(follower=user).values('following_id')
        )


    class Meta:
        """
        Ensures that a user cannot follow the same user more than once.
        """
        unique_together = ("follower", "following")

    def __str__(self):
        """
        Human-readable representation of the follow relationship,
        useful for admin display and debugging.
        """
        return f"{self.follower.username} follows {self.following.username}"