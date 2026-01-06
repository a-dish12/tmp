from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from unittest.mock import patch

User = get_user_model()


class SurpriseMeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="testuser@example.com",
        )

        self.other_user = User.objects.create_user(
            username="othertestuser",
            password="otherpassword",
            email="othertestuser@example.com",
        )

        self.client.login(username="testuser", password="password")

        self.salad = Recipe.objects.create(
            title="Chicken Salad",
            description="Very healthy",
            ingredients="vegetables",
            time=5,
            meal_type="breakfast",
            author=self.other_user,
        )

        self.sandwich = Recipe.objects.create(
            title="Chicken Sandwich",
            description="Quick lunch",
            ingredients="chicken, bread",
            time=7,
            meal_type="lunch",
            author=self.other_user,
        )

        self.burrito = Recipe.objects.create(
            title="Burritos",
            description="Can be healthy",
            ingredients="Something new, chicken",
            time=50,
            meal_type="snack",
            author=self.other_user,
        )

        self.meatpie = Recipe.objects.create(
            title="Meat Pie",
            description="Straight from Nigeria",
            ingredients="Beef, lamb, onions, garlic",
            time=60,
            meal_type="snack",
            author=self.other_user,
        )

    # --------------------------------------------------
    # Surprise quiz form
    # --------------------------------------------------

    def test_surprise_quiz_loads(self):
        response = self.client.get(reverse("dashboard-surprise"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surprise-quiz.html")

    # --------------------------------------------------
    # Surprise recipe selection
    # --------------------------------------------------

    def test_surprise_result_redirects_to_recipe(self):
        with patch("random.choice", return_value=self.salad):
            response = self.client.get(reverse("surprise-result"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("recipe_detail", kwargs={"pk": self.salad.pk}))

    def test_surprise_filters_by_meal_type(self):
        with patch("random.choice", return_value=self.salad):
            response = self.client.get(
                reverse("surprise-result"),
                {"meal_type": ["breakfast"]},
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("recipe_detail", kwargs={"pk": self.salad.pk}))

    def test_surprise_no_results_renders_quiz(self):
        response = self.client.get(
            reverse("surprise-result"),
            {"meal_type": ["dinner"]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surprise-quiz.html")

    # --------------------------------------------------
    # Edge cases & coverage branches
    # --------------------------------------------------

    def test_surprise_queryset_none(self):
        with patch(
            "recipes.views.surprise_recipe_view.DashboardView.get_queryset",
            return_value=None,
        ):
            response = self.client.get(reverse("surprise-result"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surprise-quiz.html")

    def test_surprise_recipe_without_pk(self):
        class FakeRecipe:
            pass

        with patch(
            "recipes.views.surprise_recipe_view.DashboardView.get_queryset",
            return_value=[FakeRecipe()],
        ):
            response = self.client.get(reverse("surprise-result"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surprise-quiz.html")

    def test_surprise_exception_handled(self):
        with patch(
            "recipes.views.surprise_recipe_view.DashboardView.get_queryset",
            side_effect=Exception("Boom"),
        ):
            response = self.client.get(reverse("surprise-result"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surprise-quiz.html")

    def test_surprise_with_list_queryset(self):
        """Test when get_queryset returns iterable without .count()."""

        class SimpleList:
            def __init__(self, items):
                self.items = items

            def __iter__(self):
                return iter(self.items)

            def __len__(self):
                return len(self.items)

            def __getitem__(self, index):
                return self.items[index]

        recipe_wrapper = SimpleList([self.salad, self.sandwich])

        with patch(
            "recipes.views.surprise_recipe_view.DashboardView.get_queryset",
            return_value=recipe_wrapper,
        ), patch("random.choice", return_value=self.sandwich):
            response = self.client.get(reverse("surprise-result"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("recipe_detail", kwargs={"pk": self.sandwich.pk}),
        )
