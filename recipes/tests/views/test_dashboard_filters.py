from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Rating

User = get_user_model()


class DashboardFilterTests(TestCase):
    """Tests for dashboard filtering functionality."""
    
    def setUp(self):
        """Set up test users and login."""
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

    def _create_recipe(self, title, ingredients, time=10, meal_type="breakfast"):
        """Helper method to create recipes."""
        return Recipe.objects.create(
            title=title,
            description="Test description",
            ingredients=ingredients,
            time=time,
            meal_type=meal_type,
            author=self.other_user
        )

    # Meal Type Filter Tests
    def test_filter_by_meal_type(self):
        """Test filtering by meal type."""
        self._create_recipe("Breakfast Dish", "Eggs", meal_type="breakfast")
        
        response = self.client.get(reverse("dashboard"), {"meal_types": ["breakfast"]})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Breakfast Dish")

    def test_get_selected_meal_types_deduplication(self):
        """Test that duplicate meal types are removed."""
        self._create_recipe("Breakfast Dish", "Eggs", meal_type="breakfast")
        
        response = self.client.get(
            reverse("dashboard"),
            {"meal_types": ["breakfast", "breakfast", "lunch"]}
        )
        
        selected = response.context['selected_meal_types']
        self.assertEqual(len(selected), 2)
        self.assertIn("breakfast", selected)
        self.assertIn("lunch", selected)

    # Search Filter Tests
    def test_filter_by_search(self):
        """Test search functionality."""
        self._create_recipe("Breakfast Dish", "Eggs")
        
        response = self.client.get(reverse("dashboard"), {"search": "Eggs"})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Breakfast Dish")

    # Diet Filter Tests
    def test_filter_by_diet_vegan(self):
        """Test filtering by vegan diet."""
        self._create_recipe("Vegan Salad", "lettuce, tomato", meal_type="lunch")
        self._create_recipe("Cheese Pizza", "cheese, flour", meal_type="dinner")
        
        response = self.client.get(reverse("dashboard"), {"diet": "vegan"})
        
        self.assertContains(response, "Vegan Salad")
        self.assertNotContains(response, "Cheese Pizza")

    def test_filter_by_diet_vegetarian(self):
        """Test filtering by vegetarian diet."""
        self._create_recipe("Cheese Pasta", "pasta, cheese", time=25, meal_type="lunch")
        self._create_recipe("Chicken Curry", "chicken, tomato", time=45, meal_type="dinner")
        
        response = self.client.get(reverse("dashboard"), {"diet": "veg"})
        
        self.assertContains(response, "Cheese Pasta")
        self.assertNotContains(response, "Chicken Curry")

    def test_filter_by_diet_non_veg(self):
        """Test filtering by non-vegetarian diet."""
        self._create_recipe("Beef Steak", "beef, salt", time=30, meal_type="dinner")
        self._create_recipe("Garden Salad", "lettuce, tomato", meal_type="lunch")
        
        response = self.client.get(reverse("dashboard"), {"diet": "non_veg"})
        
        self.assertContains(response, "Beef Steak")
        self.assertNotContains(response, "Garden Salad")

    # Rating Filter Tests
    def test_filter_by_rating_4_plus(self):
        """Test filtering by 4+ star rating."""
        rater = User.objects.create_user(username="rater", email="rater@test.com", password="pass123")
        
        high_rated = self._create_recipe("Amazing Dish", "magic", time=20, meal_type="dinner")
        Rating.objects.create(recipe=high_rated, user=rater, stars=5)
        
        low_rated = self._create_recipe("Mediocre Dish", "stuff", time=15, meal_type="lunch")
        Rating.objects.create(recipe=low_rated, user=rater, stars=2)
        
        response = self.client.get(reverse("dashboard"), {"rating_filter": "4_plus"})
        
        self.assertContains(response, "Amazing Dish")
        self.assertNotContains(response, "Mediocre Dish")

    def test_filter_by_rating_3_plus(self):
        """Test filtering by 3+ star rating."""
        rater = User.objects.create_user(username="rater2", email="rater2@test.com", password="pass123")
        
        good_recipe = self._create_recipe("Good Dish", "ingredients", time=25, meal_type="dinner")
        Rating.objects.create(recipe=good_recipe, user=rater, stars=3)
        
        response = self.client.get(reverse("dashboard"), {"rating_filter": "3_plus"})
        
        self.assertContains(response, "Good Dish")

    def test_filter_by_rating_invalid_key(self):
        """Test that invalid rating filter returns all recipes."""
        self._create_recipe("Any Recipe", "test", time=20, meal_type="lunch")
        
        response = self.client.get(reverse("dashboard"), {"rating_filter": "invalid_key"})
        
        self.assertContains(response, "Any Recipe")