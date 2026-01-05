"""Test for notification views"""
from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Notification


class NotificationViewsTestCase(TestCase):
    """Test suite for notification-related views"""

    fixtures=[
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
    ]
    def setUp(self):
        """Create users and some notifications for pagination"""
        self.user = User.objects.get(username="@johndoe")
        self.other_user = User.objects.get(username="@janedoe")

        self.list_url = reverse('notifications_list')
        self.dropdown_url =reverse('notifications_dropdown')
        self.mark_all_url =reverse('mark_all_notifications_read')
        
        for i in range(30):
            Notification.objects.create(
                recipient = self.user,
                title=f"Notif {i}",
                message = "Hello world",
                is_read=(i%2==0),
                action_url=""
            )
        self.other_user_notification= Notification.objects.create(
            recipient = self.other_user,
            title="Other users notification",
            message = "Not yours",
            is_read = False,
            action_url=""
        )
    
    def test_notifications_list_redirects_when_not_logged_in(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('log_in'), response['Location'])
    

    def test_notifications_list_page_loads_when_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code,200)
        expected_unread = self.user.notifications.filter(is_read=False).count()
        self.assertEqual(response.context['unread_count'], expected_unread)
        self.assertIn('notifications', response.context)
        self.assertIn('page_obj', response.context)
    def test_notifications_list_invalid_page_param_uses_last_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.list_url, {'page':999})
        self.assertEqual(response.status_code, 200)

        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.number, page_obj.paginator.num_pages)
    
    def test_notification_dropdown_redirects_when_not_logged_in(self):
        response = self.client.get(self.dropdown_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('log_in'), response['Location'])
    
    def test_notifications_dropdown_returns_json_and_unread_count(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.dropdown_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = response.json()
        self.assertIn('notifications',data)
        self.assertIn('unread_count',data)
        
        self.assertLessEqual(len(data['notifications']), 10)

        expected_unread = self.user.notifications.filter(is_read=False).count()
        self.assertEqual(data['unread_count'], expected_unread)

        if data['notifications']:
            item = data['notifications'][0]
            self.assertIn('id', item)
            self.assertIn('title', item)
            self.assertIn('message', item)
            self.assertIn('is_read', item)
            self.assertIn('created_at', item)
            self.assertIn('action_url', item)

    def test_mark_notification_read_sets_is_read_and_redirects_to_list_when_no_action_url(self):
        self.client.login(username=self.user.username, password='Password123')
        notif = self.user.notifications.filter(is_read=False).first()
        url = reverse('mark_notification_read', kwargs={'notification_id': notif.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['Location'], reverse('notifications_list'))

        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_mark_notifications_read_redirects_to_action_url_when_present(self):
        self.client.login(username=self.user.username, password='Password123')

        notif = Notification.objects.create(
            recipient = self.user,
            title="Action notif",
            message= "Click through", 
            is_read=False,
            action_url=reverse('dashboard')
        )
        url = reverse('mark_notification_read', kwargs={'notification_id': notif.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['Location'], reverse('dashboard'))
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
    
    def test_mark_notification_read_404_for_others_users_notification(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('mark_notification_read', kwargs={'notification_id': self.other_user_notification.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_mark_all_notifications_read_marks_all_and_redirects(self):
        self.client.login(username=self.user.username, password='Password123')

        self.assertTrue(self.user.notifications.filter(is_read=False).exists())
        response = self.client.get(self.mark_all_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('notifications_list'))
        self.assertFalse(self.user.notifications.filter(is_read=False).exists())
    
    def test_mark_all_notifications_read_ajax_returns_json(self):
        self.client.login(username=self.user.username, password = 'Password123')
        Notification.objects.create(
            recipient = self.user,
            title="Unread",
            message="Unread", 
            is_read = False,
            action_url=""
        )
        response = self.client.get(self.mark_all_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(), {'success': True})

        self.assertFalse(self.user.notifications.filter(is_read=False).exists())


















