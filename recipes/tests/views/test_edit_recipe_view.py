"""Tests for editing and deleting recipes."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


class EditRecipeViewTestCase(TestCase):
    """Tests for editing a recipe."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="editor1",
            password="password1234",
            email="editor@test.com",
        )
        self.client.login(username="editor1", password="password1234")

        self.recipe = Recipe.objects.create(
            title="Edit me",
            description="Desc",
            ingredients="Flour",
            instructions="Mix",
            time=10,
            meal_type="lunch",
            author=self.user,
        )

        self.url = reverse("edit_recipe", kwargs={"pk": self.recipe.pk})

    def test_edit_recipe_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_edit_updates_recipe(self):
        self.client.post(
            self.url,
            {
                "title": "Updated",
                "description": "Updated",
                "ingredient_count": 1,
                "ingredient_0": "Sugar",
                "instruction_count": 1,
                "instruction_0": "Bake",
                "time": 20,
                "meal_types": ["dinner"],
            },
            follow=True,
        )

        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Updated")
        self.assertEqual(self.recipe.time, 20)

    def test_invalid_form_rerenders_page(self):
        response = self.client.post(
            self.url,
            {
                "title": "",
                "description": "Updated",
                "ingredient_count": 1,
                "ingredient_0": "Sugar",
                "instruction_count": 1,
                "instruction_0": "Bake",
                "time": 20,
                "meal_types": ["dinner"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_add_ingredient_branch_sets_skip_validation(self):
        response = self.client.post(
            self.url,
            {"add_ingredient": "1", "ingredient_count": 1, "instruction_count": 1},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))

    def test_add_instruction_branch_sets_skip_validation(self):
        response = self.client.post(
            self.url,
            {"add_instruction": "1", "ingredient_count": 1, "instruction_count": 1},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))

    def test_remove_ingredient_branch_sets_skip_validation(self):
        response = self.client.post(
            self.url,
            {"remove_ingredient": "1", "ingredient_count": 2, "instruction_count": 1},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))

    def test_remove_instruction_branch_sets_skip_validation(self):
        response = self.client.post(
            self.url,
            {"remove_instruction": "1", "ingredient_count": 1, "instruction_count": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))


class EditRecipePermissionTestCase(TestCase):
    """Tests for edit permissions."""

    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            email="author@test.com",
            password="Password123",
        )
        self.other = User.objects.create_user(
            username="other",
            email="other@test.com",
            password="Password1234",
        )

        self.recipe = Recipe.objects.create(
            title="Protected",
            description="Desc",
            ingredients="Eggs",
            instructions="Cook",
            time=10,
            meal_type="lunch",
            author=self.author,
        )

        self.url = reverse("edit_recipe", kwargs={"pk": self.recipe.pk})

    def test_non_author_cannot_edit_recipe(self):
        self.client.login(username="other", password="Password1234")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class EditRecipeMinimumFieldsTestCase(TestCase):
    """Tests minimum ingredient and instruction constraints."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="editor2",
            password="password123",
            email="editor2@test.com",
        )
        self.client.login(username="editor2", password="password123")

        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test",
            ingredients="Flour",
            time=10,
            meal_type="lunch",
            author=self.user,
        )

        self.url = reverse("edit_recipe", kwargs={"pk": self.recipe.pk})

    def test_cannot_remove_ingredient_below_one(self):
        response = self.client.post(
            self.url,
            {"remove_ingredient": "1", "ingredient_count": 1, "instruction_count": 1},
        )

        self.assertTrue(response.context.get("skip_validation"))
        self.assertEqual(int(response.context["form"].data["ingredient_count"]), 1)

    def test_cannot_remove_instruction_below_one(self):
        response = self.client.post(
            self.url,
            {"remove_instruction": "1", "ingredient_count": 1, "instruction_count": 1},
        )

        self.assertTrue(response.context.get("skip_validation"))
        self.assertEqual(int(response.context["form"].data["instruction_count"]), 1)


class DeleteRecipeViewTestCase(TestCase):
    """Tests for deleting recipes."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="deleter",
            password="password123",
            email="deleter@test.com",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="password123",
            email="other@test.com",
        )

        self.recipe = Recipe.objects.create(
            title="Delete Me",
            description="Test",
            ingredients="Test",
            time=10,
            meal_type="lunch",
            author=self.user,
        )

        self.url = reverse("delete_recipe", kwargs={"pk": self.recipe.pk})

    def test_delete_recipe_page_loads(self):
        self.client.login(username="deleter", password="password123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_recipe.html")

    def test_author_can_delete_recipe(self):
        self.client.login(username="deleter", password="password123")
        response = self.client.post(self.url)

        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())
        self.assertEqual(response.status_code, 302)

    def test_non_author_cannot_delete_recipe(self):
        self.client.login(username="other", password="password123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())
