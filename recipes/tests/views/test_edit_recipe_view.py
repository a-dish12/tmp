from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class EditRecipeViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="editor1",
            password="password1234",
            email="editor@test.com"
        )
        self.client.login(username="editor1", password="password1234")

        self.recipe=Recipe.objects.create(
            title="Edit me",
            description="Desc",
            ingredients="Flour",
            instructions="Mix",
            time=10,
            meal_type="lunch",
            author=self.user
        )
    def test_edit_recipe_page_loads(self):
        response = self.client.get(
            reverse("edit_recipe", kwargs={"pk": self.recipe.pk})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_edit_recipe_post(self):
        response = self.client.post(
            reverse("edit_recipe", kwargs={"pk": self.recipe.pk}),
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
        self.assertEqual(response.status_code,200)
    
    def test_edit_recipe_invalid_form_rerenders(self):
        """Submitting an invlalid form should re-render page with errors"""
        response = self.client.post(
            reverse("edit_recipe", kwargs={"pk": self.recipe.pk}),
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
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "form")
    
    def test_edit_recipe_add_ingredient(self):
        """Clicking add ingredient increases ingredient count"""
        response = self.client.post(
            reverse("edit_recipe", kwargs={"pk": self.recipe.pk}),
            {
                "add_ingredient": "1",
                "ingredient_count": 1,
                "instruction_count": 1,

            },
        )
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.context.get("skip_validation"))
    
    def test_edit_recipe_add_instruction(self):
        """Clicking add instruction increases instruction count"""
        response = self.client.post(
            reverse("edit_recipe", kwargs={"pk": self.recipe.pk}),
            {
                "add_instruction": "1",
                "ingredient_count": 1,
                "instruction_count": 1,
            },
        )
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.context.get("skip_validation"))
    
    def test_edit_recipe_remove_ingredient(self):
        """Removing ingredient reduces count but not below 1"""
        response = self.client.post(
            reverse("edit_recipe", kwargs={"pk": self.recipe.pk}),
            {
                "remove_ingredient": "1",
                "ingredient_count": 2,
                "instruction_count": 1,
            },
        )
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.context.get("skip_validation"))
    
    def test_edit_recipe_remove_instruction(self):
        """Removing instruction reduces count but not below 1"""
        response = self.client.post(
            reverse("edit_recipe", kwargs={"pk": self.recipe.pk}),
            {
                "remove_instruction": "1",
                "ingredient_count": 1,
                "instruction_count": 2,
            },
        )
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.context.get("skip_validation"))
    

class EditRecipePermissionTest(TestCase):
    """Tests that only the author can edit a recipe"""

    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            email="author@test.com",
            password="Password123"
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
            instructions = "Cook",
            time=10,
            meal_type="lunch",
            author=self.author,
        )
    def test_non_author_cannot_edit_recipe(self):
        """If user isn't tha author should receive 403 as they shouldn't have access"""
        self.client.login(username="other", password="Password1234")
        response = self.client.get(
            reverse("edit_recipe", kwargs={"pk": self.recipe.pk})
        )
        self.assertEqual(response.status_code,403)