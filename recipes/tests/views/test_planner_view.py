"""Tests for planner/planner meal views."""
from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta
from recipes.models import User, Recipe, PlannedDay, PlannedMeal
from recipes.tests.helpers import LogInTester


class AddToPlannerViewTestCase(TestCase, LogInTester):
    """Tests for the add to planner view."""

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
        
        self.url = reverse('add_to_planner', kwargs={'recipe_pk': self.recipe.pk})
        self.redirect_url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})
        self.today = date.today()

    def test_add_to_planner_url(self):
        self.assertEqual(self.url, f'/recipes/{self.recipe.pk}/add-to-planner/')

    def test_add_to_planner_redirects_when_not_logged_in(self):
        """Test that non-authenticated users are redirected to login."""
        response = self.client.post(self.url, {
            'date': self.today.isoformat(),
            'meal_type': 'breakfast'
        }, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_add_to_planner(self):
        """Test that a user can successfully add a recipe to planner."""
        self.client.login(username=self.user.username, password='Password123')
        
        response = self.client.post(self.url, {
            'date': self.today.isoformat(),
            'meal_type': 'breakfast'
        }, follow=True)
        
        self.assertTrue(PlannedDay.objects.filter(user=self.user, date=self.today).exists())
        planned_day = PlannedDay.objects.get(user=self.user, date=self.today)
        self.assertTrue(PlannedMeal.objects.filter(
            planned_day=planned_day,
            recipe=self.recipe,
            meal_type='breakfast'
        ).exists())
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)

    def test_add_to_planner_requires_date(self):
        """Test that adding to planner requires a date."""
        self.client.login(username=self.user.username, password='Password123')
        before_count = PlannedMeal.objects.count()
        
        response = self.client.post(self.url, {
            'meal_type': 'breakfast'
        }, follow=True)
        
        self.assertEqual(PlannedMeal.objects.count(), before_count)

    def test_add_to_planner_requires_meal_type(self):
        """Test that adding to planner requires a meal type."""
        self.client.login(username=self.user.username, password='Password123')
        before_count = PlannedMeal.objects.count()
        
        response = self.client.post(self.url, {
            'date': self.today.isoformat()
        }, follow=True)
        
        self.assertEqual(PlannedMeal.objects.count(), before_count)

    def test_add_same_recipe_to_different_meals(self):
        """Test that the same recipe can be added to different meal types."""
        self.client.login(username=self.user.username, password='Password123')
        
        self.client.post(self.url, {
            'date': self.today.isoformat(),
            'meal_type': 'breakfast'
        })
        
        self.client.post(self.url, {
            'date': self.today.isoformat(),
            'meal_type': 'lunch'
        })
        
        planned_day = PlannedDay.objects.get(user=self.user, date=self.today)
        self.assertEqual(planned_day.meals.filter(recipe=self.recipe).count(), 2)

    def test_add_same_recipe_to_different_dates(self):
        """Test that the same recipe can be added to different dates."""
        self.client.login(username=self.user.username, password='Password123')
        tomorrow = self.today + timedelta(days=1)
        
        self.client.post(self.url, {
            'date': self.today.isoformat(),
            'meal_type': 'lunch'
        })
        
        self.client.post(self.url, {
            'date': tomorrow.isoformat(),
            'meal_type': 'lunch'
        })
        
        self.assertEqual(PlannedMeal.objects.filter(recipe=self.recipe).count(), 2)

    def test_cannot_add_duplicate_meal(self):
        """Test that the same recipe cannot be added twice to the same meal/date."""
        self.client.login(username=self.user.username, password='Password123')
        
        self.client.post(self.url, {
            'date': self.today.isoformat(),
            'meal_type': 'dinner'
        })
        
        before_count = PlannedMeal.objects.count()
        
        self.client.post(self.url, {
            'date': self.today.isoformat(),
            'meal_type': 'dinner'
        })
        
        # Count should not increase
        self.assertEqual(PlannedMeal.objects.count(), before_count)


