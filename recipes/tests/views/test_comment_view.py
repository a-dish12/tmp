"""Tests for comment-related views."""

from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Comment
from recipes.tests.test_helpers import LogInTester


class AddCommentViewTestCase(TestCase, LogInTester):
    """Tests for adding comments to recipes."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
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
            meal_type="lunch",
        )

        self.url = reverse('add_comment', kwargs={'recipe_pk': self.recipe.pk})
        self.redirect_url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_add_comment_url(self):
        self.assertEqual(self.url, f'/recipes/{self.recipe.pk}/comments/add/')

    def test_add_comment_redirects_when_not_logged_in(self):
        response = self.client.post(self.url, {'text': 'Nice'}, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_comment_creation(self):
        self.client.login(username=self.user.username, password='Password123')

        self.client.post(self.url, {'text': 'Great recipe!'}, follow=True)

        self.assertTrue(
            Comment.objects.filter(
                recipe=self.recipe,
                user=self.user,
                text='Great recipe!',
            ).exists()
        )

    def test_add_comment_requires_text(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Comment.objects.count()

        self.client.post(self.url, {'text': ''}, follow=True)

        self.assertEqual(Comment.objects.count(), before_count)

    def test_user_can_comment_on_own_recipe(self):
        self.client.login(username=self.other_user.username, password='Password123')

        self.client.post(self.url, {'text': 'My own comment'}, follow=True)

        self.assertTrue(
            Comment.objects.filter(recipe=self.recipe, user=self.other_user).exists()
        )

    def test_multiple_comments_on_same_recipe(self):
        Comment.objects.create(recipe=self.recipe, user=self.other_user, text='First')

        self.client.login(username=self.user.username, password='Password123')
        self.client.post(self.url, {'text': 'Second'})

        self.assertEqual(Comment.objects.filter(recipe=self.recipe).count(), 2)


class DeleteCommentViewTestCase(TestCase, LogInTester):
    """Tests for deleting comments."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
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
            meal_type="lunch",
        )

        self.comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            text='Test comment',
        )

        self.url = reverse('delete_comment', kwargs={'comment_pk': self.comment.pk})
        self.redirect_url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_delete_comment_url(self):
        self.assertEqual(self.url, f'/comments/{self.comment.pk}/delete/')

    def test_delete_comment_redirects_when_not_logged_in(self):
        response = self.client.post(self.url, follow=True)
        redirect_url = f"{reverse('log_in')}?next={self.url}"
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_user_can_delete_own_comment(self):
        self.client.login(username=self.user.username, password='Password123')

        self.client.post(self.url, follow=True)

        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_user_cannot_delete_others_comment(self):
        self.client.login(username=self.other_user.username, password='Password123')

        self.client.post(self.url, follow=True)

        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())


class RecipeDetailViewCommentsDisplayTestCase(TestCase):
    """Tests for displaying comments on the recipe detail page."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
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
            meal_type="lunch",
        )

        self.url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_recipe_detail_shows_comment_count(self):
        Comment.objects.create(recipe=self.recipe, user=self.user, text='One')
        Comment.objects.create(recipe=self.recipe, user=self.other_user, text='Two')

        response = self.client.get(self.url)

        self.assertContains(response, '2')

    def test_recipe_detail_displays_comments_and_authors(self):
        Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            text='Great recipe!',
        )

        response = self.client.get(self.url)

        self.assertContains(response, 'Great recipe!')
        self.assertContains(response, self.user.username)

    def test_comment_form_visible_to_logged_in_users(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.url)

        self.assertContains(response, 'Post Comment')
