"""Tests for comment views."""
from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Comment, Notification
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
    
    def test_comment_creates_notification_for_recipe_author(self):
        """Test that adding a comment creates a notification for the recipe author."""
        self.client.login(username=self.user.username, password='Password123')
        
        # Initially no notifications
        self.assertEqual(Notification.objects.filter(recipient=self.other_user).count(), 0)
        
        comment_text = 'Great recipe!'
        response = self.client.post(self.url, {'text': comment_text})
        
        # Check notification was created
        self.assertEqual(Notification.objects.filter(recipient=self.other_user).count(), 1)
        notification = Notification.objects.get(recipient=self.other_user)
        self.assertEqual(notification.notification_type, 'comment_reply')
        self.assertIn(self.user.username, notification.message)
        self.assertIn(self.recipe.title, notification.message)
    
    def test_comment_on_own_recipe_no_notification(self):
        """Test that commenting on your own recipe doesn't create a notification."""
        # Create recipe by the commenter
        own_recipe = Recipe.objects.create(
            author=self.user,
            title="My Recipe",
            description="My test recipe",
            ingredients="Test ingredients",
            time=30,
            meal_type="dinner"
        )
        
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('add_comment', kwargs={'recipe_pk': own_recipe.pk})
        
        # Initially no notifications
        initial_count = Notification.objects.filter(recipient=self.user).count()
        
        comment_text = 'Commenting on my own recipe!'
        response = self.client.post(url, {'text': comment_text})
        
        # Should not create notification
        self.assertEqual(Notification.objects.filter(recipient=self.user).count(), initial_count)

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

    def test_recipe_detail_shows_comment_form_when_logged_in(self):
        """Test that comment form is shown to logged-in users."""
        self.client.login(username=self.user.username, password='Password123')
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Post Comment')
