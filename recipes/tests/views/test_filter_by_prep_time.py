"""Tests for dashboard preparation time filtering."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


class DashboardTimeFilteringTests(TestCase):

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')

        self.other_user = User.objects.get(username='@janedoe')
        self.url = reverse('dashboard')

        for time in [20, 45, 60, 90, 120]:
            Recipe.objects.create(
                title='Test Recipe',
                description='Testing recipe',
                ingredients='Eggs',
                time=time,
                meal_type='breakfast',
                author=self.other_user,
            )

    def test_new_style_filter_under_20(self):
        response = self.client.get(self.url, {'time_filter': 'under_20'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 1)
        self.assertContains(response, 'Prep time: 20 minutes')

    def test_legacy_filter_0_to_20(self):
        response = self.client.get(self.url, {'min_time': 0, 'max_time': 20})

        self.assertEqual(response.context_data['recipes'].count(), 1)
        self.assertContains(response, 'Prep time: 20 minutes')

    def test_legacy_filter_0_to_45(self):
        response = self.client.get(self.url, {'min_time': 0, 'max_time': 45})

        self.assertEqual(response.context_data['recipes'].count(), 2)
        self.assertContains(response, 'Prep time: 20 minutes')
        self.assertContains(response, 'Prep time: 45 minutes')

    def test_legacy_filter_0_to_60(self):
        response = self.client.get(self.url, {'min_time': 0, 'max_time': 60})

        self.assertEqual(response.context_data['recipes'].count(), 3)
        self.assertContains(response, 'Prep time: 60 minutes')

    def test_filter_over_90(self):
        response = self.client.get(self.url, {'min_time': 90, 'max_time': 1000})

        self.assertEqual(response.context_data['recipes'].count(), 2)
        self.assertContains(response, 'Prep time: 90 minutes')
        self.assertContains(response, 'Prep time: 120 minutes')

    def test_all_times_returned(self):
        response = self.client.get(self.url)

        self.assertEqual(response.context_data['recipes'].count(), 5)

    def test_no_results_shows_empty_message(self):
        Recipe.objects.filter(time__range=[0, 20]).delete()

        response = self.client.get(self.url, {'min_time': 0, 'max_time': 20})

        self.assertEqual(response.context_data['recipes'].count(), 0)
        self.assertContains(response, 'No recipes available from other users yet.')
