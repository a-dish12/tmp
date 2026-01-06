"""Tests for dashboard meal type filtering."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


class DashboardMealTypeFilteringTests(TestCase):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username='@johndoe', password='Password123')

        self.other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123',
        )

        self.breakfast_recipe = Recipe.objects.create(
            author=self.other_user,
            title='Banana Pancakes',
            description='Fluffy banana pancakes',
            ingredients='banana\nflour\neggs',
            time=20,
            meal_type='breakfast',
        )

        self.lunch_recipe = Recipe.objects.create(
            author=self.other_user,
            title='Pesto Pasta',
            description='Pasta with fresh pesto',
            ingredients='pasta\nbasil\ngarlic\nparmesan',
            time=30,
            meal_type='lunch',
        )

        self.url = reverse('dashboard')

    def test_filter_by_breakfast(self):
        response = self.client.get(self.url, {'meal_type': 'breakfast'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Banana Pancakes')
        self.assertNotContains(response, 'Pesto Pasta')

    def test_filter_by_lunch(self):
        response = self.client.get(self.url, {'meal_type': 'lunch'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pesto Pasta')
        self.assertNotContains(response, 'Banana Pancakes')

    def test_filter_with_no_results_shows_empty_message(self):
        response = self.client.get(self.url, {'meal_type': 'dinner'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No recipes of the requested meal type are available from other users yet."
        )

    def test_no_recipes_at_all_shows_default_message(self):
        Recipe.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No recipes available from other users yet."
        )
