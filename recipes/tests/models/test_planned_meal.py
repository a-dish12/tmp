"""Unit tests for PlannedMeal and PlannedDay models."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError
from datetime import date, timedelta
from recipes.models import User, Recipe, PlannedDay, PlannedMeal


class PlannedDayModelTestCase(TestCase):
    """Unit tests for the PlannedDay model."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.today = date.today()
        
        self.planned_day = PlannedDay.objects.create(
            user=self.user,
            date=self.today
        )

    def test_valid_planned_day(self):
        self._assert_planned_day_is_valid()

    def test_planned_day_requires_user(self):
        self.planned_day.user = None
        self._assert_planned_day_is_invalid()

    def test_planned_day_requires_date(self):
        self.planned_day.date = None
        self._assert_planned_day_is_invalid()

    def test_user_can_have_multiple_planned_days(self):
        """Test that a user can have multiple planned days."""
        tomorrow = self.today + timedelta(days=1)
        planned_day2 = PlannedDay.objects.create(
            user=self.user,
            date=tomorrow
        )
        self.assertEqual(self.user.planned_days.count(), 2)

    def test_unique_user_date_combination(self):
        """Test that a user cannot have duplicate planned days for same date."""
        with self.assertRaises(IntegrityError):
            PlannedDay.objects.create(
                user=self.user,
                date=self.today
            )

    def test_planned_day_string_representation(self):
        """Test the string representation of a planned day."""
        self.assertIn(str(self.today), str(self.planned_day))

    def _assert_planned_day_is_valid(self):
        try:
            self.planned_day.full_clean()
        except ValidationError:
            self.fail('Test planned day should be valid')

    def _assert_planned_day_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.planned_day.full_clean()


class PlannedMealModelTestCase(TestCase):
    """Unit tests for the PlannedMeal model."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.today = date.today()
        
        self.planned_day = PlannedDay.objects.create(
            user=self.user,
            date=self.today
        )
        
        self.recipe = Recipe.objects.create(
            author=self.other_user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="lunch"
        )
        
        self.planned_meal = PlannedMeal.objects.create(
            planned_day=self.planned_day,
            meal_type="breakfast",
            recipe=self.recipe
        )

    def test_valid_planned_meal(self):
        self._assert_planned_meal_is_valid()

    def test_planned_meal_requires_planned_day(self):
        self.planned_meal.planned_day = None
        self._assert_planned_meal_is_invalid()

    def test_planned_meal_requires_meal_type(self):
        self.planned_meal.meal_type = ''
        self._assert_planned_meal_is_invalid()

    def test_planned_meal_requires_recipe(self):
        self.planned_meal.recipe = None
        self._assert_planned_meal_is_invalid()

    def test_planned_day_can_have_multiple_meals(self):
        """Test that a planned day can have multiple meals."""
        PlannedMeal.objects.create(
            planned_day=self.planned_day,
            meal_type="lunch",
            recipe=self.recipe
        )
        self.assertEqual(self.planned_day.meals.count(), 2)

    def test_unique_planned_meal_constraint(self):
        """Test that same recipe cannot be added twice for same meal type on same day."""
        with self.assertRaises(IntegrityError):
            PlannedMeal.objects.create(
                planned_day=self.planned_day,
                meal_type="breakfast",
                recipe=self.recipe
            )

    def test_same_recipe_can_be_planned_for_different_meal_types(self):
        """Test that same recipe can be added for different meal types."""
        PlannedMeal.objects.create(
            planned_day=self.planned_day,
            meal_type="dinner",
            recipe=self.recipe
        )
        self.assertEqual(PlannedMeal.objects.filter(recipe=self.recipe).count(), 2)

    def test_planned_meal_string_representation(self):
        """Test the string representation of a planned meal."""
        self.assertIn("Breakfast", str(self.planned_meal))
        self.assertIn(self.recipe.title, str(self.planned_meal))

    def _assert_planned_meal_is_valid(self):
        try:
            self.planned_meal.full_clean()
        except ValidationError:
            self.fail('Test planned meal should be valid')

    def _assert_planned_meal_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.planned_meal.full_clean()
