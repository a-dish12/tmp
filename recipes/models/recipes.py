from django.db import models
from django.conf import settings
from django.db.models import Avg


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    ingredients = models.TextField(blank=False)
    time = models.PositiveIntegerField(help_text="preparation time in minutes")
    meal_type = models.TextField(help_text="breakfast/lunch/dinner", blank=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["time"]

    def __str__(self):
        return f"Recipe: {self.title} by {self.author}"
    
    def average_rating(self):
        """Calculate average rating for this recipe."""
        result = self.ratings.aggregate(Avg('stars'))
        return result['stars__avg'] or 0

    def rating_count(self):
        """Count total number of ratings."""
        return self.ratings.count()
    
    def user_can_rate(self, user):
        """Check if a user can rate this recipe."""
        if not user.is_authenticated:
            return False
        if self.author == user:
            return False
        return True
    
    def get_user_rating(self, user=None):
        """
        Get the rating this user gave (if any).
        Can be called from template without passing user explicitly.
        """
        if user is None:
            # If called from template without args, return None
            # View should pass user explicitly
            return None
        if not user.is_authenticated:
            return None
        try:
            return self.ratings.get(user=user).stars
        except:
            return None
