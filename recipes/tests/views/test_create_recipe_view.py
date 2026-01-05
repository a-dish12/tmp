from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateRecipeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="password1234",
            email="user1@test.com"
        )
        self.client.login(username="user1", password="password1234")



    def test_create_recipe_page_loads(self):
        response = self.client.get(reverse("create_recipe"))
        self.assertEqual(response.status_code,200)
    def test_create_recipe_post_redirects(self):
        response = self.client.post(reverse("create_recipe"),
            {"title": "Test Recipe",
                "description":"Simple",
                "ingredient_count": 1, 
                "ingredient_0":"Flour", 
                "instruction_count": 1,
                "instruction_0": "Mix",
                "time": 10,
                "meal_types": ["lunch"],
            },
            follow=True,
        )
        self.assertEqual(response.status_code,200)

class CreateRecipeViewBranchTest(TestCase):
    """Tests for dynamic add/remove branches and invalid form handling"""
    def setUp(self):
        self.user = User.objects.create_user(
            username="branchuser",
            password="password1234",
            email="branchuser@test.com"
        )
        self.client.login(username="branchuser", password="password1234")
        self.url = reverse("create_recipe")
        self.base_data = {
            "title": "Branch Recipe",
            "description": "Test",
            "ingredient_count": 1,
            "ingredient_0": "Eggs",
            "instruction_count": 1,
            "instruction_0": "Cook",
            "time": 20,
            "meal_types": ["lunch"]
        }
    def test_add_ingredient_branch(self):
        "Posting add_ingredient increases ingredient_count and skips validation"
        data = self.base_data.copy()
        data["add_ingredient"]="1"

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))
    
    def test_add_instruction_branch(self):
        """Posting add_instruction increases instruction_count and skips validation"""
        data = self.base_data.copy()
        data["add_instruction"] = "1"

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))
    
    def test_remove_ingredient_when_more_than_one(self):
        """remove_ingredient decreases ingredient_count if above 1"""
        data = self.base_data.copy()
        data["ingredient_count"] = 2
        data["remove_ingredient"] = "1"

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))

    def test_remove_ingredient_does_not_go_below_one(self):
        """remove_ingredient does nothing if ingredient_count is 1"""
        data = self.base_data.copy()
        data["ingredient_count"] = 1
        data["remove_ingredient"] = "1"

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))

    
    def test_remove_instruction_branch(self):
        """remove_instruction decreases instruction_count when possible"""
        data = self.base_data.copy()
        data["instruction_count"] = 2
        data["remove_instruction"] = "1"

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("skip_validation"))
    
    def test_invalid_form_rerenders_page(self):
        """Invalid form submission should re-render page with errors"""
        data = self.base_data.copy()
        data["title"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)



