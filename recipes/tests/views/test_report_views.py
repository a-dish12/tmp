"""Tests for report views."""

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

from recipes.models import User, Recipe, Comment, Report, Notification


class ReportViewTestBase(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.admin = User.objects.create_superuser(
            username='@admin',
            email='admin@test.com',
            password='Password123'
        )

    def _post(self, url, reason='spam', description='test'):
        return self.client.post(url, {
            'reason': reason,
            'description': description
        })

    def _assert_message_contains(self, response, text):
        messages = list(response.wsgi_request._messages)
        self.assertTrue(
            any(text.lower() in str(m).lower() for m in messages),
            f"Expected message containing '{text}', got {[str(m) for m in messages]}"
        )


class ReportRecipeViewTestCase(ReportViewTestBase):

    def setUp(self):
        super().setUp()
        self.recipe = Recipe.objects.create(
            author=self.user2,
            title='Recipe',
            description='Desc',
            ingredients='x',
            time=10,
            meal_type='lunch'
        )
        self.url = reverse('report_recipe', kwargs={'recipe_pk': self.recipe.pk})

    def test_requires_login(self):
        response = self._post(self.url)
        self.assertIn('/log_in/', response.url)

    def test_get_form_branch(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_content.html')

    def test_creates_report_and_notification(self):
        self.client.login(username='@johndoe', password='Password123')
        self._post(self.url)
        self.assertEqual(Report.objects.count(), 1)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user,
                notification_type='report_received'
            ).exists()
        )

    def test_auto_hide_recipe_and_notify_author(self):
        reporters = [
            self.user,
            User.objects.get(username='@petrapickles'),
            User.objects.get(username='@peterpickles'),
            User.objects.create_user(username='@fourth', email='fourth@test.com', password='Password123'),
            User.objects.create_user(username='@fifth', email='fifth@test.com', password='Password123'),
        ]

        for u in reporters:
            self.client.login(username=u.username, password='Password123')
            self._post(self.url)

        self.recipe.refresh_from_db()
        self.assertTrue(self.recipe.is_hidden)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.recipe.author,
                notification_type='content_removed'
            ).exists()
        )

    def test_invalid_form_with_field_errors(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, {'reason': '', 'description': ''})
        self.assertEqual(response.status_code, 200)
        self._assert_message_contains(response, 'please provide')

    def test_cannot_report_own_recipe(self):
        self.client.login(username='@janedoe', password='Password123')
        response = self._post(self.url)
        self.assertEqual(Report.objects.count(), 0)
        self._assert_message_contains(response, 'own recipe')

    def test_staff_cannot_report(self):
        self.client.login(username='@admin', password='Password123')
        response = self._post(self.url)
        self.assertEqual(Report.objects.count(), 0)
        self._assert_message_contains(response, 'staff')

    def test_cannot_report_twice(self):
        self.client.login(username='@johndoe', password='Password123')
        self._post(self.url)
        response = self._post(self.url)
        self.assertEqual(Report.objects.count(), 1)
        self._assert_message_contains(response, 'already')

    def test_auto_hide_already_hidden_recipe(self):
        self.recipe.is_hidden = True
        self.recipe.save()

        reporters = [
            self.user,
            User.objects.get(username='@petrapickles'),
            User.objects.get(username='@peterpickles'),
            User.objects.create_user(username='@user6', email='u6@test.com', password='Password123'),
            User.objects.create_user(username='@user7', email='u7@test.com', password='Password123'),
        ]

        initial_notification_count = Notification.objects.filter(
            notification_type='content_removed'
        ).count()

        for user in reporters:
            self.client.login(username=user.username, password='Password123')
            self._post(self.url)
            self.client.logout()

        final_notification_count = Notification.objects.filter(
            notification_type='content_removed'
        ).count()
        
        self.assertEqual(initial_notification_count, final_notification_count)

    @patch('recipes.forms.report_form.ReportForm.is_valid')
    def test_form_field_errors_trigger_fallback_message(self, mock_is_valid):
        mock_is_valid.return_value = False
        
        self.client.login(username='@johndoe', password='Password123')
        
        with patch('recipes.forms.report_form.ReportForm.non_field_errors') as mock_non_field:
            mock_non_field.return_value = []
            
            response = self.client.post(self.url, {
                'reason': 'spam',
                'description': 'test'
            })
            
            self.assertEqual(response.status_code, 200)
            self._assert_message_contains(response, 'correct the errors')


