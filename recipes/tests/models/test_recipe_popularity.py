"""Tests for recipe popularity and view tracking features."""
from django.test import TestCase
from django.core.cache import cache
from django.utils import timezone
from recipes.models import Recipe, User, Rating
from datetime import timedelta


class RecipeViewTrackingTestCase(TestCase):
    """Test view tracking functionality."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="Test description",
            ingredients="flour, water",
            time=30,
            meal_type="lunch"
        )
        cache.clear()

    def tearDown(self):
        """Clear cache after each test."""
        cache.clear()

    def test_recipe_has_view_tracking_fields(self):
        """Test that recipe has view tracking fields."""
        self.assertEqual(self.recipe.total_views, 0)
        self.assertIsNone(self.recipe.last_viewed_at)

    def test_add_viewer_increments_total_views(self):
        """Test that adding a viewer increments total views."""
        initial_views = self.recipe.total_views
        self.recipe.add_viewer(user_id=1)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.total_views, initial_views + 1)

    def test_add_viewer_updates_last_viewed_at(self):
        """Test that adding a viewer updates last_viewed_at."""
        self.assertIsNone(self.recipe.last_viewed_at)
        before = timezone.now()
        self.recipe.add_viewer(user_id=1)
        self.recipe.refresh_from_db()
        after = timezone.now()
        
        self.assertIsNotNone(self.recipe.last_viewed_at)
        self.assertGreaterEqual(self.recipe.last_viewed_at, before)
        self.assertLessEqual(self.recipe.last_viewed_at, after)

    def test_same_viewer_only_counts_once(self):
        """Test that the same viewer viewing again doesn't increment views."""
        self.recipe.add_viewer(user_id=1)
        self.recipe.refresh_from_db()
        initial_views = self.recipe.total_views
        
        # Same viewer again
        self.recipe.add_viewer(user_id=1)
        self.recipe.refresh_from_db()
        
        self.assertEqual(self.recipe.total_views, initial_views)

    def test_different_viewers_count_separately(self):
        """Test that different viewers increment views separately."""
        self.recipe.add_viewer(user_id=1)
        self.recipe.refresh_from_db()
        initial_views = self.recipe.total_views
        
        self.recipe.add_viewer(user_id=2)
        self.recipe.refresh_from_db()
        
        self.assertEqual(self.recipe.total_views, initial_views + 1)

    def test_get_active_viewers_returns_count(self):
        """Test that get_active_viewers returns correct count."""
        self.assertEqual(self.recipe.get_active_viewers(), 0)
        
        self.recipe.add_viewer(user_id=1)
        self.assertEqual(self.recipe.get_active_viewers(), 1)
        
        self.recipe.add_viewer(user_id=2)
        self.assertEqual(self.recipe.get_active_viewers(), 2)

    def test_anonymous_viewers_tracked(self):
        """Test that anonymous viewers are tracked."""
        self.recipe.add_viewer(user_id="anon_session123")
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.total_views, 1)
        self.assertEqual(self.recipe.get_active_viewers(), 1)


class RecipePopularityTestCase(TestCase):
    """Test recipe popularity scoring."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123',
            first_name='Jane',
            last_name='Doe'
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Popular Recipe",
            description="Test description",
            ingredients="flour, water",
            time=30,
            meal_type="lunch"
        )

    def test_popularity_score_with_no_ratings_or_views(self):
        """Test popularity score for recipe with no engagement."""
        score = self.recipe.get_popularity_score()
        self.assertEqual(score, 0)

    def test_popularity_score_with_only_views(self):
        """Test popularity score based on views."""
        self.recipe.total_views = 100
        self.recipe.save()
        
        score = self.recipe.get_popularity_score()
        self.assertEqual(score, 10.0)  # 100 * 0.1

    def test_popularity_score_with_ratings(self):
        """Test popularity score with ratings."""
        Rating.objects.create(recipe=self.recipe, user=self.other_user, stars=5)
        
        score = self.recipe.get_popularity_score()
        # avg_rating=5, rating_count=1 -> 5 * 1 = 5
        self.assertEqual(score, 5.0)

    def test_popularity_score_with_multiple_ratings(self):
        """Test popularity score with multiple ratings."""
        user3 = User.objects.create_user(
            username='@user3',
            email='user3@example.com',
            password='Password123'
        )
        
        Rating.objects.create(recipe=self.recipe, user=self.other_user, stars=5)
        Rating.objects.create(recipe=self.recipe, user=user3, stars=4)
        
        score = self.recipe.get_popularity_score()
        # avg_rating=4.5, rating_count=2 -> 4.5 * 2 = 9
        self.assertEqual(score, 9.0)

    def test_popularity_score_with_ratings_and_views(self):
        """Test popularity score combining ratings and views."""
        Rating.objects.create(recipe=self.recipe, user=self.other_user, stars=5)
        self.recipe.total_views = 50
        self.recipe.save()
        
        score = self.recipe.get_popularity_score()
        # (5 * 1) + (50 * 0.1) = 5 + 5 = 10
        self.assertEqual(score, 10.0)


class RecipeSortingTestCase(TestCase):
    """Test recipe sorting by popularity metrics."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        """Set up test recipes with different metrics."""
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123',
            first_name='Jane',
            last_name='Doe'
        )
        
        # Recipe 1: High views
        self.recipe1 = Recipe.objects.create(
            author=self.user,
            title="Most Viewed",
            description="Test",
            ingredients="flour",
            time=30,
            meal_type="lunch",
            total_views=1000
        )
        
        # Recipe 2: High ratings
        self.recipe2 = Recipe.objects.create(
            author=self.user,
            title="Highly Rated",
            description="Test",
            ingredients="water",
            time=20,
            meal_type="dinner",
            total_views=50
        )
        Rating.objects.create(recipe=self.recipe2, user=self.other_user, stars=5)
        
        # Recipe 3: Recent
        self.recipe3 = Recipe.objects.create(
            author=self.user,
            title="Newest",
            description="Test",
            ingredients="sugar",
            time=15,
            meal_type="snack",
            total_views=10
        )

    def test_sort_by_most_viewed(self):
        """Test sorting by total views."""
        recipes = Recipe.objects.all().order_by('-total_views')
        self.assertEqual(recipes[0], self.recipe1)
        self.assertEqual(recipes[0].total_views, 1000)

    def test_sort_by_newest(self):
        """Test sorting by creation date."""
        recipes = Recipe.objects.all().order_by('-created_at')
        self.assertEqual(recipes[0], self.recipe3)

    def test_default_sort_by_time(self):
        """Test default sorting by prep time."""
        recipes = Recipe.objects.all().order_by('time')
        self.assertEqual(recipes[0], self.recipe3)
        self.assertEqual(recipes[0].time, 15)
