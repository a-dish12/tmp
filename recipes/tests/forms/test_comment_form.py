"""Unit tests for the CommentForm."""

from django.test import TestCase

from recipes.forms.comment_form import CommentForm
from recipes.models import User, Recipe


class CommentFormTestCase(TestCase):
    """Unit tests for the CommentForm."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

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

        self.valid_data = {
            'text': 'This is a great recipe!'
        }

    def test_form_has_text_field(self):
        form = CommentForm()
        self.assertIn('text', form.fields)

    def test_valid_comment_form(self):
        form = CommentForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_text(self):
        form = CommentForm(data={'text': ''})
        self.assertFalse(form.is_valid())

    def test_form_accepts_long_text(self):
        form = CommentForm(data={'text': 'x' * 1000})
        self.assertTrue(form.is_valid())

    def test_form_saves_comment_correctly(self):
        form = CommentForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        comment = form.save(commit=False)
        comment.recipe = self.recipe
        comment.user = self.user
        comment.save()

        self.assertEqual(comment.text, self.valid_data['text'])
        self.assertEqual(comment.recipe, self.recipe)
        self.assertEqual(comment.user, self.user)
