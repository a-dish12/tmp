"""Tests for planner views."""
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse

from recipes.models import User, Recipe, PlannedDay, PlannedMeal


class PlannerViewsTestCase(TestCase):
    """Tests for planner views."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.client.login(username='@johndoe', password='Password123')

        self.recipe = Recipe.objects.create(
            author=self.other_user,
            title="Test Recipe",
            description="Test",
            ingredients="Eggs\nMilk\nButter",
            time=30,
            meal_type="lunch"
        )

        self.today = date.today()

    def test_planner_events_no_params(self):
        response = self.client.get(reverse('planner_events'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_planner_events_with_range(self):
        end = self.today + timedelta(days=7)
        response = self.client.get(reverse('planner_events'), {'start': self.today.isoformat(), 'end': end.isoformat()})
        self.assertEqual(response.status_code, 200)

    def test_planner_events_returns_meal_data(self):
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=self.recipe)
        response = self.client.get(reverse('planner_events'), {'start': self.today.isoformat(), 'end': (self.today + timedelta(days=1)).isoformat()})
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn('title', data[0])

    def test_planner_day_get(self):
        url = reverse('planner_day', args=[self.today.isoformat()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'day.html')

    def test_planner_day_with_search(self):
        url = reverse('planner_day', args=[self.today.isoformat()])
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, 200)

    def test_planner_day_invalid_date(self):
        url = reverse('planner_day', args=['invalid-date'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_planner_day_post_valid(self):
        url = reverse('planner_day', args=[self.today.isoformat()])
        response = self.client.post(url, {'meal_type': 'lunch', 'recipe': self.recipe.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PlannedMeal.objects.filter(recipe=self.recipe, planned_day__date=self.today).exists())

    def test_planner_day_post_with_next_redirect(self):
        url = reverse('planner_day', args=[self.today.isoformat()])
        response = self.client.post(url + '?next=/dashboard/', {'meal_type': 'lunch', 'recipe': self.recipe.pk}, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_planner_day_post_invalid_form_rerenders(self):
        url = reverse('planner_day', args=[self.today.isoformat()])
        with patch('recipes.views.planner_view.PlannedMealForm', autospec=True) as MockForm:
            mock_form = MagicMock()
            mock_form.is_valid.return_value = False
            MockForm.return_value = mock_form
            response = self.client.post(url, {})
            self.assertEqual(response.status_code, 200)

    def test_planner_day_private_recipe_404(self):
        self.other_user.is_private = True
        self.other_user.save()
        url = reverse('planner_day', args=[self.today.isoformat()])
        response = self.client.post(url, {'meal_type': 'lunch', 'recipe': self.recipe.pk})
        self.assertEqual(response.status_code, 404)

    def test_add_to_planner_success(self):
        url = reverse('add_to_planner', kwargs={'recipe_pk': self.recipe.pk})
        response = self.client.post(url, {'date': self.today.isoformat(), 'meal_type': 'lunch'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PlannedMeal.objects.filter(recipe=self.recipe).exists())

    def test_add_to_planner_private_recipe_404(self):
        self.other_user.is_private = True
        self.other_user.save()
        url = reverse('add_to_planner', kwargs={'recipe_pk': self.recipe.pk})
        response = self.client.post(url, {'date': self.today.isoformat(), 'meal_type': 'lunch'})
        self.assertEqual(response.status_code, 404)

    def test_add_to_planner_missing_fields(self):
        url = reverse('add_to_planner', kwargs={'recipe_pk': self.recipe.pk})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 302)

    def test_add_to_planner_invalid_date_format(self):
        url = reverse('add_to_planner', kwargs={'recipe_pk': self.recipe.pk})
        response = self.client.post(url, {'date': 'invalid-date', 'meal_type': 'lunch'})
        self.assertEqual(response.status_code, 302)

    def test_add_to_planner_get_request(self):
        url = reverse('add_to_planner', kwargs={'recipe_pk': self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_add_to_planner_replaces_existing(self):
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        old_recipe = Recipe.objects.create(author=self.other_user, title="Old Recipe", description="Old", ingredients="Old", time=10, meal_type="breakfast")
        meal = PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=old_recipe)
        url = reverse('add_to_planner', kwargs={'recipe_pk': self.recipe.pk})
        self.client.post(url, {'date': self.today.isoformat(), 'meal_type': 'lunch'})
        meal.refresh_from_db()
        self.assertEqual(meal.recipe, self.recipe)

    def test_remove_from_planner(self):
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        meal = PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=self.recipe)
        url = reverse('remove_from_planner', kwargs={'meal_pk': meal.pk})
        self.client.post(url)
        self.assertFalse(PlannedMeal.objects.filter(pk=meal.pk).exists())

    def test_remove_from_planner_with_next_redirect(self):
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        meal = PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=self.recipe)
        url = reverse('remove_from_planner', kwargs={'meal_pk': meal.pk})
        response = self.client.get(url + '?next=/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_remove_from_planner_other_user_404(self):
        other_day = PlannedDay.objects.create(user=self.other_user, date=self.today)
        meal = PlannedMeal.objects.create(planned_day=other_day, meal_type='lunch', recipe=self.recipe)
        url = reverse('remove_from_planner', kwargs={'meal_pk': meal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_planner_range_default(self):
        response = self.client.get(reverse('planner_range'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner_range.html')

    def test_planner_range_invalid_dates_404(self):
        response = self.client.get(reverse('planner_range'), {'start': 'invalid', 'end': 'invalid'})
        self.assertEqual(response.status_code, 404)

    def test_planner_range_swaps_dates(self):
        start = self.today
        end = start - timedelta(days=3)
        response = self.client.get(reverse('planner_range'), {'start': start.isoformat(), 'end': end.isoformat()})
        self.assertEqual(response.status_code, 200)

    def test_planner_range_post_add_meal(self):
        response = self.client.post(reverse('planner_range'), {'date': self.today.isoformat(), 'meal_type': 'lunch', 'recipe_search': str(self.recipe.pk)})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PlannedMeal.objects.filter(recipe=self.recipe, planned_day__date=self.today, meal_type='lunch').exists())

    def test_planner_range_post_replace_existing_meal(self):
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        old_recipe = Recipe.objects.create(author=self.user, title="Old Recipe", description="Old", ingredients="Old", time=10, meal_type="lunch")
        PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=old_recipe)
        response = self.client.post(reverse('planner_range'), {'date': self.today.isoformat(), 'meal_type': 'lunch', 'recipe_search': str(self.recipe.pk)})
        self.assertEqual(response.status_code, 302)
        meal = PlannedMeal.objects.get(planned_day=planned_day, meal_type='lunch')
        self.assertEqual(meal.recipe, self.recipe)

    def test_planner_range_post_invalid_recipe(self):
        response = self.client.post(reverse('planner_range'), {'date': self.today.isoformat(), 'meal_type': 'lunch', 'recipe_search': '99999'})
        self.assertEqual(response.status_code, 302)

    def test_planner_range_post_invalid_recipe_value_error(self):
        response = self.client.post(reverse('planner_range'), {'date': self.today.isoformat(), 'meal_type': 'lunch', 'recipe_search': 'not-a-number'})
        self.assertEqual(response.status_code, 302)

    def test_planner_range_post_private_recipe(self):
        self.other_user.is_private = True
        self.other_user.save()
        response = self.client.post(reverse('planner_range'), {'date': self.today.isoformat(), 'meal_type': 'lunch', 'recipe_search': str(self.recipe.pk)})
        self.assertEqual(response.status_code, 302)

    def test_planner_range_post_with_range_params(self):
        start = self.today
        end = start + timedelta(days=6)
        response = self.client.post(reverse('planner_range'), {'date': self.today.isoformat(), 'meal_type': 'lunch', 'recipe_search': str(self.recipe.pk), 'start': start.isoformat(), 'end': end.isoformat()})
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'start={start.isoformat()}', response.url)
        self.assertIn(f'end={end.isoformat()}', response.url)

    def test_planner_range_post_no_range_params(self):
        response = self.client.post(reverse('planner_range'), {'date': self.today.isoformat(), 'meal_type': 'lunch', 'recipe_search': str(self.recipe.pk)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('planner_range'))

    def test_planner_range_with_multiple_meals_same_slot(self):
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        recipe2 = Recipe.objects.create(author=self.user, title="Recipe 2", description="Test", ingredients="Sugar", time=20, meal_type="lunch")
        PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=self.recipe)
        PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=recipe2)
        response = self.client.get(reverse('planner_range'), {'start': self.today.isoformat(), 'end': self.today.isoformat()})
        self.assertEqual(response.status_code, 200)

    def test_ingredients_list_default(self):
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=self.recipe)
        response = self.client.get(reverse('ingredients_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eggs")

    def test_ingredients_list_whitespace_lines(self):
        recipe = Recipe.objects.create(author=self.user, title="Whitespace", ingredients="Flour\n\n  \nSugar", description="x", time=5, meal_type="lunch")
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=recipe)
        response = self.client.get(reverse('ingredients_list'))
        self.assertContains(response, "Flour")
        self.assertContains(response, "Sugar")

    def test_ingredients_list_empty_ingredients(self):
        recipe = Recipe.objects.create(author=self.user, title="No Ingredients", ingredients="", description="x", time=5, meal_type="lunch")
        planned_day = PlannedDay.objects.create(user=self.user, date=self.today)
        PlannedMeal.objects.create(planned_day=planned_day, meal_type='lunch', recipe=recipe)
        response = self.client.get(reverse('ingredients_list'))
        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        self.client.logout()
        urls = [
            reverse('planner_events'),
            reverse('planner_day', args=[self.today.isoformat()]),
            reverse('planner_range'),
            reverse('ingredients_list'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/log_in/', response.url)