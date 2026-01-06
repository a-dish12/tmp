"""Tests for recipe detail views."""

from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache

from recipes.models import User, Recipe


class RecipeDetailInstructionsAndImageTestCase(TestCase):
    """Tests for conditional display of instructions and images."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            instructions="1. Step one\n2. Step two\n3. Step three",
            time=30,
            meal_type="lunch",
            image_url="https://example.com/image.jpg",
        )

        self.url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_instructions_are_displayed_when_present(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'Instructions')
        self.assertContains(response, '1. Step one')
        self.assertContains(response, '2. Step two')

    def test_instructions_section_hidden_when_empty(self):
        recipe = Recipe.objects.create(
            author=self.user,
            title="No Instructions",
            description="None",
            ingredients="Ingredients",
            time=20,
            meal_type="dinner",
        )

        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': recipe.pk})
        )

        self.assertNotContains(
            response,
            '<h5 class="card-title mt-4">Instructions</h5>',
        )

    def test_image_displayed_when_image_url_present(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'https://example.com/image.jpg')
        self.assertContains(response, '<img')

    def test_image_hidden_when_no_image_url(self):
        recipe = Recipe.objects.create(
            author=self.user,
            title="No Image",
            description="None",
            ingredients="Ingredients",
            time=15,
            meal_type="snack",
        )

        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': recipe.pk})
        )
        self.assertNotIn('<img src=', response.content.decode())

    def test_all_recipe_fields_are_displayed(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.recipe.title)
        self.assertContains(response, self.recipe.description)
        self.assertContains(response, self.recipe.ingredients)
        self.assertContains(response, self.recipe.instructions)
        self.assertContains(response, str(self.recipe.time))
        self.assertContains(response, self.recipe.meal_type.capitalize())
        self.assertContains(response, self.recipe.image_url)


class RecipeDetailViewTrackingTestCase(TestCase):
    """Tests for view tracking and viewer counts."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')

        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Tracked Recipe",
            description="Test",
            ingredients="flour",
            time=30,
            meal_type="lunch",
        )

        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_viewing_recipe_increments_views(self):
        self.client.login(username='@johndoe', password='Password123')
        initial_views = self.recipe.total_views

        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': self.recipe.pk})
        )
        self.assertEqual(response.status_code, 200)

        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.total_views, initial_views + 1)

    def test_active_viewers_in_context(self):
        self.client.login(username='@johndoe', password='Password123')

        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': self.recipe.pk})
        )

        self.assertIn('active_viewers', response.context)
        self.assertIn('total_views', response.context)

    def test_multiple_users_viewing_simultaneously(self):
        # User 1 views
        client1 = Client()
        client1.login(username='@johndoe', password='Password123')
        client1.get(reverse('recipe_detail', kwargs={'pk': self.recipe.pk}))

        # User 2 views
        other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123',
        )

        client2 = Client()
        client2.login(username='@janedoe', password='Password123')
        response = client2.get(
            reverse('recipe_detail', kwargs={'pk': self.recipe.pk})
        )

        self.assertEqual(response.context['active_viewers'], 2)
