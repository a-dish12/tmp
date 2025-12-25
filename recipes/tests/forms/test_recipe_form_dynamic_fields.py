"""Tests for recipe form with dynamic ingredient and instruction fields."""
from django.test import TestCase
from recipes.forms.recipe_form import RecipeForm
from recipes.models import User, Recipe


class RecipeFormDynamicFieldsTestCase(TestCase):
    """Test cases for dynamic ingredient and instruction fields."""
    
    fixtures = ['recipes/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'title': 'Test Recipe',
            'description': 'A test recipe',
            'ingredient_count': 3,
            'ingredient_0': '2 cups flour',
            'ingredient_1': '1 cup sugar',
            'ingredient_2': '3 eggs',
            'instruction_count': 3,
            'instruction_0': 'Mix ingredients',
            'instruction_1': 'Bake at 350°F',
            'instruction_2': 'Let cool',
            'time': 30,
            'meal_types': ['lunch']
        }
    
    def test_form_has_ingredient_count_field(self):
        """Test that form has ingredient_count field."""
        form = RecipeForm()
        self.assertIn('ingredient_count', form.fields)
    
    def test_form_has_instruction_count_field(self):
        """Test that form has instruction_count field."""
        form = RecipeForm()
        self.assertIn('instruction_count', form.fields)
    
    def test_form_accepts_multiple_ingredients(self):
        """Test form accepts multiple ingredient fields."""
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(len(ingredients), 3)
        self.assertIn('2 cups flour', ingredients)
        self.assertIn('1 cup sugar', ingredients)
        self.assertIn('3 eggs', ingredients)
    
    def test_form_accepts_multiple_instructions(self):
        """Test form accepts multiple instruction fields."""
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        instructions = recipe.get_instructions_list()
        self.assertEqual(len(instructions), 3)
        self.assertIn('Mix ingredients', instructions)
        self.assertIn('Bake at 350°F', instructions)
    
    def test_form_accepts_single_ingredient(self):
        """Test form accepts a single ingredient."""
        self.form_input['ingredient_count'] = 1
        self.form_input['ingredient_0'] = '1 cup flour'
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        self.assertEqual(recipe.get_ingredients_list(), ['1 cup flour'])
    
    def test_form_accepts_single_instruction(self):
        """Test form accepts a single instruction."""
        self.form_input['instruction_count'] = 1
        self.form_input['instruction_0'] = 'Mix and bake'
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        self.assertEqual(recipe.get_instructions_list(), ['Mix and bake'])
    
    def test_form_rejects_all_empty_ingredients(self):
        """Test form rejects when all ingredients are empty."""
        self.form_input['ingredient_0'] = ''
        self.form_input['ingredient_1'] = ''
        self.form_input['ingredient_2'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('ingredient_0', form.errors)
        self.assertIn('Please add at least one ingredient.', form.errors['ingredient_0'])
    
    def test_form_rejects_all_empty_instructions(self):
        """Test form rejects when all instructions are empty."""
        self.form_input['instruction_0'] = ''
        self.form_input['instruction_1'] = ''
        self.form_input['instruction_2'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('instruction_0', form.errors)
        self.assertIn('Please add at least one instruction.', form.errors['instruction_0'])
    
    def test_form_creates_dynamic_ingredient_fields(self):
        """Test form dynamically creates ingredient fields based on count."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Existing Recipe',
            description='Test',
            ingredients='2 cups flour\n1 cup sugar',
            instructions='Mix\nBake',
            time=30,
            meal_type='lunch'
        )
        form = RecipeForm(instance=recipe)
        self.assertIn('ingredient_0', form.fields)
        self.assertIn('ingredient_1', form.fields)
        self.assertEqual(form.fields['ingredient_0'].initial, '2 cups flour')
        self.assertEqual(form.fields['ingredient_1'].initial, '1 cup sugar')
    
    def test_form_creates_dynamic_instruction_fields(self):
        """Test form dynamically creates instruction fields based on count."""
        recipe = Recipe.objects.create(
            author=self.user,
            title='Existing Recipe',
            description='Test',
            ingredients='Flour',
            instructions='Mix ingredients\nBake at 350\nCool down',
            time=30,
            meal_type='lunch'
        )
        form = RecipeForm(instance=recipe)
        self.assertIn('instruction_0', form.fields)
        self.assertIn('instruction_1', form.fields)
        self.assertIn('instruction_2', form.fields)
        self.assertEqual(form.fields['instruction_0'].initial, 'Mix ingredients')
        self.assertEqual(form.fields['instruction_1'].initial, 'Bake at 350')
        self.assertEqual(form.fields['instruction_2'].initial, 'Cool down')
    
    def test_form_initializes_single_fields_for_new_recipe(self):
        """Test form initializes with single field for new recipes."""
        form = RecipeForm()
        self.assertIn('ingredient_0', form.fields)
        self.assertIn('instruction_0', form.fields)
        self.assertEqual(form.fields['ingredient_count'].initial, 1)
        self.assertEqual(form.fields['instruction_count'].initial, 1)
    
    def test_form_skips_empty_ingredients(self):
        """Test form skips empty ingredient fields."""
        self.form_input['ingredient_1'] = ''  # Empty middle field
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(len(ingredients), 2)  # Only non-empty ones
        self.assertIn('2 cups flour', ingredients)
        self.assertIn('3 eggs', ingredients)
    
    def test_form_has_meal_types_field(self):
        """Test form has meal_types multi-select field."""
        form = RecipeForm()
        self.assertIn('meal_types', form.fields)
        self.assertEqual(form.fields['meal_types'].__class__.__name__, 'MultipleChoiceField')
    
    def test_form_accepts_multiple_meal_types(self):
        """Test form accepts multiple meal types."""
        self.form_input['meal_types'] = ['breakfast', 'lunch']
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        self.assertEqual(recipe.meal_type, 'breakfast,lunch')
        recipe.author = self.user
        recipe.save()
        # Original whitespace preserved in storage
        self.assertIn('flour', recipe.ingredients)
        self.assertIn('sugar', recipe.ingredients)
