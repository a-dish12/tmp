"""Unit tests for Recipe model with instructions and image fields."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.utils import timezone
from recipes.models import User, Recipe, Rating


class RecipeInstructionsAndImageTestCase(TestCase):
    """Unit tests for Recipe instructions and image fields."""
    
    fixtures = [
        'recipes/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="lunch"
        )

    def test_recipe_without_instructions_is_valid(self):
        """Test that instructions field is optional."""
        self.recipe.instructions = ""
        self._assert_recipe_is_valid()

    def test_recipe_with_instructions_is_valid(self):
        """Test that recipe can have instructions."""
        self.recipe.instructions = "1. Step one\n2. Step two\n3. Step three"
        self._assert_recipe_is_valid()

    def test_recipe_instructions_can_be_long(self):
        """Test that instructions can be lengthy."""
        self.recipe.instructions = "Step " * 200
        self._assert_recipe_is_valid()

    def test_recipe_without_image_is_valid(self):
        """Test that image fields are optional."""
        self.recipe.image = None
        self.recipe.image_url = None
        self._assert_recipe_is_valid()

    def test_recipe_with_image_url_is_valid(self):
        """Test that recipe can have an image URL."""
        self.recipe.image_url = "https://example.com/image.jpg"
        self._assert_recipe_is_valid()

    def test_recipe_image_url_must_be_valid_url(self):
        """Test that image_url must be a valid URL."""
        self.recipe.image_url = "not a valid url"
        self._assert_recipe_is_invalid()

    def test_get_image_url_returns_image_url_when_no_upload(self):
        """Test that get_image_url returns URL when no image uploaded."""
        self.recipe.image_url = "https://example.com/image.jpg"
        self.recipe.image = None
        self.assertEqual(self.recipe.get_image_url(), "https://example.com/image.jpg")

    def test_get_image_url_returns_none_when_no_image(self):
        """Test that get_image_url returns None when no image provided."""
        self.recipe.image = None
        self.recipe.image_url = None
        self.assertIsNone(self.recipe.get_image_url())

    def _assert_recipe_is_valid(self):
        try:
            self.recipe.full_clean()
        except ValidationError:
            self.fail('Test recipe should be valid')

    def _assert_recipe_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()


class RecipeModelCoverageTestCase(TestCase):
    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123'
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Coverage Recipe",
            description="Test",
            ingredients="milk\nbread\nbutter",
            time=10,
            meal_type="lunch"
        )

    def test_average_rating_no_ratings(self):
        self.assertEqual(self.recipe.average_rating(), 0)

    def test_rating_count_no_ratings(self):
        self.assertEqual(self.recipe.rating_count(), 0)

    def test_rating_count_with_ratings(self):
        Rating.objects.create(recipe=self.recipe, user=self.other_user, stars=4)
        self.assertEqual(self.recipe.rating_count(), 1)

    def test_user_can_rate_anonymous(self):
        self.assertFalse(self.recipe.user_can_rate(AnonymousUser()))

    def test_user_can_rate_author(self):
        self.assertFalse(self.recipe.user_can_rate(self.user))

    def test_user_can_rate_other_user(self):
        self.assertTrue(self.recipe.user_can_rate(self.other_user))

    def test_get_user_rating_no_argument(self):
        self.assertIsNone(self.recipe.get_user_rating())

    def test_get_user_rating_anonymous_user(self):
        """Test get_user_rating with anonymous user."""
        self.assertIsNone(self.recipe.get_user_rating(AnonymousUser()))

    def test_get_user_rating_no_rating_for_user(self):
        self.assertIsNone(self.recipe.get_user_rating(self.other_user))

    def test_get_user_rating_existing(self):
        Rating.objects.create(recipe=self.recipe, user=self.other_user, stars=5)
        self.assertEqual(self.recipe.get_user_rating(self.other_user), 5)

    def test_get_user_rating_exception_handling(self):
        """Test get_user_rating handles exceptions (line 76)."""
        # Create a rating
        Rating.objects.create(recipe=self.recipe, user=self.other_user, stars=4)
        
        # Delete all ratings to cause DoesNotExist
        Rating.objects.all().delete()
        
        # Should return None instead of raising exception
        result = self.recipe.get_user_rating(self.other_user)
        self.assertIsNone(result)

    def test_get_diet_type_display_vegetarian(self):
        self.assertEqual(self.recipe.get_diet_type_display(), "Vegetarian")

    def test_get_image_url_with_uploaded_image(self):
        image = SimpleUploadedFile(
            "test.jpg",
            b"imagecontent",
            content_type="image/jpeg"
        )
        self.recipe.image = image
        self.recipe.save()
        self.assertIsNotNone(self.recipe.get_image_url())

    def test_get_ingredients_list_with_ingredients(self):
        """Test get_ingredients_list returns proper list."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="List Test",
            description="Test",
            ingredients="flour\nsugar\neggs",
            time=20,
            meal_type="dessert"
        )
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(len(ingredients), 3)
        self.assertIn("flour", ingredients)
        self.assertIn("sugar", ingredients)
        self.assertIn("eggs", ingredients)

    def test_get_ingredients_list_empty(self):
        """Test get_ingredients_list with empty ingredients (line 145)."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="Empty Ingredients",
            description="Test",
            ingredients="",
            time=20,
            meal_type="lunch"
        )
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(ingredients, [])

    def test_get_ingredients_list_with_empty_lines(self):
        """Test get_ingredients_list filters out empty lines."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="Whitespace Test",
            description="Test",
            ingredients="flour\n\nsugar\n  \neggs",
            time=20,
            meal_type="dessert"
        )
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(len(ingredients), 3)

    def test_get_instructions_list_with_instructions(self):
        """Test get_instructions_list returns proper list."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="Instructions Test",
            description="Test",
            ingredients="flour",
            instructions="Mix ingredients\nBake at 350F\nLet cool",
            time=45,
            meal_type="dessert"
        )
        instructions = recipe.get_instructions_list()
        self.assertEqual(len(instructions), 3)
        self.assertIn("Mix ingredients", instructions)

    def test_get_instructions_list_empty(self):
        """Test get_instructions_list with empty instructions (line 151)."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="No Instructions",
            description="Test",
            ingredients="flour",
            instructions="",
            time=20,
            meal_type="lunch"
        )
        instructions = recipe.get_instructions_list()
        self.assertEqual(instructions, [])

    def test_get_meal_types_list_single_type(self):
        """Test get_meal_types_list with single meal type."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="Single Type",
            description="Test",
            ingredients="flour",
            time=20,
            meal_type="lunch"
        )
        meal_types = recipe.get_meal_types_list()
        self.assertEqual(len(meal_types), 1)
        self.assertIn("lunch", meal_types)

    def test_get_meal_types_list_multiple_types(self):
        """Test get_meal_types_list with multiple meal types."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="Multiple Types",
            description="Test",
            ingredients="flour",
            time=20,
            meal_type="breakfast,lunch,dinner"
        )
        meal_types = recipe.get_meal_types_list()
        self.assertEqual(len(meal_types), 3)
        self.assertIn("breakfast", meal_types)
        self.assertIn("lunch", meal_types)
        self.assertIn("dinner", meal_types)

    def test_get_meal_types_list_empty(self):
        """Test get_meal_types_list with empty meal_type (line 156)."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="No Meal Type",
            description="Test",
            ingredients="flour",
            time=20,
            meal_type=""
        )
        meal_types = recipe.get_meal_types_list()
        self.assertEqual(meal_types, [])

    def test_get_meal_types_display_single_type(self):
        """Test get_meal_types_display with single type."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="Display Test",
            description="Test",
            ingredients="flour",
            time=20,
            meal_type="lunch"
        )
        display = recipe.get_meal_types_display()
        self.assertEqual(display, "Lunch")

    def test_get_meal_types_display_multiple_types(self):
        """Test get_meal_types_display with multiple types."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="Multiple Display",
            description="Test",
            ingredients="flour",
            time=20,
            meal_type="breakfast,snack"
        )
        display = recipe.get_meal_types_display()
        self.assertEqual(display, "Breakfast, Snack")

    def test_get_meal_types_display_empty(self):
        """Test get_meal_types_display with empty meal_type (lines 162-166)."""
        recipe = Recipe.objects.create(
            author=self.user,
            title="Empty Display",
            description="Test",
            ingredients="flour",
            time=20,
            meal_type=""
        )
        display = recipe.get_meal_types_display()
        self.assertEqual(display, "Not specified")


class RecipeViewTrackingTestCase(TestCase):
    """Test view tracking functionality."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="Test description",
            ingredients="flour, water",
            time=30,
            meal_type="lunch"
        )
        cache.clear()

    def tearDown(self):
        """Clear cache after each test."""
        cache.clear()

    def test_add_viewer_increments_total_views(self):
        """Test that adding a viewer increments total views."""
        initial_views = self.recipe.total_views
        self.recipe.add_viewer(user_id=1)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.total_views, initial_views + 1)

    def test_same_viewer_only_counts_once(self):
        """Test that the same viewer viewing again doesn't increment views."""
        self.recipe.add_viewer(user_id=1)
        self.recipe.refresh_from_db()
        initial_views = self.recipe.total_views
        
        self.recipe.add_viewer(user_id=1)
        self.recipe.refresh_from_db()
        
        self.assertEqual(self.recipe.total_views, initial_views)

    def test_get_active_viewers_returns_count(self):
        """Test that get_active_viewers returns correct count."""
        self.assertEqual(self.recipe.get_active_viewers(), 0)
        
        self.recipe.add_viewer(user_id=1)
        self.assertEqual(self.recipe.get_active_viewers(), 1)

    def test_get_popularity_score_with_ratings_and_views(self):
        """Test popularity score combining ratings and views."""
        other_user = User.objects.create_user(
            username='@other',
            email='other@example.com',
            password='Password123'
        )
        Rating.objects.create(recipe=self.recipe, user=other_user, stars=5)
        self.recipe.total_views = 50
        self.recipe.save()
        
        score = self.recipe.get_popularity_score()
        # (5 * 1) + (50 * 0.1) = 10
        self.assertEqual(score, 10.0)

    def test_vegan_recipe_explicit_coverage(self):
        """Explicitly test vegan path for branch coverage (line 101)."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Pure Vegan',
            description='Vegan recipe',
            ingredients='lettuce\ntomato\ncucumber\nolive oil',  # No meat, no dairy, no honey
            time=15,
            meal_type='lunch'
        )
        # Should hit line 101 (return DIET_VEGAN)
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEGAN)
        self.assertEqual(recipe.get_diet_type_display(), 'Vegan')

    def test_recipe_with_only_dairy_no_meat(self):
        """Test recipe with dairy but no meat (line 97 True branch)."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Dairy Only',
            description='Vegetarian with dairy',
            ingredients='tomato\nbasil\nyogurt',  # Has dairy, no meat
            time=20,
            meal_type='snack'
        )
        # Should hit line 97 (return DIET_VEG)
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEG)

    def test_recipe_with_ghee(self):
        """Test recipe with ghee (dairy keyword)."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Ghee Recipe',
            description='With ghee',
            ingredients='rice\nghee\nsalt',
            time=25,
            meal_type='dinner'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEG)

    def test_recipe_with_cream(self):
        """Test recipe with cream (dairy keyword)."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Creamy Soup',
            description='With cream',
            ingredients='potato\ncream\nsalt\npepper',
            time=30,
            meal_type='dinner'
        )
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEG)

    def test_empty_ingredients_returns_vegan(self):
        """Test that empty ingredients defaults to vegan."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='No Ingredients',
            description='Test',
            ingredients='',
            time=10,
            meal_type='snack'
        )
        # Empty ingredients should return vegan (line 101)
        self.assertEqual(recipe.get_diet_type(), Recipe.DIET_VEGAN)