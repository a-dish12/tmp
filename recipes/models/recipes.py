from django.db import models
from django.conf import settings
class Recipe(models.Model):
    author= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title=models.CharField(max_length=100,blank=False)
    description=models.TextField(blank=False)
    ingredients=models.TextField(blank=False)
    time=models.PositiveIntegerField(help_text="preparation time in minutes")
    meal_type=models.TextField(help_text="breakfast/lunch/dinner",blank=False,default="")

    class Meta:
        ordering=["time"]

        def __str__(self):
            return f"Recipe: {self.title} by {self.author}"
        

