from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Logged-in user 
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        # Create recipe owned by logged-in user (will be excluded)
        Recipe.objects.create(
            title="Pasta",
            description="Great pasta",
            ingredients="someething something",
            time=10,
            meal_type="lunch",
            author=self.user
        )

        # Create a second user with a UNIQUE email
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com", 
            password="password"
        )

        # Recipe from another user (should appear)
        self.salad = Recipe.objects.create(
            title="Chicken Salad",
            description="Very healthy",
            ingredients="vegetables",
            time=5,
            meal_type="breakfast",
            author=self.other_user
        )
        self.sandwich = Recipe.objects.create(
            title="Chicken Sandwich",
            description="Quick lunch",
            ingredients="chicken, bread",
            time=7,
            meal_type="lunch",
            author=self.other_user
        )
        self.burrito = Recipe.objects.create(
            title="Burritos",
            description="Can be healthy as long as not eaten too much",
            ingredients="Something new, chicken, ",
            time=50,
            meal_type="Snack",
            author=self.other_user
        )
        self.meatpie = Recipe.objects.create(
            title="Meat Pie",
            description="Straight from Nigeria extremely lovely",
            ingredients="Beef,lamb, onions, garlic, carrots, peas, thyme, curry powder, salt, pepper",
            time=60,
            meal_type="Snack",
            author=self.other_user
        )



#for exact searches
    def test_dashboard_search_exact(self):
        """
        The dashboard search should return recipes from *other*
          usersthat match
        the search term, while excluding the logged-in 
        user's own recipes
        """
        response = self.client.get(
            reverse('dashboard'),
            {'search': 'Chicken Salad'}
        )

        self.assertEqual(response.status_code, 200)

        # Should appear (belongs to other user)
        self.assertContains(response, "Chicken Salad")

        # Should NOT appear (belongs to logged-in user)
        self.assertNotContains(response, "Pasta")

    #partial search
    def test_dashboard_search_partial(self):
        """Search should match titles even when full name isn't typed"""
        response = self.client.get(
            reverse('dashboard'),
            {'search': 'Chicken'}
        )
        self.assertEqual(response.status_code, 200)

        # Should appear (belongs to other user)
        self.assertContains(response, "Chicken Salad")
        self.assertContains(response, "Chicken Sandwich")

        # Should NOT appear (belongs to logged-in user)
        self.assertNotContains(response, "Pasta")


    #no search provided
    def test_dashboard_search_empty(self):
        """Search should match all titles as nothing is typed"""
        response = self.client.get(
            reverse('dashboard')
        )
        self.assertEqual(response.status_code, 200)

        # Should appear (belongs to other user)
        self.assertContains(response, "Chicken Salad")
        self.assertContains(response, "Chicken Sandwich")

        # Should NOT appear (belongs to logged-in user)
        self.assertNotContains(response, "Pasta")

    #Search with no matches
    def test_dashboard_search_partial(self):
        """Search should match no titles as title doesn't exist"""
        response = self.client.get(
            reverse('dashboard'),
            {'search': 'xyz'}
        )
        self.assertEqual(response.status_code, 200)

        # No matching recipes
        self.assertNotContains(response, "Chicken Salad")
        self.assertNotContains(response, "Chicken Sandwich")
        self.assertNotContains(response, "Pasta")