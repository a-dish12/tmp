from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class SurpriseMeTests(TestCase):
    

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password = "password",
            email="testuser@example.com",
        )   
    
        self.other_user = User.objects.create_user(
            username="othertestuser",
            password = "otherpassword",
            email="othertestuser@example.com",
        )


        self.client.login(username="testuser", password="password")
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
            meal_type="snack",
            author=self.other_user
        )
        self.meatpie = Recipe.objects.create(
            title="Meat Pie",
            description="Straight from Nigeria extremely lovely",
            ingredients="Beef,lamb, onions, garlic, carrots, peas, thyme, curry powder, salt, pepper",
            time=60,
            meal_type="snack",
            author=self.other_user
        )

    def test_surprise_me_recipe(self):
        response = self.client.get(reverse("dashboard-surprise"))

        self.assertEqual(response.status_code, 302)
        possible_ids = [
            str(self.salad.pk),
            str(self.sandwich.pk),
            str(self.burrito.pk),
            str(self.meatpie.pk),
            
        ]
        self.assertTrue(
            any(recipe_id in response.url for recipe_id in possible_ids)
        )