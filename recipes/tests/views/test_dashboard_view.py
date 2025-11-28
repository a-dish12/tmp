"""Tests for the profile view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from recipes.forms import RecipeForm
from recipes.models import Recipe
from recipes.tests.helpers import reverse_with_next

class DashboardViewTest(TestCase):

    def setUp(self):
        self.url = reverse('dashboard')

    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/')