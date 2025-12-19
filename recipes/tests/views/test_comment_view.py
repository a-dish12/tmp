"""Tests for comment views."""
from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Comment
from recipes.tests.helpers import LogInTester


class AddCommentViewTestCase(TestCase, LogInTester):
    """Tests for the add comment view."""

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
        
        self.url = reverse('add_comment', kwargs={'recipe_pk': self.recipe.pk})
        self.redirect_url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_add_comment_url(self):
        self.assertEqual(self.url, f'/recipes/{self.recipe.pk}/comments/add/')

    def test_add_comment_redirects_when_not_logged_in(self):
        """Test that non-authenticated users are redirected to login."""
        response = self.client.post(self.url, {'text': 'Great recipe!'}, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_comment_creation(self):
        """Test that a user can successfully add a comment."""
        self.client.login(username=self.user.username, password='Password123')
        comment_text = 'This is a great recipe!'
        
        response = self.client.post(self.url, {'text': comment_text}, follow=True)
        
        self.assertTrue(Comment.objects.filter(recipe=self.recipe, user=self.user, text=comment_text).exists())
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)

    def test_add_comment_requires_text(self):
        """Test that comment requires text field."""
        self.client.login(username=self.user.username, password='Password123')
        before_count = Comment.objects.count()
        
        response = self.client.post(self.url, {'text': ''}, follow=True)
        
        self.assertEqual(Comment.objects.count(), before_count)

    def test_user_can_comment_on_own_recipe(self):
        """Test that users can comment on their own recipes."""
        self.client.login(username=self.other_user.username, password='Password123')
        
        response = self.client.post(self.url, {'text': 'My own comment'}, follow=True)
        
        self.assertTrue(Comment.objects.filter(recipe=self.recipe, user=self.other_user).exists())

    def test_multiple_comments_on_same_recipe(self):
        """Test that multiple users can comment on the same recipe."""
        Comment.objects.create(recipe=self.recipe, user=self.other_user, text='First comment')
        
        self.client.login(username=self.user.username, password='Password123')
        self.client.post(self.url, {'text': 'Second comment'})
        
        self.assertEqual(Comment.objects.filter(recipe=self.recipe).count(), 2)


class AddReplyViewTestCase(TestCase, LogInTester):
    """Tests for the add reply view."""

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
            text='Original comment'
        )
        
        self.url = reverse('add_reply', kwargs={'comment_pk': self.comment.pk})
        self.redirect_url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_add_reply_url(self):
        self.assertEqual(self.url, f'/comments/{self.comment.pk}/reply/')

    def test_add_reply_redirects_when_not_logged_in(self):
        """Test that non-authenticated users are redirected to login."""
        response = self.client.post(self.url, {'text': 'Reply'}, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_reply_creation(self):
        """Test that a user can successfully add a reply."""
        self.client.login(username=self.other_user.username, password='Password123')
        reply_text = 'Thanks for the comment!'
        
        response = self.client.post(self.url, {'text': reply_text}, follow=True)
        
        self.assertTrue(Comment.objects.filter(
            recipe=self.recipe,
            user=self.other_user,
            text=reply_text,
            parent=self.comment
        ).exists())
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)

    def test_reply_has_correct_parent(self):
        """Test that reply is correctly linked to parent comment."""
        self.client.login(username=self.other_user.username, password='Password123')
        
        self.client.post(self.url, {'text': 'Reply'})
        
        reply = Comment.objects.get(text='Reply')
        self.assertEqual(reply.parent, self.comment)
        self.assertTrue(reply.is_reply())

    def test_nested_replies(self):
        """Test that replies can be nested."""
        self.client.login(username=self.other_user.username, password='Password123')
        
        # First level reply
        self.client.post(self.url, {'text': 'First reply'})
        first_reply = Comment.objects.get(text='First reply')
        
        # Second level reply
        reply_to_reply_url = reverse('add_reply', kwargs={'comment_pk': first_reply.pk})
        self.client.post(reply_to_reply_url, {'text': 'Reply to reply'})
        
        second_reply = Comment.objects.get(text='Reply to reply')
        self.assertEqual(second_reply.parent, first_reply)
        self.assertEqual(second_reply.get_depth(), 2)


class DeleteCommentViewTestCase(TestCase, LogInTester):
    """Tests for the delete comment view."""

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
            text='Test comment'
        )
        
        self.url = reverse('delete_comment', kwargs={'comment_pk': self.comment.pk})
        self.redirect_url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_delete_comment_url(self):
        self.assertEqual(self.url, f'/comments/{self.comment.pk}/delete/')

    def test_delete_comment_redirects_when_not_logged_in(self):
        """Test that non-authenticated users are redirected to login."""
        response = self.client.post(self.url, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_comment_deletion(self):
        """Test that a user can delete their own comment."""
        self.client.login(username=self.user.username, password='Password123')
        comment_id = self.comment.pk
        
        response = self.client.post(self.url, follow=True)
        
        self.assertFalse(Comment.objects.filter(pk=comment_id).exists())
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)

    def test_cannot_delete_other_users_comment(self):
        """Test that users cannot delete comments by other users."""
        self.client.login(username=self.other_user.username, password='Password123')
        comment_id = self.comment.pk
        
        response = self.client.post(self.url, follow=True)
        
        self.assertTrue(Comment.objects.filter(pk=comment_id).exists())

    def test_deleting_comment_deletes_replies(self):
        """Test that deleting a comment also deletes its replies."""
        reply = Comment.objects.create(
            recipe=self.recipe,
            user=self.other_user,
            text='Reply',
            parent=self.comment
        )
        
        self.client.login(username=self.user.username, password='Password123')
        self.client.post(self.url)
        
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())
        self.assertFalse(Comment.objects.filter(pk=reply.pk).exists())


class RecipeDetailViewCommentsDisplayTestCase(TestCase):
    """Tests for comment display in recipe detail view."""

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
        
        self.url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_recipe_detail_shows_comment_count(self):
        """Test that recipe detail page displays comment count."""
        Comment.objects.create(recipe=self.recipe, user=self.user, text='Comment 1')
        Comment.objects.create(recipe=self.recipe, user=self.other_user, text='Comment 2')
        
        response = self.client.get(self.url)
        
        self.assertContains(response, '2')

    def test_recipe_detail_shows_comments(self):
        """Test that recipe detail page displays comments."""
        comment = Comment.objects.create(recipe=self.recipe, user=self.user, text='Great recipe!')
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Great recipe!')
        self.assertContains(response, self.user.username)

    def test_recipe_detail_shows_nested_replies(self):
        """Test that recipe detail page displays nested replies."""
        parent = Comment.objects.create(recipe=self.recipe, user=self.user, text='Parent comment')
        reply = Comment.objects.create(recipe=self.recipe, user=self.other_user, text='Reply', parent=parent)
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Parent comment')
        self.assertContains(response, 'Reply')

    def test_recipe_detail_shows_comment_form_when_logged_in(self):
        """Test that comment form is shown to logged-in users."""
        self.client.login(username=self.user.username, password='Password123')
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Post Comment')
