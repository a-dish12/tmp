"""Unit tests for the PlannedMealForm."""
from django.test import TestCase
from recipes.forms.planned_meal_form import PlannedMealForm
from recipes.models import User, Recipe


class PlannedMealFormTestCase(TestCase):
    """Unit tests for the PlannedMealForm."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="lunch"
        )
        
        self.form_input = {
            'meal_type': 'breakfast',
            'recipe': self.recipe.id
        }

    def test_form_has_necessary_fields(self):
        form = PlannedMealForm(user=self.user)
        self.assertIn('meal_type', form.fields)
        self.assertIn('recipe', form.fields)

    def test_valid_planned_meal_form(self):
        form = PlannedMealForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_rejects_invalid_meal_type(self):
        self.form_input['meal_type'] = 'invalid'
        form = PlannedMealForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_accepts_breakfast(self):
        self.form_input['meal_type'] = 'breakfast'
        form = PlannedMealForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_accepts_lunch(self):
        self.form_input['meal_type'] = 'lunch'
        form = PlannedMealForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_accepts_dinner(self):
        self.form_input['meal_type'] = 'dinner'
        form = PlannedMealForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_accepts_snack(self):
        self.form_input['meal_type'] = 'snack'
        form = PlannedMealForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_requires_user_for_recipe_queryset(self):
        """Test that form requires user to filter visible recipes."""
        form = PlannedMealForm(data=self.form_input, user=self.user)
        self.assertIsNotNone(form.fields['recipe'].queryset)

    def test_form_shows_only_visible_recipes(self):
        """Test that form only shows recipes visible to the user."""
        # Create a private user with a recipe
        private_user = User.objects.get(username='@petrapickles')
        private_user.is_private = True
        private_user.save()
        
        private_recipe = Recipe.objects.create(
            author=private_user,
            title="Private Recipe",
            description="A private recipe",
            ingredients="Private ingredients",
            time=20,
            meal_type="dinner"
        )
        
        form = PlannedMealForm(user=self.other_user)
        recipe_ids = list(form.fields['recipe'].queryset.values_list('id', flat=True))
        
        # Private recipe should not be visible to other_user
        self.assertNotIn(private_recipe.id, recipe_ids)
