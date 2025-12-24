"""Unit tests for the RecipeForm with instructions and image fields."""
from django.test import TestCase
from recipes.forms.recipe_form import RecipeForm
from recipes.models import User


class RecipeFormExtensionsTestCase(TestCase):
    """Unit tests for RecipeForm with new fields."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        
        self.form_input = {
            'title': 'Test Recipe',
            'description': 'A test recipe',
            'ingredient_count': 1,
            'ingredient_0': 'Test ingredients',
            'instruction_count': 2,
            'instruction_0': 'Step one',
            'instruction_1': 'Step two',
            'time': 30,
            'meal_types': ['lunch'],
            'image_url': 'https://example.com/image.jpg'
        }

    def test_form_has_instruction_count_field(self):
        form = RecipeForm()
        self.assertIn('instruction_count', form.fields)

    def test_form_has_image_field(self):
        form = RecipeForm()
        self.assertIn('image', form.fields)

    def test_form_has_image_url_field(self):
        form = RecipeForm()
        self.assertIn('image_url', form.fields)

    def test_valid_form_with_instructions(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_empty_instruction_fields(self):
        self.form_input['instruction_0'] = ''
        self.form_input['instruction_1'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())  # Should reject all empty instructions

    def test_form_accepts_long_instructions(self):
        self.form_input['instruction_0'] = 'Step ' * 200
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_empty_image_url(self):
        self.form_input['image_url'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_valid_image_url(self):
        self.form_input['image_url'] = 'https://example.com/recipe.png'
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_invalid_image_url(self):
        self.form_input['image_url'] = 'not a url'
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_saves_instructions(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        instructions = recipe.get_instructions_list()
        self.assertIn('Step one', instructions)
        self.assertIn('Step two', instructions)

    def test_form_saves_image_url(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        self.assertEqual(recipe.image_url, self.form_input['image_url'])
