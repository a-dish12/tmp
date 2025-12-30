from django.db import models
from django.conf import settings
from recipes.models.planned_day import PlannedDay
from recipes.models.recipes import Recipe

class PlannedMeal(models.Model):
    """
    Represents a single planned meal on a specific day.

    This model links a recipe to a particular day and meal type
    (e.g. breakfast, lunch, dinner, snack) within the meal planner.
    """

    # The day on which this meal is planned
    planned_day = models.ForeignKey(PlannedDay,
                on_delete= models.CASCADE,
                related_name="meals")
    
    # The type of meal (e.g. breakfast, lunch, dinner, snack)
    meal_type = models.CharField(max_length=20)

    # The recipe assigned to this meal slot
    recipe = models.ForeignKey(Recipe,
                on_delete= models.CASCADE,
                related_name="planned_meals")

    class Meta:
        """
        Prevents the same recipe from being added multiple times
        to the same meal type on the same day.
        """
        unique_together = ("planned_day", "meal_type", "recipe")

    def __str__(self):
        """
        Human-readable representation of the planned meal,
        useful for admin views and debugging.
        """
        return f"{self.meal_type.title()} - {self.recipe.title}"