class RemoveFromPlannerViewTestCase(TestCase, LogInTester):
    """Tests for the remove from planner view."""

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
        
        self.today = date.today()
        self.planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        self.planned_meal = PlannedMeal.objects.create(
            planned_day=self.planned_day,
            meal_type='breakfast',
            recipe=self.recipe
        )
        
        self.url = reverse('remove_from_planner', kwargs={'meal_pk': self.planned_meal.pk})

    def test_remove_from_planner_url(self):
        self.assertEqual(self.url, f'/planned-meals/{self.planned_meal.pk}/remove/')

    def test_remove_from_planner_redirects_when_not_logged_in(self):
        """Test that non-authenticated users are redirected to login."""
        response = self.client.post(self.url, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_remove_from_planner(self):
        """Test that a user can successfully remove a meal from planner."""
        self.client.login(username=self.user.username, password='Password123')
        meal_id = self.planned_meal.pk
        
        response = self.client.post(self.url)
        
        self.assertFalse(PlannedMeal.objects.filter(pk=meal_id).exists())

    def test_cannot_remove_other_users_meal(self):
        """Test that users cannot remove meals from other users' planners."""
        self.client.login(username=self.other_user.username, password='Password123')
        meal_id = self.planned_meal.pk
        
        response = self.client.get(self.url)
        
        # Should get 404 for other user's meal
        self.assertEqual(response.status_code, 404)
        self.assertTrue(PlannedMeal.objects.filter(pk=meal_id).exists())

    def test_remove_with_next_parameter_redirects_correctly(self):
        """Test that remove redirects to 'next' parameter if provided."""
        self.client.login(username=self.user.username, password='Password123')
        recipe_url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})
        url_with_next = f"{self.url}?next={recipe_url}"
        
        response = self.client.post(url_with_next, follow=True)
        
        self.assertRedirects(response, recipe_url, status_code=302, target_status_code=200)


class PlannerDayViewTestCase(TestCase, LogInTester):
    """Tests for the planner day view."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.today = date.today()
        
        self.recipe = Recipe.objects.create(
            author=self.other_user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="lunch"
        )
        
        self.url = reverse('planner_day', kwargs={'date': self.today.isoformat()})

    def test_planner_day_url(self):
        self.assertEqual(self.url, f'/planner/{self.today.isoformat()}/')

    def test_planner_day_redirects_when_not_logged_in(self):
        """Test that non-authenticated users are redirected to login."""
        response = self.client.get(self.url, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_planner_day(self):
        """Test that logged-in users can access planner day view."""
        self.client.login(username=self.user.username, password='Password123')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'day.html')

    def test_planner_day_shows_planned_meals(self):
        """Test that planner day displays planned meals."""
        self.client.login(username=self.user.username, password='Password123')
        
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        PlannedMeal.objects.create(
            planned_day=planned_day,
            meal_type='breakfast',
            recipe=self.recipe
        )
        
        response = self.client.get(self.url)
        
        self.assertContains(response, self.recipe.title)
        self.assertContains(response, 'breakfast')

    def test_planner_day_can_add_meal(self):
        """Test that users can add meals from the day view."""
        self.client.login(username=self.user.username, password='Password123')
        
        response = self.client.post(self.url, {
            'meal_type': 'dinner',
            'recipe': self.recipe.id
        }, follow=True)
        
        planned_day = PlannedDay.objects.get(user=self.user, date=self.today)
        self.assertTrue(PlannedMeal.objects.filter(
            planned_day=planned_day,
            recipe=self.recipe,
            meal_type='dinner'
        ).exists())

    def test_planner_day_shows_remove_buttons(self):
        """Test that planner day shows remove buttons for planned meals."""
        self.client.login(username=self.user.username, password='Password123')
        
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        meal = PlannedMeal.objects.create(
            planned_day=planned_day,
            meal_type='lunch',
            recipe=self.recipe
        )
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Remove')
        self.assertContains(response, reverse('remove_from_planner', kwargs={'meal_pk': meal.pk}))


class RecipeDetailPlannedMealsDisplayTestCase(TestCase, LogInTester):
    """Tests for planned meals display in recipe detail view."""

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
        self.today = date.today()

    def test_recipe_detail_shows_add_to_planner_form(self):
        """Test that recipe detail shows add to planner form when logged in."""
        self.client.login(username=self.user.username, password='Password123')
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Add to Meal Planner')
        self.assertContains(response, 'name="date"')
        self.assertContains(response, 'name="meal_type"')

    def test_recipe_detail_shows_existing_planned_meals(self):
        """Test that recipe detail shows where recipe is already planned."""
        self.client.login(username=self.user.username, password='Password123')
        
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        PlannedMeal.objects.create(
            planned_day=planned_day,
            meal_type='breakfast',
            recipe=self.recipe
        )
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Currently planned for')
        self.assertContains(response, 'breakfast')

    def test_recipe_detail_shows_remove_buttons_for_planned_meals(self):
        """Test that recipe detail shows remove buttons for planned meals."""
        self.client.login(username=self.user.username, password='Password123')
        
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        meal = PlannedMeal.objects.create(
            planned_day=planned_day,
            meal_type='lunch',
            recipe=self.recipe
        )
        
        response = self.client.get(self.url)
        
        remove_url = reverse('remove_from_planner', kwargs={'meal_pk': meal.pk})
        self.assertContains(response, remove_url)
