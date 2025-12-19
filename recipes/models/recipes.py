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
    instructions = models.TextField(blank=True, help_text="Step-by-step cooking instructions")
    time = models.PositiveIntegerField(help_text="preparation time in minutes")
    meal_type = models.TextField(help_text="breakfast/lunch/dinner", blank=False, default="")
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True, help_text="Upload an image from your device")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Or provide an image URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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