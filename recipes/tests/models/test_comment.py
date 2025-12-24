"""Unit tests for the Comment model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import User, Recipe, Comment


class CommentModelTestCase(TestCase):
    """Unit tests for the Comment model."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        
        self.recipe = Recipe.objects.create(
            author=self.other_user,
            title="Test Recipe",
            description="A test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="lunch"
        )
        
        self.comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            text="This is a great recipe!"
        )

    def test_valid_comment(self):
        self._assert_comment_is_valid()

    def test_comment_requires_recipe(self):
        self.comment.recipe = None
        self._assert_comment_is_invalid()

    def test_comment_requires_user(self):
        self.comment.user = None
        self._assert_comment_is_invalid()

    def test_comment_requires_text(self):
        self.comment.text = ''
        self._assert_comment_is_invalid()

    def test_comment_text_can_be_long(self):
        self.comment.text = 'x' * 1000
        self._assert_comment_is_valid()

    def test_comment_string_representation(self):
        """Test the string representation of a comment."""
        expected = f"Comment by {self.user.username} on {self.recipe.title}"
        self.assertEqual(str(self.comment), expected)

    def test_recipe_can_have_multiple_comments(self):
        """Test that a recipe can have multiple comments."""
        Comment.objects.create(
            recipe=self.recipe,
            user=self.other_user,
            text="Another comment"
        )
        self.assertEqual(self.recipe.comments.count(), 2)

    def test_comment_ordering(self):
        """Test that comments are ordered by creation time."""
        comment2 = Comment.objects.create(
            recipe=self.recipe,
            user=self.other_user,
            text="Second comment"
        )
        comment3 = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            text="Third comment"
        )
        
        comments = list(self.recipe.comments.all())
        self.assertEqual(comments[0], self.comment)
        self.assertEqual(comments[1], comment2)
        self.assertEqual(comments[2], comment3)

    def _assert_comment_is_valid(self):
        try:
            self.comment.full_clean()
        except ValidationError:
            self.fail('Test comment should be valid')

    def _assert_comment_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.comment.full_clean()
