from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class DashboardFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="viewer",
            password="password1234",
            email="viewer@test.com"
        )

        self.other_user = User.objects.create_user(
            username="chef",
            password="password12345",
            email="chef@test.com"
        )
        self.client.login(username="viewer", password="password1234")

        Recipe.objects.create(
            title="Breakfast Dish",
            description="Eggs",
            ingredients="Eggs",
            instructions="Cook",
            time=10,
            meal_type="breakfast",
            author=self.other_user
        )
    def test_filter_by_meal_type(self):
        response = self.client.get(
            reverse("dashboard"),
            {"meal_types": ["breakfast"]}
        )
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Breakfast Dish")
    
    def test_filter_by_search(self):
        response=self.client.get(
            reverse("dashboard"),
            {"search": "Eggs"}
        )
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Breakfast Dish")