"""Tests for UserRecipesView."""
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from recipes.views.user_recipes_view import UserRecipesView

User = get_user_model()


class UserRecipesViewTest(TestCase):
    """Test suite for UserRecipesView."""
    
    fixtures = ['recipes/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123',
            first_name='Jane',
            last_name='Doe'
        )
        
        # Create recipes for the logged-in user
        self.recipe1 = Recipe.objects.create(
            author=self.user,
            title='User Recipe 1',
            description='Test',
            ingredients='flour',
            time=30,
            meal_type='lunch'
        )
        self.recipe2 = Recipe.objects.create(
            author=self.user,
            title='User Recipe 2',
            description='Test',
            ingredients='sugar',
            time=20,
            meal_type='dessert'
        )
        
        # Create recipe for other user (should not appear)
        self.other_recipe = Recipe.objects.create(
            author=self.other_user,
            title='Other User Recipe',
            description='Test',
            ingredients='salt',
            time=15,
            meal_type='snack'
        )
    
    def test_get_queryset_returns_only_user_recipes(self):
        """Test that get_queryset returns only logged-in user's recipes (line 13)."""
        request = self.factory.get('/user-recipes/')
        request.user = self.user
        
        view = UserRecipesView()
        view.request = request
        
        queryset = view.get_queryset()
        
        # Check that user's recipes are in queryset
        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.recipe1, queryset)
        self.assertIn(self.recipe2, queryset)
        
        # Check that other user's recipe is NOT in queryset
        self.assertNotIn(self.other_recipe, queryset)
    
    def test_get_queryset_empty_when_user_has_no_recipes(self):
        """Test queryset is empty when user has no recipes."""
        request = self.factory.get('/user-recipes/')
        request.user = self.other_user
        
        # Delete the other user's recipe
        Recipe.objects.filter(author=self.other_user).delete()
        
        view = UserRecipesView()
        view.request = request
        
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 0)