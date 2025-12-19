"""Tests for recipe detail view with instructions and images."""
from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe


class RecipeDetailInstructionsAndImageTestCase(TestCase):
    """Tests for recipe detail view displaying instructions and images."""

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
            instructions="1. Step one\n2. Step two\n3. Step three",
            time=30,
            meal_type="lunch",
            image_url="https://example.com/image.jpg"
        )
        
        self.url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_recipe_detail_shows_instructions(self):
        """Test that recipe detail page displays instructions."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Instructions')
        self.assertContains(response, '1. Step one')
        self.assertContains(response, '2. Step two')

    def test_recipe_detail_hides_instructions_when_empty(self):
        """Test that instructions section is hidden when recipe has no instructions."""
        recipe_without_instructions = Recipe.objects.create(
            author=self.user,
            title="Recipe Without Instructions",
            description="No instructions",
            ingredients="Ingredients",
            time=20,
            meal_type="dinner"
        )
        
        url = reverse('recipe_detail', kwargs={'pk': recipe_without_instructions.pk})
        response = self.client.get(url)
        
        # Should not show instructions heading
        self.assertNotContains(response, '<h5 class="card-title mt-4">Instructions</h5>')

    def test_recipe_detail_shows_image_url(self):
        """Test that recipe detail page displays image from URL."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'https://example.com/image.jpg')
        self.assertContains(response, '<img')

    def test_recipe_detail_hides_image_when_not_provided(self):
        """Test that image section is hidden when recipe has no image."""
        recipe_without_image = Recipe.objects.create(
            author=self.user,
            title="Recipe Without Image",
            description="No image",
            ingredients="Ingredients",
            time=15,
            meal_type="snack"
        )
        
        url = reverse('recipe_detail', kwargs={'pk': recipe_without_image.pk})
        response = self.client.get(url)
        
        # Check that no img tag is displayed for this recipe
        content = response.content.decode()
        self.assertNotIn('<img src=', content)

    def test_recipe_detail_shows_all_fields(self):
        """Test that recipe detail shows all recipe information including new fields."""
        response = self.client.get(self.url)
        
        self.assertContains(response, self.recipe.title)
        self.assertContains(response, self.recipe.description)
        self.assertContains(response, self.recipe.ingredients)
        self.assertContains(response, self.recipe.instructions)
        self.assertContains(response, str(self.recipe.time))
        self.assertContains(response, self.recipe.meal_type.capitalize())
        self.assertContains(response, self.recipe.image_url)
