from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import User, Recipe


class DashboardSortingTestCase(TestCase):
    """Tests for dashboard sorting behaviour."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')

        self.other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123'
        )

        # Older recipe (created first)
        self.quick_recipe = Recipe.objects.create(
            author=self.other_user,
            title="Quick Recipe",
            description="Fast recipe",
            ingredients="flour",
            time=10,
            meal_type="lunch"
        )

        # Newer recipe (created after)
        self.most_viewed_recipe = Recipe.objects.create(
            author=self.other_user,
            title="Most Viewed Recipe",
            description="Popular recipe",
            ingredients="water",
            time=20,
            meal_type="dinner"
        )

    def test_sort_by_newest(self):
        """
        Recipes should be ordered by creation date descending.
        Assert relative ordering rather than fixed index.
        """
        self.client.login(username='@johndoe', password='Password123')

        response = self.client.get(
            reverse('dashboard'),
            {'sort': 'newest'}
        )

        recipes = list(response.context['recipes'])

        # Both recipes must be present
        self.assertIn(self.quick_recipe, recipes)
        self.assertIn(self.most_viewed_recipe, recipes)

        # Newer recipe must appear before older recipe
        self.assertLess(
            recipes.index(self.most_viewed_recipe),
            recipes.index(self.quick_recipe)
        )

    def test_sort_by_time(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('dashboard'), {'sort': 'time'})
        recipes = list(response.context['recipes'])
        self.assertEqual(recipes[0], self.quick_recipe)

    def test_sort_by_most_viewed(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('dashboard'), {'sort': 'most_viewed'})
        recipes = list(response.context['recipes'])
        self.assertIn(self.quick_recipe, recipes)
        self.assertIn(self.most_viewed_recipe, recipes)
