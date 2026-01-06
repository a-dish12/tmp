"""Tests for the home view."""

from django.test import TestCase
from django.urls import reverse
from recipes.models import User


class HomeViewTestCase(TestCase):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='@johndoe')

    def test_home_url(self):
        self.assertEqual(self.url, '/')

    def test_home_page_renders_for_anonymous_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_logged_in_user_is_redirected_to_dashboard(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            reverse('dashboard'),
        )
