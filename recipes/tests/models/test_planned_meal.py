"""
Unit tests for the PlannedDay and PlannedMeal models.

These tests verify model validation, uniqueness constraints, cascade
deletion behaviour, related names, and string representations.
"""

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError
from datetime import date, timedelta

from recipes.models import User, Recipe, PlannedDay, PlannedMeal


class PlannedDayModelTestCase(TestCase):
    """
    Test suite for the PlannedDay model.
    """

    fixtures = [
        'recipes/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        """
        Create a sample user and a planned day for testing.
        """
        self.user = User.objects.get(username='@johndoe')
        self.today = date.today()

        self.planned_day = PlannedDay.objects.create(
            user=self.user,
            date=self.today
        )

    def test_valid_planned_day(self):
        """
        A PlannedDay with valid fields passes validation.
        """
        self._assert_planned_day_is_valid()

    def test_planned_day_requires_user(self):
        """
        A PlannedDay without a user is invalid.
        """
        self.planned_day.user = None
        self._assert_planned_day_is_invalid()

    def test_planned_day_requires_date(self):
        """
        A PlannedDay without a date is invalid.
        """
        self.planned_day.date = None
        self._assert_planned_day_is_invalid()

    def test_user_can_have_multiple_planned_days(self):
        """
        A user can create multiple planned days on different dates.
        """
        tomorrow = self.today + timedelta(days=1)
        PlannedDay.objects.create(
            user=self.user,
            date=tomorrow
        )

        self.assertEqual(self.user.planned_days.count(), 2)

    def test_unique_user_date_combination(self):
        """
        A user cannot have more than one planned day for the same date.
        """
        with self.assertRaises(IntegrityError):
            PlannedDay.objects.create(
                user=self.user,
                date=self.today
            )

    def test_planned_day_string_representation(self):
        """
        The string representation includes the planned date.
        """
        self.assertIn(str(self.today), str(self.planned_day))

    def test_planned_days_deleted_when_user_deleted(self):
        """
        PlannedDay objects are deleted when their owning user is deleted.
        """
        planned_day_id = self.planned_day.id
        self.user.delete()

        self.assertFalse(PlannedDay.objects.filter(id=planned_day_id).exists())

    def _assert_planned_day_is_valid(self):
        try:
            self.planned_day.full_clean()
        except ValidationError:
            self.fail('PlannedDay should be valid')

    def _assert_planned_day_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.planned_day.full_clean()


class PlannedMealModelTestCase(TestCase):
    """
    Test suite for the PlannedMeal model.
    """

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        """
        Create a planned day and a planned meal for testing.
        """
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
        """
        A PlannedMeal with valid fields passes validation.
        """
        self._assert_planned_meal_is_valid()

    def test_planned_meal_requires_planned_day(self):
        """
        A PlannedMeal without a planned day is invalid.
        """
        self.planned_meal.planned_day = None
        self._assert_planned_meal_is_invalid()

    def test_planned_meal_requires_meal_type(self):
        """
        A PlannedMeal without a meal type is invalid.
        """
        self.planned_meal.meal_type = ''
        self._assert_planned_meal_is_invalid()

    def test_planned_meal_requires_recipe(self):
        """
        A PlannedMeal without a recipe is invalid.
        """
        self.planned_meal.recipe = None
        self._assert_planned_meal_is_invalid()

    def test_planned_day_can_have_multiple_meals(self):
        """
        A planned day can contain multiple meals.
        """
        PlannedMeal.objects.create(
            planned_day=self.planned_day,
            meal_type="lunch",
            recipe=self.recipe
        )

        self.assertEqual(self.planned_day.meals.count(), 2)

    def test_unique_planned_meal_constraint(self):
        """
        The same recipe cannot be added twice for the same meal type on the same day.
        """
        with self.assertRaises(IntegrityError):
            PlannedMeal.objects.create(
                planned_day=self.planned_day,
                meal_type="breakfast",
                recipe=self.recipe
            )

    def test_same_recipe_can_be_planned_for_different_meal_types(self):
        """
        The same recipe can be planned for different meal types.
        """
        PlannedMeal.objects.create(
            planned_day=self.planned_day,
            meal_type="dinner",
            recipe=self.recipe
        )

        self.assertEqual(
            PlannedMeal.objects.filter(recipe=self.recipe).count(),
            2
        )

    def test_planned_meal_string_representation(self):
        """
        The string representation includes the meal type and recipe title.
        """
        self.assertIn("Breakfast", str(self.planned_meal))
        self.assertIn(self.recipe.title, str(self.planned_meal))

    def test_planned_meals_deleted_when_planned_day_deleted(self):
        """
        PlannedMeal objects are deleted when their PlannedDay is deleted.
        """
        planned_meal_id = self.planned_meal.id
        self.planned_day.delete()

        self.assertFalse(
            PlannedMeal.objects.filter(id=planned_meal_id).exists()
        )

    def test_planned_meals_deleted_when_recipe_deleted(self):
        """
        PlannedMeal objects are deleted when their Recipe is deleted.
        """
        planned_meal_id = self.planned_meal.id
        self.recipe.delete()

        self.assertFalse(
            PlannedMeal.objects.filter(id=planned_meal_id).exists()
        )

    def test_planned_day_meals_related_name_contains_created_meal(self):
        """
        The related name 'meals' returns the planned meal for the planned day.
        """
        self.assertIn(
            self.planned_meal,
            self.planned_day.meals.all()
        )

    def test_meal_type_max_length_validation(self):
        """
        The meal_type field enforces its max_length constraint.
        """
        self.planned_meal.meal_type = "x" * 21
        self._assert_planned_meal_is_invalid()

    def _assert_planned_meal_is_valid(self):
        try:
            self.planned_meal.full_clean()
        except ValidationError:
            self.fail('PlannedMeal should be valid')

    def _assert_planned_meal_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.planned_meal.full_clean()
