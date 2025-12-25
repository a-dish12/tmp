"""Unit tests for the CommentForm."""
from django.test import TestCase
from recipes.forms.comment_form import CommentForm
from recipes.models import User, Recipe


class CommentFormTestCase(TestCase):
    """Unit tests for the CommentForm."""

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
        
        self.form_input = {
            'text': 'This is a great recipe!'
        }

    def test_form_has_necessary_fields(self):
        form = CommentForm()
        self.assertIn('text', form.fields)

    def test_valid_comment_form(self):
        form = CommentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_text(self):
        self.form_input['text'] = ''
        form = CommentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_long_text(self):
        self.form_input['text'] = 'x' * 1000
        form = CommentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_saves_correctly(self):
        form = CommentForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.recipe = self.recipe
        comment.user = self.user
        comment.save()
        self.assertEqual(comment.text, self.form_input['text'])
        self.assertEqual(comment.recipe, self.recipe)
        self.assertEqual(comment.user, self.user)

