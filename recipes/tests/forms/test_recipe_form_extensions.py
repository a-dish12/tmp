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
            'ingredients': 'Test ingredients',
            'instructions': '1. Step one\n2. Step two',
            'time': 30,
            'meal_type': 'lunch',
            'image_url': 'https://example.com/image.jpg'
        }

    def test_form_has_instructions_field(self):
        form = RecipeForm()
        self.assertIn('instructions', form.fields)

    def test_form_has_image_field(self):
        form = RecipeForm()
        self.assertIn('image', form.fields)

    def test_form_has_image_url_field(self):
        form = RecipeForm()
        self.assertIn('image_url', form.fields)

    def test_valid_form_with_instructions(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_empty_instructions(self):
        self.form_input['instructions'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_long_instructions(self):
        self.form_input['instructions'] = 'Step ' * 200
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
        self.assertEqual(recipe.instructions, self.form_input['instructions'])

    def test_form_saves_image_url(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        self.assertEqual(recipe.image_url, self.form_input['image_url'])
