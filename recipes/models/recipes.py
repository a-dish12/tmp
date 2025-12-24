from django.db import models
from django.conf import settings
from django.db.models import Avg


class Recipe(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('dessert', 'Dessert'),
    ]
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    ingredients = models.TextField(blank=False)
    instructions = models.TextField(blank=True, help_text="Step-by-step cooking instructions")
    time = models.PositiveIntegerField(help_text="preparation time in minutes")
    meal_type = models.TextField(help_text="breakfast/lunch/dinner", blank=False, default="")
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True, help_text="Upload an image from your device")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Or provide an image URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0, help_text="Total number of times this recipe has been viewed")
    last_viewed_at = models.DateTimeField(null=True, blank=True, help_text="Last time this recipe was viewed")
    is_hidden = models.BooleanField(default=False, help_text="Hidden by moderator or auto-hidden due to reports")

    MEAT_KEYWORDS = ["chicken", "mutton", "fish", "lamb", "pork", "beef", "egg", "eggs", "shrimp", "prawns", "bacon"]
    DAIRY_KEYWORDS = ["milk", "cheese", "butter", "ghee", "yogurt", "cream"]
    HONEY_KEYWORDS = ["honey"]

    DIET_NON_VEG = "non_veg"
    DIET_VEG = "veg"
    DIET_VEGAN = "vegan"

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
        
    def get_diet_type(self):
        ingredients = self.ingredients.lower()

        if any(w in ingredients for w in self.MEAT_KEYWORDS):
            return self.DIET_NON_VEG

        if any(w in ingredients for w in self.DAIRY_KEYWORDS + self.HONEY_KEYWORDS):
            return self.DIET_VEG

        return self.DIET_VEGAN
    
    def get_image_url(self):
        """Return image URL, prioritizing uploaded image over URL field."""
        if self.image:
            return self.image.url
        return self.image_url
    
    def get_active_viewers(self):
        """Get count of users currently viewing this recipe."""
        from django.core.cache import cache
        cache_key = f'recipe_viewers_{self.pk}'
        viewers = cache.get(cache_key, set())
        return len(viewers)
    
    def add_viewer(self, user_id):
        """Add a user to active viewers and increment total views."""
        from django.core.cache import cache
        from django.utils import timezone
        
        cache_key = f'recipe_viewers_{self.pk}'
        viewers = cache.get(cache_key, set())
        
        # Only count as new view if user wasn't already viewing
        is_new_viewer = user_id not in viewers
        
        viewers.add(user_id)
        # Keep viewer in cache for 5 minutes (300 seconds)
        cache.set(cache_key, viewers, 300)
        
        if is_new_viewer:
            self.total_views += 1
            self.last_viewed_at = timezone.now()
            self.save(update_fields=['total_views', 'last_viewed_at'])
    
    def get_popularity_score(self):
        """Calculate popularity score based on ratings, views, and recency."""
        avg_rating = self.average_rating() or 0
        rating_weight = avg_rating * self.rating_count()
        view_weight = self.total_views * 0.1
        return rating_weight + view_weight
    
    def get_ingredients_list(self):
        """Return ingredients as a list, split by newlines."""
        if not self.ingredients:
            return []
        return [ing.strip() for ing in self.ingredients.split('\n') if ing.strip()]
    
    def get_instructions_list(self):
        """Return instructions as a list, split by newlines."""
        if not self.instructions:
            return []
        return [inst.strip() for inst in self.instructions.split('\n') if inst.strip()]
    
    def get_meal_types_list(self):
        """Return meal types as a list, split by commas."""
        if not self.meal_type:
            return []
        return [mt.strip() for mt in self.meal_type.split(',') if mt.strip()]
    
    def get_meal_types_display(self):
        """Return formatted meal types for display."""
        meal_types = self.get_meal_types_list()
        if not meal_types:
            return "Not specified"
        # Capitalize each meal type for display
        return ', '.join([mt.capitalize() for mt in meal_types])