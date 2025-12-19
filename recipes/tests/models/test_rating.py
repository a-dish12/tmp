"""Unit tests for the Rating model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import User, Recipe, Rating


class RatingModelTestCase(TestCase):
    """Unit tests for the Rating model."""

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
        
        self.rating = Rating.objects.create(
            recipe=self.recipe,
            user=self.user,
            stars=4
        )

    def test_valid_rating(self):
        self._assert_rating_is_valid()

    def test_rating_stars_cannot_be_less_than_1(self):
        self.rating.stars = 0
        self._assert_rating_is_invalid()

    def test_rating_stars_cannot_be_more_than_5(self):
        self.rating.stars = 6
        self._assert_rating_is_invalid()

    def test_rating_stars_can_be_1(self):
        self.rating.stars = 1
        self._assert_rating_is_valid()

    def test_rating_stars_can_be_5(self):
        self.rating.stars = 5
        self._assert_rating_is_valid()

    def test_rating_requires_recipe(self):
        self.rating.recipe = None
        self._assert_rating_is_invalid()

    def test_rating_requires_user(self):
        self.rating.user = None
        self._assert_rating_is_invalid()

    def test_unique_rating_per_user_per_recipe(self):
        """Test that a user can only rate a recipe once."""
        with self.assertRaises(Exception):
            Rating.objects.create(
                recipe=self.recipe,
                user=self.user,
                stars=3
            )

    def test_different_users_can_rate_same_recipe(self):
        """Test that different users can rate the same recipe."""
        third_user = User.objects.get(username='@petrapickles')
        rating2 = Rating.objects.create(
            recipe=self.recipe,
            user=third_user,
            stars=5
        )
        self.assertEqual(Rating.objects.filter(recipe=self.recipe).count(), 2)

    def test_recipe_average_rating_calculation(self):
        """Test that recipe calculates average rating correctly."""
        Rating.objects.create(
            recipe=self.recipe,
            user=User.objects.get(username='@petrapickles'),
            stars=2
        )
        # Average of 4 and 2 should be 3.0
        self.assertEqual(self.recipe.average_rating(), 3.0)

    def test_recipe_rating_count(self):
        """Test that recipe counts ratings correctly."""
        self.assertEqual(self.recipe.rating_count(), 1)
        Rating.objects.create(
            recipe=self.recipe,
            user=User.objects.get(username='@petrapickles'),
            stars=5
        )
        self.assertEqual(self.recipe.rating_count(), 2)

    def test_rating_string_representation(self):
        """Test the string representation of a rating."""
        expected = f"{self.user.username} rated {self.recipe.title}: 4 stars"
        self.assertEqual(str(self.rating), expected)

    def _assert_rating_is_valid(self):
        try:
            self.rating.full_clean()
        except ValidationError:
            self.fail('Test rating should be valid')

    def _assert_rating_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.rating.full_clean()
