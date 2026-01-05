""" Extra tests for planner-related views
These focus on:
-Calendar UI rendering
-Calendar JSON events
-Planner range view
- Ingredients list generation

They add to test_planner_view.py

"""
from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta
from recipes.models import User, Recipe, PlannedDay, PlannedMeal
from recipes.tests.test_helpers import LogInTester

    
class PlannerRangeViewTestCase(TestCase,LogInTester):
    """Tests for the range-based planner view"""
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.recipe = Recipe.objects.create(
            author = self.other_user,
            title="Range Recipe",
            description="Test",
            ingredients = "Milk",
            time =15,
            meal_type="breakfast"
        )
        self.url = reverse('planner_range')

    def test_range_redirects_when_not_logged_in(self):
        """Planner range view should be log in protected"""
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, f"{reverse('log_in')}?next={self.url}")

    def test_range_renders_default_week(self):
        """Logged-in users shoudl see the planner range page"""
        self.client.login(username=self.user.username, password =  'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner_range.html')
    
    def test_range_post_adds_meal(self):
        """Posting valid date should add a planned meal"""
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, {
            'date': date.today().isoformat(),
            'meal_type': 'breakfast',
            'recipe_search': self.recipe.pk
        }, follow=True
        )
        self.assertTrue(
            PlannedMeal.objects.filter(
                planned_day__user = self.user, recipe = self.recipe
            ).exists()
        )
    def test_range_post_replaces_existing_meal(self):
        """Posting a meal to the same slot replaces the existing one"""
        self.client.login(username=self.user.username, password='Password123')
        today = date.today()
        planned_day = PlannedDay.objects.create(user=self.user, date=today)
        old_recipe = Recipe.objects.create(
            author = self.other_user,
            title="Old Recipe",
            description="Old",
            ingredients="Old",
            time=10,
            meal_type="breakfast"
        )
        PlannedMeal.objects.create(
            planned_day = planned_day,
            meal_type = "breakfast",
            recipe=old_recipe
        )
        self.client.post(self.url,{
            'date': today.isoformat(),
            'meal_type': 'breakfast',
            'recipe_search': self.recipe.pk
        })
        meal = PlannedMeal.objects.get(planned_day=planned_day, meal_type="breakfast")
        self.assertEqual(meal.recipe, self.recipe)

    def test_range_post_invalid_recipe_does_not_crash(self):
        """Invalid recipe IDs should not create meals"""
        self.client.login(username=self.user.username, password='Password123')
        before = PlannedMeal.objects.count()

        self.client.post(
            self.url,{
                'date': date.today().isoformat(),
                'meal_type': 'breakfast',
                'recipe_search': 999999
            }
        )
        self.assertEqual(PlannedMeal.objects.count(), before)
    
    def test_range_swaps_start_and_end_dates(self):
        """Planner range should handle start date after end date"""
        self.client.login(username=self.user.username, password='Password123')

        start = date.today()
        end = start - timedelta(days=3)

        response = self.client.get(self.url,
                                   {
                                       'start': start.isoformat(),
                                       'end': end.isoformat()
                                   })
        self.assertEqual(response.status_code, 200)


class IngredientsListViewTestCase(TestCase, LogInTester):
    """Tests for ingredient list generator"""
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.recipe = Recipe.objects.create(
            author = self.other_user,
            title="Ingredient Recipe",
            description="Test",
            ingredients = "Eggs\nMilk\nButter",
            time =25,
            meal_type="dinner"
        )
        today = date.today()
        planned_day = PlannedDay.objects.create(user=self.user, date = today)
        PlannedMeal.objects.create(
            planned_day = planned_day,
            meal_type='dinner',
            recipe = self.recipe
        )
        self.url = reverse('ingredients_list')
    
    def test_ingredients_redirect_when_not_logged_in(self):
        """Ingredients list should require authentication"""
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, f"{reverse('log_in')}?next={self.url}")

    def test_ingredients_list_contains_ingredients(self):
        """Ingredients list should show individual ingredient lines"""
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eggs")
        self.assertContains(response, "Milk")
        self.assertContains(response, "Butter")
    

