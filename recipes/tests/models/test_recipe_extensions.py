"""Unit tests for Recipe model with instructions and image fields."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import User, Recipe


class RecipeInstructionsAndImageTestCase(TestCase):
    """Unit tests for Recipe instructions and image fields."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="lunch"
        )

    def test_recipe_without_instructions_is_valid(self):
        """Test that instructions field is optional."""
        self.recipe.instructions = ""
        self._assert_recipe_is_valid()

    def test_recipe_with_instructions_is_valid(self):
        """Test that recipe can have instructions."""
        self.recipe.instructions = "1. Step one\n2. Step two\n3. Step three"
        self._assert_recipe_is_valid()

    def test_recipe_instructions_can_be_long(self):
        """Test that instructions can be lengthy."""
        self.recipe.instructions = "Step " * 200
        self._assert_recipe_is_valid()

    def test_recipe_without_image_is_valid(self):
        """Test that image fields are optional."""
        self.recipe.image = None
        self.recipe.image_url = None
        self._assert_recipe_is_valid()

    def test_recipe_with_image_url_is_valid(self):
        """Test that recipe can have an image URL."""
        self.recipe.image_url = "https://example.com/image.jpg"
        self._assert_recipe_is_valid()

    def test_recipe_image_url_must_be_valid_url(self):
        """Test that image_url must be a valid URL."""
        self.recipe.image_url = "not a valid url"
        self._assert_recipe_is_invalid()

    def test_get_image_url_returns_image_url_when_no_upload(self):
        """Test that get_image_url returns URL when no image uploaded."""
        self.recipe.image_url = "https://example.com/image.jpg"
        self.recipe.image = None
        self.assertEqual(self.recipe.get_image_url(), "https://example.com/image.jpg")

    def test_get_image_url_returns_none_when_no_image(self):
        """Test that get_image_url returns None when no image provided."""
        self.recipe.image = None
        self.recipe.image_url = None
        self.assertIsNone(self.recipe.get_image_url())

    def _assert_recipe_is_valid(self):
        try:
            self.recipe.full_clean()
        except ValidationError:
            self.fail('Test recipe should be valid')

    def _assert_recipe_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
