from django.test import TestCase
from recipes.models import Recipe, User


class RecipeDietTypeInferenceTestCase(TestCase):
    """Tests for Recipe diet type inference from ingredients."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

    def test_vegan_recipe_with_no_animal_products(self):
        """Test that recipe with no meat/dairy is classified as vegan."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Vegan Pasta',
            description='Delicious vegan pasta',
            ingredients='tomato\nbasil\nolive oil\ngarlic\npasta',
            time=30,
            meal_type='lunch'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEGAN)

    def test_vegetarian_recipe_with_dairy(self):
        """Test that recipe with dairy is classified as vegetarian."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Cheese Pizza',
            description='Classic pizza',
            ingredients='flour\ncheese\ntomato\nbasil',
            time=30,
            meal_type='dinner'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEG)

    def test_vegetarian_recipe_with_milk(self):
        """Test that recipe with milk is classified as vegetarian."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Milk Shake',
            description='Yummy shake',
            ingredients='milk\nbanana\nsugar',
            time=5,
            meal_type='snack'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEG)

    def test_vegetarian_recipe_with_butter(self):
        """Test that recipe with butter is classified as vegetarian."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Butter Toast',
            description='Simple toast',
            ingredients='bread\nbutter\nsalt',
            time=5,
            meal_type='breakfast'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEG)

    def test_vegetarian_recipe_with_honey(self):
        """Test that recipe with honey is classified as vegetarian."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Honey Oats',
            description='Healthy breakfast',
            ingredients='oats\nhoney\nwater',
            time=10,
            meal_type='breakfast'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEG)

    def test_non_veg_recipe_with_chicken(self):
        """Test that recipe with chicken is classified as non-vegetarian."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Chicken Curry',
            description='Spicy curry',
            ingredients='chicken\ntomato\nonion\nspices',
            time=45,
            meal_type='dinner'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_NON_VEG)

    def test_non_veg_recipe_with_eggs(self):
        """Test that recipe with eggs is classified as non-vegetarian."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Scrambled Eggs',
            description='Quick breakfast',
            ingredients='eggs\nbutter\nsalt\npepper',
            time=10,
            meal_type='breakfast'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_NON_VEG)

    def test_non_veg_recipe_with_fish(self):
        """Test that recipe with fish is classified as non-vegetarian."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Grilled Fish',
            description='Healthy fish',
            ingredients='fish\nlemon\nherbs\noil',
            time=25,
            meal_type='lunch'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_NON_VEG)

    def test_non_veg_recipe_with_beef(self):
        """Test that recipe with beef is classified as non-vegetarian."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Beef Steak',
            description='Juicy steak',
            ingredients='beef\nsalt\npepper\nbutter',
            time=30,
            meal_type='dinner'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_NON_VEG)

    def test_case_insensitive_detection(self):
        """Test that diet type detection is case-insensitive."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='CHICKEN Salad',
            description='Mixed salad',
            ingredients='CHICKEN\nlettuce\ntomato',
            time=20,
            meal_type='lunch'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_NON_VEG)

    def test_meat_keyword_in_middle_of_word(self):
        """Test that meat keywords are detected even within words."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Chicken Noodles',
            description='Asian noodles',
            ingredients='chicken breast\nnoodles\nsoy sauce',
            time=25,
            meal_type='dinner'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_NON_VEG)

    def test_multiple_animal_products_returns_non_veg(self):
        """Test recipe with both meat and dairy is still non-veg."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Chicken Alfredo',
            description='Creamy pasta',
            ingredients='chicken\npasta\ncream\ncheese\ngarlic',
            time=35,
            meal_type='dinner'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_NON_VEG)

    def test_diet_type_display_method_vegan(self):
        """Test get_diet_type_display for vegan recipe."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Vegan Salad',
            description='Fresh salad',
            ingredients='lettuce\ntomato\navocado',
            time=10,
            meal_type='lunch'
        )
        self.assertEqual(recipe.get_diet_type_display(), 'Vegan')

    def test_diet_type_display_method_vegetarian(self):
        """Test get_diet_type_display for vegetarian recipe."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Cheese Sandwich',
            description='Simple sandwich',
            ingredients='bread\ncheese\nbutter',
            time=5,
            meal_type='snack'
        )
        self.assertEqual(recipe.get_diet_type_display(), 'Vegetarian')

    def test_diet_type_display_method_non_veg(self):
        """Test get_diet_type_display for non-veg recipe."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Egg Omelette',
            description='Classic omelette',
            ingredients='eggs\nsalt\npepper\noil',
            time=10,
            meal_type='breakfast'
        )
        self.assertEqual(recipe.get_diet_type_display(), 'Non-Vegetarian')