class PlannerEventsTest(TestCase, LogInTester):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.client.login(username="@johndoe", password="Password123")
        self.url = "/planner/events/"
    def test_events_with_start_and_end(self):
        response = self.client.get(self.url,{
            'start': date.today().isoformat(),
            'end': (date.today() + timedelta(days=1)).isoformat()
        })
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.json(), list)
    def test_events_with_only_start(self):
        response=self.client.get(self.url,{
            'start': date.today().isoformat()
        })
        self.assertEqual(response.status_code,200)
    

class PlannerDayBranchTest(TestCase, LogInTester):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.private_user = User.objects.get(username='@janedoe')
        self.private_user.is_private = True
        self.private_user.save()

        self.recipe = Recipe.objects.create(
            author=self.private_user,
            title="Private",
            description="x",
            ingredients="x",
            time=10,
            meal_type="lunch"
        )
        self.client.login(username="@johndoe", password = "Password123")
        self.url = reverse('planner_day', args=[date.today().isoformat()])

    def test_planner_next_redirect(self):
        self.private_user.is_private=False
        self.private_user.save()
        response = self.client.post(
            f"{self.url}?next=/",
            {'meal_type': 'lunch', 'recipe': self.recipe.pk},
            follow=False
        )
        self.assertEqual(response.status_code,302)
    def test_planner_day_recipe_not_visible_404(self):
        self.private_user.is_private=True
        self.private_user.save()
        self.client.login(username=self.user.username, password='Password123')
        response=self.client.post(self.url,{
            'meal_type': 'lunch',
            'recipe':self.recipe.pk
        })
        self.assertEqual(response.status_code, 404)

class AddToPlannerTest(TestCase, LogInTester):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other = User.objects.get(username='@janedoe')

        self.recipe = Recipe.objects.create(
            author = self.other,
            title="Test",
            description="x",
            ingredients = "x",
            time=10,
            meal_type="lunch"
        )
        self.client.login(username="@johndoe", password="Password123")
        self.url=reverse('add_to_planner', kwargs={'recipe_pk': self.recipe.pk})
    
    def test_missing_date(self):
        response=self.client.post(self.url, {'meal_type': 'lunch'})
        self.assertEqual(response.status_code, 302)
    def test_invalid_date(self):
        response=self.client.post(self.url,{
            'date': 'not-a-date',
            'meal_type': 'lunch'
        })
        self.assertEqual(response.status_code, 302)
    
class PlannerRangeEdgeTest(TestCase, LogInTester):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username="@johndoe", password="Password123")
        self.url = reverse('planner_range')
    
    def test_invalid_recipe_value_error(self):
        response = self.client.post(self.url,{
            'date': date.today().isoformat(),
            'meal_type': 'breakfast',
            'recipe_search': 'abc'
        })
        self.assertEqual(response.status_code,302)

    def test_invalid_start_end_404(self):
        response=self.client.get(self.url,{
            'start': 'invalid',
            'end': 'invalid'
        })
        self.assertEqual(response.status_code, 404)

class IngredientsEmptyTest(TestCase, LogInTester):
    fixtures = [
        'recipes/tests/fixtures/default_user.json']
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username="@johndoe", password="Password123")

        recipe = Recipe.objects.create(
            author = self.user,
            title="Empty",
            ingredients="",
            description="x",
            time = 5, 
            meal_type="lunch"
        )
        day = PlannedDay.objects.create(user=self.user, date=date.today())
        PlannedMeal.objects.create(
            planned_day=day,
            meal_type='lunch',
            recipe=recipe
        )
        self.url = reverse('ingredients_list')
    def test_empty_ingredients_are_skipped(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
