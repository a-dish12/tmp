"""
Unit tests for the RecipeForm.

These tests cover:
- Basic form validation
- Dynamic ingredient and instruction fields
- Meal type handling
- Image and image_url fields
- clean() and save() logic
"""

from django.test import TestCase
from recipes.forms.recipe_form import RecipeForm
from recipes.models import User, Recipe


class RecipeFormTestCase(TestCase):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

        self.valid_data = {
            'title': 'Test Recipe',
            'description': 'A test recipe',
            'ingredient_count': 3,
            'ingredient_0': '2 cups flour',
            'ingredient_1': '1 cup sugar',
            'ingredient_2': '3 eggs',
            'instruction_count': 2,
            'instruction_0': 'Mix ingredients',
            'instruction_1': 'Bake at 350°F',
            'time': 30,
            'meal_types': ['lunch'],
            'image_url': 'https://example.com/image.jpg'
        }

    # ---------- Helpers ----------

    def _save_recipe(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        return recipe

    # ---------- Basic validation ----------

    def test_valid_recipe_form(self):
        form = RecipeForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_has_core_fields(self):
        form = RecipeForm()
        for field in [
            'title', 'description', 'time',
            'meal_types', 'ingredient_count', 'instruction_count'
        ]:
            self.assertIn(field, form.fields)

    # ---------- Meal types ----------

    def test_form_accepts_multiple_meal_types(self):
        data = self.valid_data | {'meal_types': ['breakfast', 'lunch']}
        form = RecipeForm(data=data)
        self.assertTrue(form.is_valid())
        recipe = self._save_recipe(form)
        self.assertEqual(recipe.meal_type, 'breakfast,lunch')

    # ---------- Ingredients ----------

    def test_form_accepts_multiple_ingredients(self):
        form = RecipeForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        recipe = self._save_recipe(form)
        self.assertEqual(
            recipe.get_ingredients_list(),
            ['2 cups flour', '1 cup sugar', '3 eggs']
        )

    def test_form_accepts_single_ingredient(self):
        data = self.valid_data | {
            'ingredient_count': 1,
            'ingredient_0': 'Flour'
        }
        form = RecipeForm(data=data)
        self.assertTrue(form.is_valid())
        recipe = self._save_recipe(form)
        self.assertEqual(recipe.get_ingredients_list(), ['Flour'])

    def test_form_rejects_all_empty_ingredients(self):
        data = self.valid_data | {
            'ingredient_0': '',
            'ingredient_1': '',
            'ingredient_2': ''
        }
        form = RecipeForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('ingredient_0', form.errors)

    def test_form_skips_empty_ingredient_fields(self):
        data = self.valid_data | {'ingredient_1': ''}
        form = RecipeForm(data=data)
        self.assertTrue(form.is_valid())
        recipe = self._save_recipe(form)
        self.assertEqual(len(recipe.get_ingredients_list()), 2)

    # ---------- Instructions ----------

    def test_form_accepts_multiple_instructions(self):
        form = RecipeForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        recipe = self._save_recipe(form)
        self.assertEqual(
            recipe.get_instructions_list(),
            ['Mix ingredients', 'Bake at 350°F']
        )

    def test_form_rejects_all_empty_instructions(self):
        data = self.valid_data | {
            'instruction_0': '',
            'instruction_1': ''
        }
        form = RecipeForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('instruction_0', form.errors)

    def test_form_accepts_long_instructions(self):
        data = self.valid_data | {'instruction_0': 'Step ' * 200}
        form = RecipeForm(data=data)
        self.assertTrue(form.is_valid())

    # ---------- Dynamic fields from instance ----------

    def test_form_creates_dynamic_fields_from_existing_recipe(self):
        recipe = Recipe.objects.create(
            author=self.user,
            title='Existing Recipe',
            description='Test',
            ingredients='Flour\nSugar',
            instructions='Mix\nBake',
            time=30,
            meal_type='lunch'
        )
        form = RecipeForm(instance=recipe)

        self.assertIn('ingredient_0', form.fields)
        self.assertIn('ingredient_1', form.fields)
        self.assertEqual(form.fields['ingredient_0'].initial, 'Flour')
        self.assertEqual(form.fields['ingredient_1'].initial, 'Sugar')

        self.assertIn('instruction_0', form.fields)
        self.assertIn('instruction_1', form.fields)
        self.assertEqual(form.fields['instruction_0'].initial, 'Mix')
        self.assertEqual(form.fields['instruction_1'].initial, 'Bake')

    def test_form_initializes_single_fields_for_new_recipe(self):
        form = RecipeForm()
        self.assertEqual(form.fields['ingredient_count'].initial, 1)
        self.assertEqual(form.fields['instruction_count'].initial, 1)
        self.assertIn('ingredient_0', form.fields)
        self.assertIn('instruction_0', form.fields)

    # ---------- Image fields ----------

    def test_form_has_image_fields(self):
        form = RecipeForm()
        self.assertIn('image', form.fields)
        self.assertIn('image_url', form.fields)

    def test_form_accepts_valid_image_url(self):
        form = RecipeForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_accepts_empty_image_url(self):
        data = self.valid_data | {'image_url': ''}
        form = RecipeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_rejects_invalid_image_url(self):
        data = self.valid_data | {'image_url': 'not a url'}
        form = RecipeForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_saves_image_url(self):
        form = RecipeForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        recipe = self._save_recipe(form)
        self.assertEqual(recipe.image_url, self.valid_data['image_url'])
