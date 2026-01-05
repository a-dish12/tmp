"""Tests for rating views."""
from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Rating
from recipes.tests.test_helpers import LogInTester


class RateRecipeViewTestCase(TestCase, LogInTester):
    """Tests for the rate recipe view."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        
        self.recipe = Recipe.objects.create(
            author=self.other_user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="lunch"
        )
        
        self.url = reverse('rate_recipe', kwargs={'recipe_pk': self.recipe.pk})
        self.redirect_url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_rate_recipe_url(self):
        self.assertEqual(self.url, f'/recipes/{self.recipe.pk}/rate/')

    def test_rate_recipe_redirects_when_not_logged_in(self):
        """Test that non-authenticated users are redirected to login."""
        response = self.client.post(self.url, {'stars': 5}, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_rating_creation(self):
        """Test that a user can successfully rate a recipe."""
        self.client.login(username=self.user.username, password='Password123')
        self.assertFalse(Rating.objects.filter(recipe=self.recipe, user=self.user).exists())
        
        response = self.client.post(self.url, {'stars': 4}, follow=True)
        
        self.assertTrue(Rating.objects.filter(recipe=self.recipe, user=self.user).exists())
        rating = Rating.objects.get(recipe=self.recipe, user=self.user)
        self.assertEqual(rating.stars, 4)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)

    def test_update_existing_rating(self):
        """Test that a user can update their existing rating."""
        self.client.login(username=self.user.username, password='Password123')
        
        # Create initial rating
        Rating.objects.create(recipe=self.recipe, user=self.user, stars=3)
        
        # Update rating
        response = self.client.post(self.url, {'stars': 5}, follow=True)
        
        rating = Rating.objects.get(recipe=self.recipe, user=self.user)
        self.assertEqual(rating.stars, 5)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)

    def test_cannot_rate_own_recipe(self):
        """Test that users cannot rate their own recipes."""
        self.client.login(username=self.other_user.username, password='Password123')
        
        response = self.client.post(self.url, {'stars': 5}, follow=True)
        
        self.assertFalse(Rating.objects.filter(recipe=self.recipe, user=self.other_user).exists())
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)

    def test_rating_increments_recipe_rating_count(self):
        """Test that rating increases the recipe's rating count."""
        self.client.login(username=self.user.username, password='Password123')
        initial_count = self.recipe.rating_count()
        
        self.client.post(self.url, {'stars': 4})
        
        self.assertEqual(self.recipe.rating_count(), initial_count + 1)


class RecipeDetailViewRatingDisplayTestCase(TestCase, LogInTester):
    """Tests for rating display in recipe detail view."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        
        self.recipe = Recipe.objects.create(
            author=self.other_user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="lunch"
        )
        
        self.url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_recipe_detail_shows_average_rating(self):
        """Test that recipe detail page displays average rating."""
        Rating.objects.create(recipe=self.recipe, user=self.user, stars=4)
        Rating.objects.create(recipe=self.recipe, user=User.objects.get(username='@petrapickles'), stars=2)
        
        response = self.client.get(self.url)
        
        self.assertContains(response, '3.0')  # Average of 4 and 2

    def test_recipe_detail_shows_rating_count(self):
        """Test that recipe detail page displays rating count."""
        Rating.objects.create(recipe=self.recipe, user=self.user, stars=5)
        
        response = self.client.get(self.url)
        
        self.assertContains(response, '1 rating')

    def test_recipe_detail_shows_user_rating_when_logged_in(self):
        """Test that logged-in users see their own rating."""
        self.client.login(username=self.user.username, password='Password123')
        Rating.objects.create(recipe=self.recipe, user=self.user, stars=4)
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'You rated this: 4')

    def test_recipe_detail_shows_rating_form_when_not_rated(self):
        """Test that rating form is shown when user hasn't rated."""
        self.client.login(username=self.user.username, password='Password123')
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Rate this recipe')
        self.assertContains(response, 'name="stars"')
