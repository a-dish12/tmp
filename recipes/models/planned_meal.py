from django.db import models
from django.conf import settings
from recipes.models.planned_day import PlannedDay
from recipes.models.recipes import Recipe

class PlannedMeal(models.Model):
    planned_day = models.ForeignKey(PlannedDay,
                on_delete= models.CASCADE,
                related_name="meals")
    meal_type = models.CharField(max_length=20)
    recipe = models.ForeignKey(Recipe,
                on_delete= models.CASCADE,
                related_name="planned_meals")


    class Meta:
        unique_together = ("planned_day", "meal_type", "recipe")
