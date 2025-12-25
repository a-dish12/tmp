from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, User


class RecipeDetailDietTypeDisplayTestCase(TestCase):
    """Tests for diet type display on recipe detail page."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = None

    def test_vegan_recipe_shows_diet_badge(self):
        """Test that vegan recipe displays vegan badge."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Vegan Bowl',
            description='Healthy bowl',
            ingredients='quinoa\navocado\ntomato',
            time=20,
            meal_type='lunch'
        )
        self.url = reverse('recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Diet Type:')
        self.assertContains(response, 'Vegan')
        self.assertContains(response, '🌱')

    def test_vegetarian_recipe_shows_diet_badge(self):
        """Test that vegetarian recipe displays vegetarian badge."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Paneer Curry',
            description='Indian curry',
            ingredients='paneer\ntomato\ncream\nspices',
            time=30,
            meal_type='dinner'
        )
        self.url = reverse('recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Diet Type:')
        self.assertContains(response, 'Vegetarian')
        self.assertContains(response, '🥛')

    def test_non_veg_recipe_shows_diet_badge(self):
        """Test that non-vegetarian recipe displays non-veg badge."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Chicken Tikka',
            description='Grilled chicken',
            ingredients='chicken\nyogurt\nspices\nlemon',
            time=40,
            meal_type='dinner'
        )
        self.url = reverse('recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Diet Type:')
        self.assertContains(response, 'Non-Vegetarian')
        self.assertContains(response, '🍖')

    def test_diet_type_visible_when_logged_in(self):
        """Test that diet type is visible when user is logged in."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            description='Test',
            ingredients='pasta\ntomato',
            time=20,
            meal_type='lunch'
        )
        self.client.login(username='@johndoe', password='Password123')
        self.url = reverse('recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Diet Type:')

    def test_diet_type_visible_when_not_logged_in(self):
        """Test that diet type is visible even when not logged in."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            description='Test',
            ingredients='pasta\ntomato',
            time=20,
            meal_type='lunch'
        )
        self.url = reverse('recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Diet Type:')
