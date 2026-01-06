"""Tests for notification model and views."""
from django.test import TestCase, Client
from django.urls import reverse

from recipes.models import User, Recipe, Notification


class NotificationModelTestCase(TestCase):
    """Test cases for Notification model."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            description='Test',
            ingredients='flour',
            instructions='Bake',
            time=30,
            meal_type='lunch'
        )

    def _create_user(self, username):
        return User.objects.create_user(
            username=username,
            email=f'{username[1:]}@test.com',
            password='Password123',
            first_name='Test',
            last_name='User'
        )

    def test_create_report_received_notification(self):
        notification = Notification.create_report_received_notification(self.user)

        self.assertEqual(notification.recipient, self.user)
        self.assertEqual(notification.notification_type, 'report_received')
        self.assertIn('Report', notification.title)
        self.assertFalse(notification.is_read)

    def test_create_report_resolved_notification_hidden(self):
        notification = Notification.create_report_resolved_notification(
            self.user, 'hidden', 'Test Recipe'
        )
        self.assertIn('removed', notification.message)

    def test_create_report_resolved_notification_deleted(self):
        notification = Notification.create_report_resolved_notification(
            self.user, 'deleted', 'Test Recipe'
        )
        self.assertIn('removed', notification.message)

    def test_create_report_resolved_notification_dismissed(self):
        notification = Notification.create_report_resolved_notification(
            self.user, 'dismissed', 'Test Recipe'
        )
        self.assertIn('no violation', notification.message)
        self.assertNotIn('removed', notification.message)

    def test_create_report_resolved_notification_other_action(self):
        notification = Notification.create_report_resolved_notification(
            self.user, 'warned', 'Test Recipe'
        )
        self.assertIn('appropriate action', notification.message)

    def test_create_content_removed_notification(self):
        notification = Notification.create_content_removed_notification(
            self.user, 'recipe', 'Test Recipe', 'Spam'
        )
        self.assertEqual(notification.notification_type, 'content_removed')
        self.assertIn('removed', notification.title.lower())

    def test_create_warning_notification(self):
        notification = Notification.create_warning_notification(
            self.user, 'Spam'
        )
        self.assertEqual(notification.notification_type, 'warning_issued')
        self.assertIn('warning', notification.title.lower())

    def test_notification_str_representation(self):
        notification = Notification.objects.create(
            recipient=self.user,
            notification_type='report_received',
            title='Test Notification',
            message='Test message'
        )
        self.assertEqual(
            str(notification),
            f"Test Notification - {self.user.username}"
        )

    def test_notification_ordering(self):
        notif1 = Notification.objects.create(
            recipient=self.user,
            notification_type='report_received',
            title='First',
            message='First'
        )
        notif2 = Notification.objects.create(
            recipient=self.user,
            notification_type='warning_issued',
            title='Second',
            message='Second'
        )

        self.assertEqual(list(Notification.objects.all()), [notif2, notif1])

    def test_create_follow_request_notification(self):
        requester = self._create_user('@requester')
        notification = Notification.create_follow_request_notification(requester, self.user)

        self.assertEqual(notification.notification_type, 'follow_request')
        self.assertIn(requester.username, notification.message)
        self.assertIsNotNone(notification.action_url)
        self.assertFalse(notification.is_read)

    def test_create_rating_notification(self):
        rater = self._create_user('@rater')
        notification = Notification.create_rating_notification(rater, self.recipe, 5)

        self.assertEqual(notification.notification_type, 'recipe_rated')
        self.assertIn('5 stars', notification.message)
        self.assertIsNotNone(notification.action_url)

    def test_create_rating_notification_singular_star(self):
        rater = self._create_user('@rater2')
        notification = Notification.create_rating_notification(rater, self.recipe, 1)

        self.assertIn('1 star', notification.message)
        self.assertNotIn('1 stars', notification.message)

    def test_create_comment_notification(self):
        commenter = self._create_user('@commenter')
        notification = Notification.create_comment_notification(commenter, self.recipe)

        self.assertEqual(notification.notification_type, 'comment_reply')
        self.assertIn(commenter.username, notification.message)
        self.assertIsNotNone(notification.action_url)


class NotificationViewTestCase(TestCase):
    """Test cases for notification views."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')

        self.notification1 = Notification.objects.create(
            recipient=self.user,
            notification_type='report_received',
            title='Report Received',
            message='Your content was reported'
        )
        self.notification2 = Notification.objects.create(
            recipient=self.user,
            notification_type='warning_issued',
            title='Warning',
            message='You received a warning',
            is_read=True
        )

    def test_notifications_list_requires_login(self):
        response = self.client.get(reverse('notifications_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_notifications_list_shows_notifications(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('notifications_list'))

        self.assertContains(response, 'Report Received')
        self.assertContains(response, 'Warning')

    def test_mark_notification_read(self):
        self.client.login(username='@johndoe', password='Password123')
        self.client.get(
            reverse('mark_notification_read', kwargs={'notification_id': self.notification1.id})
        )

        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)

    def test_mark_all_notifications_read(self):
        self.client.login(username='@johndoe', password='Password123')
        self.client.post(reverse('mark_all_notifications_read'))

        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
        self.assertTrue(self.notification2.is_read)

    def test_notifications_dropdown_ajax(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(
            reverse('notifications_dropdown'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        data = response.json()
        self.assertEqual(len(data['notifications']), 2)
        self.assertEqual(data['unread_count'], 1)

    def test_unread_count_decreases_after_marking_read(self):
        self.client.login(username='@johndoe', password='Password123')
        self.assertEqual(self.user.unread_notifications_count(), 1)

        self.client.get(
            reverse('mark_notification_read', kwargs={'notification_id': self.notification1.id})
        )

        self.assertEqual(self.user.unread_notifications_count(), 0)

    def test_cannot_mark_other_users_notification_read(self):
        other_user = User.objects.create_user(
            username='@otheruser',
            email='other@test.com',
            password='Password123'
        )
        other_notification = Notification.objects.create(
            recipient=other_user,
            notification_type='report_received',
            title='Other Notification',
            message='Test'
        )

        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(
            reverse('mark_notification_read', kwargs={'notification_id': other_notification.id})
        )

        self.assertEqual(response.status_code, 404)