class ReportCommentViewTestCase(ReportViewTestBase):

    def setUp(self):
        super().setUp()
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Recipe',
            description='Desc',
            ingredients='x',
            time=10,
            meal_type='lunch'
        )
        self.comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user2,
            text='Bad comment'
        )
        self.url = reverse('report_comment', kwargs={'comment_pk': self.comment.pk})

    def test_requires_login(self):
        response = self._post(self.url)
        self.assertIn('/log_in/', response.url)

    def test_get_form_branch(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_content.html')

    def test_creates_report_and_notification(self):
        self.client.login(username='@johndoe', password='Password123')
        self._post(self.url)
        self.assertEqual(Report.objects.count(), 1)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user,
                notification_type='report_received'
            ).exists()
        )

    def test_auto_hide_comment_and_notify_author(self):
        reporters = [
            self.user,
            User.objects.get(username='@petrapickles'),
            User.objects.get(username='@peterpickles'),
        ]

        for u in reporters:
            self.client.login(username=u.username, password='Password123')
            self._post(self.url)

        self.comment.refresh_from_db()
        self.assertTrue(self.comment.is_hidden)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.comment.user,
                notification_type='content_removed'
            ).exists()
        )

    def test_invalid_form_with_field_errors(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, {'reason': '', 'description': ''})
        self.assertEqual(response.status_code, 200)
        self._assert_message_contains(response, 'please provide')

    def test_cannot_report_own_comment(self):
        self.client.login(username='@janedoe', password='Password123')
        response = self._post(self.url)
        self.assertEqual(Report.objects.count(), 0)
        self._assert_message_contains(response, 'own comment')

    def test_staff_cannot_report_comment(self):
        self.client.login(username='@admin', password='Password123')
        response = self._post(self.url)
        self.assertEqual(Report.objects.count(), 0)
        self._assert_message_contains(response, 'staff')

    def test_cannot_report_comment_twice(self):
        self.client.login(username='@johndoe', password='Password123')
        self._post(self.url)
        self.assertEqual(Report.objects.count(), 1)
        response = self._post(self.url)
        self.assertEqual(Report.objects.count(), 1)
        self._assert_message_contains(response, 'already')

    def test_auto_hide_already_hidden_comment(self):
        self.comment.is_hidden = True
        self.comment.save()

        reporters = [
            self.user,
            User.objects.get(username='@petrapickles'),
            User.objects.get(username='@peterpickles'),
        ]

        initial_notification_count = Notification.objects.filter(
            notification_type='content_removed'
        ).count()

        for user in reporters:
            self.client.login(username=user.username, password='Password123')
            self._post(self.url)
            self.client.logout()

        final_notification_count = Notification.objects.filter(
            notification_type='content_removed'
        ).count()
        
        self.assertEqual(initial_notification_count, final_notification_count)

    @patch('recipes.forms.report_form.ReportForm.is_valid')
    def test_comment_form_field_errors_trigger_fallback_message(self, mock_is_valid):
        mock_is_valid.return_value = False
        
        self.client.login(username='@johndoe', password='Password123')
        
        with patch('recipes.forms.report_form.ReportForm.non_field_errors') as mock_non_field:
            mock_non_field.return_value = []
            
            response = self.client.post(self.url, {
                'reason': 'spam',
                'description': 'test'
            })
            
            self.assertEqual(response.status_code, 200)
            self._assert_message_contains(response, 'correct the errors')