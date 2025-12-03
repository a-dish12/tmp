from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
    )

    friends = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True,
    )


    def follow(self, other_user):
        other_user.followers.add(self)

    def unfollow(self, other_user):
        other_user.followers.remove(self)

    def is_following(self, other_user):
        return other_user.followers.filter(pk=self.pk).exists()

    def is_followed_by(self, other_user):
        return self.followers.filter(pk=other_user.pk).exists()
    
    def befriend(self, other_user):
        self.friends.add(other_user)

    def unfriend(self, other_user):
        self.friends.remove(other_user)

    def is_friends_with(self, other_user):
        return self.friends.filter(pk=other_user.pk).exists()

    

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)