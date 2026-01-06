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
        """A correctly constructed comment should be valid."""
        try:
            self.comment.full_clean()
        except ValidationError:
            self.fail("Test comment should be valid")

    def test_comment_requires_recipe(self):
        """A comment must be linked to a recipe."""
        self.comment.recipe = None
        with self.assertRaises(ValidationError):
            self.comment.full_clean()

    def test_comment_requires_user(self):
        """A comment must have a user."""
        self.comment.user = None
        with self.assertRaises(ValidationError):
            self.comment.full_clean()

    def test_comment_requires_text(self):
        """A comment must contain text."""
        self.comment.text = ''
        with self.assertRaises(ValidationError):
            self.comment.full_clean()

    def test_comment_text_can_be_long(self):
        """Long comment text should be allowed."""
        self.comment.text = 'x' * 1000
        try:
            self.comment.full_clean()
        except ValidationError:
            self.fail("Long comment text should be valid")

    def test_comment_string_representation(self):
        """Test the string representation of a comment."""
        expected = f"Comment by {self.user.username} on {self.recipe.title}"
        self.assertEqual(str(self.comment), expected)

    def test_recipe_can_have_multiple_comments(self):
        """A recipe can have multiple comments."""
        Comment.objects.create(
            recipe=self.recipe,
            user=self.other_user,
            text="Another comment"
        )
        self.assertEqual(self.recipe.comments.count(), 2)

    def test_comment_ordering(self):
        """Comments should be ordered by creation time."""
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
        self.assertEqual(comments, [self.comment, comment2, comment3])

    def test_is_reply_false_for_root_comment(self):
        """Root comments should not be replies."""
        self.assertFalse(self.comment.is_reply())

    def test_is_reply_true_for_child_comment(self):
        """Child comments should be recognised as replies."""
        reply = Comment.objects.create(
            recipe=self.recipe,
            user=self.other_user,
            text="Reply comment",
            parent=self.comment
        )
        self.assertTrue(reply.is_reply())

    def test_get_depth_for_root_comment(self):
        """Root comments should have depth 0."""
        self.assertEqual(self.comment.get_depth(), 0)

    def test_get_depth_for_single_reply(self):
        """Direct replies should have depth 1."""
        reply = Comment.objects.create(
            recipe=self.recipe,
            user=self.other_user,
            text="Reply",
            parent=self.comment
        )
        self.assertEqual(reply.get_depth(), 1)

    def test_get_depth_for_nested_reply(self):
        """Replies to replies should increase depth correctly."""
        reply = Comment.objects.create(
            recipe=self.recipe,
            user=self.other_user,
            text="Reply",
            parent=self.comment
        )
        reply2 = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            text="Reply to reply",
            parent=reply
        )
        self.assertEqual(reply2.get_depth(), 2)

    def test_comment_is_hidden_default_false(self):
        """Comments should not be hidden by default."""
        self.assertFalse(self.comment.is_hidden)

    def test_comment_can_be_hidden(self):
        """Comments can be marked as hidden."""
        self.comment.is_hidden = True
        self.comment.save()
