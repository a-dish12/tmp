"""Tests for the log out view."""

from django.test import TestCase
from django.urls import reverse

from recipes.models import User
from recipes.tests.test_helpers import LogInTester


class LogOutViewTestCase(TestCase, LogInTester):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.get(username='@johndoe')

    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')

    def test_logged_in_user_is_logged_out_and_redirected(self):
        self.client.login(username='@johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())

        response = self.client.get(self.url)

        self.assertFalse(self._is_logged_in())
        self.assertRedirects(response, reverse('home'))

    def test_anonymous_user_is_redirected_to_home(self):
        response = self.client.get(self.url)

        self.assertFalse(self._is_logged_in())
        self.assertRedirects(response, reverse('home'))
