from django.test import TestCase
from recipes.forms.recipe_form import RecipeForm

class RecipeCreationFormTests(TestCase):
    def test_valid_recipe_form(self):
        form = RecipeForm(data={
            "title": "Form Recipe",
            "description": "Good food",
            "ingredient_count": 1,
            "ingredient_0": "Flour",
            "instruction_count": 1,
            "instruction_0": "Bake",
            "time": 20,
            "meal_types": ["dinner"]
        })
        self.assertTrue(form.is_valid())