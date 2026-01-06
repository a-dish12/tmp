"""Tests for notification-related views."""

from django.test import TestCase
from django.urls import reverse

from recipes.models import User, Notification


class NotificationViewsTestCase(TestCase):
    """Tests for notification list, dropdown, and update actions."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')

        self.list_url = reverse('notifications_list')
        self.dropdown_url = reverse('notifications_dropdown')
        self.mark_all_url = reverse('mark_all_notifications_read')

        # Create notifications for pagination and unread counts
        for i in range(30):
            Notification.objects.create(
                recipient=self.user,
                title=f'Notif {i}',
                message='Hello world',
                is_read=(i % 2 == 0),
                action_url='',
            )

        self.other_user_notification = Notification.objects.create(
            recipient=self.other_user,
            title='Other user notification',
            message='Not yours',
            is_read=False,
            action_url='',
        )

    # --------------------
    # Notifications list
    # --------------------

    def test_notifications_list_requires_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('log_in'), response['Location'])

    def test_notifications_list_loads_for_logged_in_user(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('notifications', response.context)
        self.assertIn('page_obj', response.context)

        expected_unread = self.user.notifications.filter(is_read=False).count()
        self.assertEqual(response.context['unread_count'], expected_unread)

    def test_notifications_list_invalid_page_uses_last_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.list_url, {'page': 999})

        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.number, page_obj.paginator.num_pages)

    # --------------------
    # Notifications dropdown
    # --------------------

    def test_notifications_dropdown_requires_login(self):
        response = self.client.get(self.dropdown_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('log_in'), response['Location'])

    def test_notifications_dropdown_returns_json(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.dropdown_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = response.json()
        self.assertIn('notifications', data)
        self.assertIn('unread_count', data)

        self.assertLessEqual(len(data['notifications']), 10)

        expected_unread = self.user.notifications.filter(is_read=False).count()
        self.assertEqual(data['unread_count'], expected_unread)

        if data['notifications']:
            notification = data['notifications'][0]
            self.assertIn('id', notification)
            self.assertIn('title', notification)
            self.assertIn('message', notification)
            self.assertIn('is_read', notification)
            self.assertIn('created_at', notification)
            self.assertIn('action_url', notification)

    # --------------------
    # Mark single notification
    # --------------------

    def test_mark_notification_read_marks_and_redirects_to_list(self):
        self.client.login(username=self.user.username, password='Password123')
        notification = self.user.notifications.filter(is_read=False).first()

        url = reverse(
            'mark_notification_read',
            kwargs={'notification_id': notification.id},
        )
        response = self.client.get(url)

        self.assertRedirects(response, self.list_url)

        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_notification_read_redirects_to_action_url(self):
        self.client.login(username=self.user.username, password='Password123')

        notification = Notification.objects.create(
            recipient=self.user,
            title='Action notification',
            message='Click through',
            is_read=False,
            action_url=reverse('dashboard'),
        )

        url = reverse(
            'mark_notification_read',
            kwargs={'notification_id': notification.id},
        )
        response = self.client.get(url)

        self.assertRedirects(response, reverse('dashboard'))

        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_notification_read_404_for_other_users_notification(self):
        self.client.login(username=self.user.username, password='Password123')

        url = reverse(
            'mark_notification_read',
            kwargs={'notification_id': self.other_user_notification.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # --------------------
    # Mark all notifications
    # --------------------

    def test_mark_all_notifications_read_marks_all_and_redirects(self):
        self.client.login(username=self.user.username, password='Password123')

        self.assertTrue(self.user.notifications.filter(is_read=False).exists())
        response = self.client.get(self.mark_all_url)

        self.assertRedirects(response, self.list_url)
        self.assertFalse(self.user.notifications.filter(is_read=False).exists())

    def test_mark_all_notifications_read_ajax_returns_json(self):
        self.client.login(username=self.user.username, password='Password123')

        Notification.objects.create(
            recipient=self.user,
            title='Unread',
            message='Unread',
            is_read=False,
            action_url='',
        )

        response = self.client.get(
            self.mark_all_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(), {'success': True})
        self.assertFalse(self.user.notifications.filter(is_read=False).exists())
