from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

class DashboardFilteringTests(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json'
    ]
    
    def setUp(self):
        """Set up test user and log in."""
        User = get_user_model()
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username='@johndoe', password='Password123')
        
        # Create another user who will be the author of recipes
        self.other_user = User.objects.create_user(
            username='@janedoe',
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            password='Password123'
        )
        
        # Create test recipes by the other user
        self.breakfast_recipe = Recipe.objects.create(
            author=self.other_user,
            title='Banana Pancakes',
            description='Fluffy banana pancakes',
            ingredients='banana\nflour\neggs',
            time=20,
            meal_type='breakfast'
        )
        
        self.lunch_recipe = Recipe.objects.create(
            author=self.other_user,
            title='Pesto Pasta',
            description='Pasta with fresh pesto',
            ingredients='pasta\nbasil\ngarlic\nparmesan',
            time=30,
            meal_type='lunch'
        )
    
    def test_filter_by_breakfast(self):
        """Filter should return only breakfast recipes."""
        response = self.client.get(reverse('dashboard'), {'meal_type': 'breakfast'})
        self.assertEqual(response.status_code, 200)

        # Should contain breakfast recipe
        self.assertContains(response, 'Banana Pancakes')

        # Should NOT contain lunch recipe
        self.assertNotContains(response, 'Pesto Pasta')

    def test_filter_by_lunch(self):
        """Filter should return only lunch recipes."""
        response = self.client.get(reverse('dashboard'), {'meal_type': 'lunch'})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Pesto Pasta')
        self.assertNotContains(response, 'Banana Pancakes')

    def test_filter_by_meal_type_with_no_results(self):
        """If no recipes match the filter, show the custom empty message."""
        response = self.client.get(reverse('dashboard'), {'meal_type': 'dinner'})
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "No recipes of the requested meal type are available from other users yet."
        )

    def test_no_recipes_at_all_shows_default_message(self):
        """If no recipes exist at all, show the default message."""
        Recipe.objects.all().delete()  # remove the seeded recipes

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No recipes available from other users yet.")