"""Tests for dashboard sorting and trending features."""
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from recipes.models import Recipe, User, Rating


class DashboardSortingTestCase(TestCase):
    """Test dashboard sorting functionality."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123',
            first_name='Jane',
            last_name='Doe'
        )
        
        # Create recipes with different metrics
        self.popular_recipe = Recipe.objects.create(
            author=self.other_user,
            title="Popular Recipe",
            description="Most popular",
            ingredients="flour, water",
            time=30,
            meal_type="lunch",
            total_views=50
        )
        Rating.objects.create(recipe=self.popular_recipe, user=self.user, stars=5)
        
        self.viewed_recipe = Recipe.objects.create(
            author=self.other_user,
            title="Most Viewed Recipe",
            description="Most viewed",
            ingredients="sugar",
            time=20,
            meal_type="snack",
            total_views=500
        )
        
        self.quick_recipe = Recipe.objects.create(
            author=self.other_user,
            title="Quick Recipe",
            description="Fast to make",
            ingredients="milk",
            time=10,
            meal_type="breakfast",
            total_views=10
        )
        
        self.client.login(username='@johndoe', password='Password123')
        cache.clear()

    def tearDown(self):
        """Clear cache."""
        cache.clear()

    def test_dashboard_default_sort(self):
        """Test dashboard default sort by prep time."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context['recipes'])
        
        # Should be sorted by time (ascending)
        self.assertEqual(recipes[0].time, 10)
        self.assertEqual(recipes[0], self.quick_recipe)

    def test_dashboard_sort_by_most_viewed(self):
        """Test sorting by most viewed."""
        response = self.client.get(reverse('dashboard') + '?sort=most_viewed')
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context['recipes'])
        
        # Should be sorted by total_views (descending)
        self.assertEqual(recipes[0], self.viewed_recipe)
        self.assertEqual(recipes[0].total_views, 500)

    def test_dashboard_sort_by_newest(self):
        """Test sorting by newest first."""
        response = self.client.get(reverse('dashboard') + '?sort=newest')
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context['recipes'])
        
        # Most recently created should be first
        self.assertEqual(recipes[0], self.quick_recipe)

    def test_dashboard_sort_by_popular(self):
        """Test sorting by popularity (rating * count)."""
        response = self.client.get(reverse('dashboard') + '?sort=popular')
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context['recipes'])
        
        # Recipe with rating should be first
        self.assertEqual(recipes[0], self.popular_recipe)

    def test_dashboard_sort_by_trending(self):
        """Test sorting by active viewers."""
        # Add active viewers to one recipe
        self.viewed_recipe.add_viewer(user_id=1)
        self.viewed_recipe.add_viewer(user_id=2)
        self.viewed_recipe.add_viewer(user_id=3)
        
        response = self.client.get(reverse('dashboard') + '?sort=trending')
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context['recipes'])
        
        # Recipe with most active viewers should be first
        self.assertEqual(recipes[0], self.viewed_recipe)

    def test_sort_option_in_context(self):
        """Test that sort options are in context."""
        response = self.client.get(reverse('dashboard'))
        self.assertIn('sort_options', response.context)
        self.assertIn('selected_sort', response.context)

    def test_selected_sort_preserved(self):
        """Test that selected sort is preserved in context."""
        response = self.client.get(reverse('dashboard') + '?sort=most_viewed')
        self.assertEqual(response.context['selected_sort'], 'most_viewed')

    def test_invalid_sort_uses_default(self):
        """Test that invalid sort option uses default."""
        response = self.client.get(reverse('dashboard') + '?sort=invalid')
        self.assertEqual(response.status_code, 200)
        # Should still work, just use default sorting


class RecipeDetailViewTrackingTestCase(TestCase):
    """Test view tracking in recipe detail view."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="Test",
            ingredients="flour",
            time=30,
            meal_type="lunch"
        )
        cache.clear()

    def tearDown(self):
        """Clear cache."""
        cache.clear()

    def test_viewing_recipe_increments_views(self):
        """Test that viewing a recipe increments the view count."""
        self.client.login(username='@johndoe', password='Password123')
        initial_views = self.recipe.total_views
        
        response = self.client.get(reverse('recipe_detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.total_views, initial_views + 1)

    def test_active_viewers_in_context(self):
        """Test that active viewers count is in context."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('recipe_detail', kwargs={'pk': self.recipe.pk}))
        
        self.assertIn('active_viewers', response.context)
        self.assertIn('total_views', response.context)

    def test_multiple_users_viewing_simultaneously(self):
        """Test multiple users viewing recipe at same time."""
        # User 1 views
        client1 = Client()
        client1.login(username='@johndoe', password='Password123')
        client1.get(reverse('recipe_detail', kwargs={'pk': self.recipe.pk}))
        
        # User 2 views
        other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123'
        )
        client2 = Client()
        client2.login(username='@janedoe', password='Password123')
        response = client2.get(reverse('recipe_detail', kwargs={'pk': self.recipe.pk}))
        
        # Should have 2 active viewers
        self.assertEqual(response.context['active_viewers'], 2)


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

    def test_trending_badge_displayed(self):
        """Test that trending badge is displayed in template."""
        # Make recipe trending
        self.trending_recipe.add_viewer(user_id=1)
        self.trending_recipe.add_viewer(user_id=2)
        self.trending_recipe.add_viewer(user_id=3)
        
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('dashboard'))
        
        content = response.content.decode()
        # Should contain trending badge
        self.assertIn('Trending', content)
