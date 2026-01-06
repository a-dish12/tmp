from django.test import TestCase, Client
from django.core.cache import cache

from recipes.models import User, Recipe

class TrendingRecipesTestCase(TestCase):
    """Test trending recipe features."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123'
        )
        
        self.trending_recipe = Recipe.objects.create(
            author=self.other_user,
            title="Trending Recipe",
            description="Hot right now",
            ingredients="flour",
            time=30,
            meal_type="lunch"
        )
        
        self.normal_recipe = Recipe.objects.create(
            author=self.other_user,
            title="Normal Recipe",
            description="Not trending",
            ingredients="water",
            time=20,
            meal_type="dinner"
        )
        
        cache.clear()

    def tearDown(self):
        """Clear cache."""
        cache.clear()

    def test_recipe_is_trending_with_enough_viewers(self):
        """Test that recipe shows as trending with 3+ viewers."""
        # Add 3 active viewers
        self.trending_recipe.add_viewer(user_id=1)
        self.trending_recipe.add_viewer(user_id=2)
        self.trending_recipe.add_viewer(user_id=3)
        
        self.assertEqual(self.trending_recipe.get_active_viewers(), 3)

    def test_recipe_not_trending_with_few_viewers(self):
        """Test that recipe doesn't show as trending with < 3 viewers."""
        self.normal_recipe.add_viewer(user_id=1)
        self.assertEqual(self.normal_recipe.get_active_viewers(), 1)
        self.assertLess(self.normal_recipe.get_active_viewers(), 3)

    
