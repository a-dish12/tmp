from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from unittest.mock import patch

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

    def test_surprise_quiz_loads(self):
        response = self.client.get(reverse("dashboard-surprise"))

        self.assertEqual(response.status_code, 200)
    
    def test_surprise_result_redirects_to_recipe(self):
        response=self.client.get(reverse("surprise-result"))
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith("/recipes/"))

    def test_surprise_filters_by_meal_type(self):
        response = self.client.get(reverse("surprise-result"),
                                   {"meal_type": ["breakfast"]})
        self.assertIn(f"/recipes/{self.salad.pk}/", response.url)
    
    def test_surprise_no_results_redirects_dashboard(self):
        response = self.client.get(reverse("surprise-result"),
                                   {"meal_type": ["dinner"]})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surprise-quiz.html")

    def test_surprise_queryset_none(self):
        with patch(
            "recipes.views.surprise_recipe_view.DashboardView.get_queryset",
            return_vale=None
        ):
            response = self.client.get(reverse("surprise-result"))
            self.assertEqual(response.status_code,200)
            self.assertTemplateUsed(response, "surprise-quiz.html")
        
    def test_surprise_recipe_without_pk(self):
        class FakeRecipe:
            pass
        with patch(
            "recipes.views.surprise_recipe_view.DashboardView.get_queryset",
            return_value=[FakeRecipe()]
        ):
            response = self.client.get(reverse("surprise-result"))
            self.assertEqual(response.status_code,200)
            self.assertTemplateUsed(response, "surprise-quiz.html")
    
    def test_surprise_exception_handled(self):
         with patch(
            "recipes.views.surprise_recipe_view.DashboardView.get_queryset",
            side_effect=Exception("Boom")
        ):
            response = self.client.get(reverse("surprise-result"))
            self.assertEqual(response.status_code,200)
            self.assertTemplateUsed(response, "surprise-quiz.html")
       
