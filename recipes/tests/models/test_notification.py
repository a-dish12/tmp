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
    
    def test_create_report_received_notification(self):
        """Test creating a report received notification."""
        notification = Notification.create_report_received_notification(
            self.user
        )
        self.assertEqual(notification.recipient, self.user)
        self.assertEqual(notification.notification_type, 'report_received')
        self.assertIn('Report', notification.title)
        self.assertFalse(notification.is_read)
    
    def test_create_report_resolved_notification(self):
        """Test creating a report resolved notification."""
        notification = Notification.create_report_resolved_notification(
            self.user,
            'hidden',
            'Test Recipe'
        )
        self.assertEqual(notification.notification_type, 'report_resolved')
        self.assertIn('resolved', notification.title.lower())
    
    def test_create_content_removed_notification(self):
        """Test creating a content removed notification."""
        notification = Notification.create_content_removed_notification(
            self.user,
            'recipe',
            'Test Recipe',
            'Spam or Advertising'
        )
        self.assertEqual(notification.notification_type, 'content_removed')
        self.assertIn('removed', notification.title.lower())
    
    def test_create_warning_notification(self):
        """Test creating a warning notification."""
        notification = Notification.create_warning_notification(
            self.user,
            'Spam or Advertising'
        )
        self.assertEqual(notification.notification_type, 'warning_issued')
        self.assertIn('warning', notification.title.lower())
    
    def test_notification_str_representation(self):
        """Test string representation of notification."""
        notification = Notification.objects.create(
            recipient=self.user,
            notification_type='report_received',
            title='Test Notification',
            message='Test message'
        )
        self.assertIn('Test Notification', str(notification))
        self.assertIn('@johndoe', str(notification))
    
    def test_notification_ordering(self):
        """Test that notifications are ordered by created_at descending."""
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
        
        notifications = list(Notification.objects.all())
        self.assertEqual(notifications[0], notif2)
        self.assertEqual(notifications[1], notif1)


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
        """Test that notifications list requires login."""
        response = self.client.get(reverse('notifications_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)
    
    def test_notifications_list_shows_notifications(self):
        """Test that notifications list shows user's notifications."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('notifications_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Report Received')
        self.assertContains(response, 'Warning')
    
    def test_mark_notification_read(self):
        """Test marking a notification as read."""
        self.client.login(username='@johndoe', password='Password123')
        url = reverse('mark_notification_read', kwargs={'notification_id': self.notification1.id})
        response = self.client.get(url)
        
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
    
    def test_mark_all_notifications_read(self):
        """Test marking all notifications as read."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('mark_all_notifications_read'))
        
        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
        self.assertTrue(self.notification2.is_read)
    
    def test_notifications_dropdown_ajax(self):
        """Test notifications dropdown AJAX endpoint."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(
            reverse('notifications_dropdown'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['notifications']), 2)
        self.assertEqual(data['unread_count'], 1)
    
    def test_unread_count_decreases_after_marking_read(self):
        """Test that unread count decreases correctly."""
        self.client.login(username='@johndoe', password='Password123')
        
        # Check initial unread count
        self.assertEqual(self.user.unread_notifications_count(), 1)
        
        # Mark as read
        url = reverse('mark_notification_read', kwargs={'notification_id': self.notification1.id})
        self.client.get(url)
        
        # Check unread count decreased
        self.assertEqual(self.user.unread_notifications_count(), 0)
    
    def test_cannot_mark_other_users_notification_read(self):
        """Test that users cannot mark other users' notifications as read."""
        other_user = User.objects.create_user(
            username='@otheruser',
            email='other@test.com',
            password='Password123',
            first_name='Other',
            last_name='User'
        )
        other_notification = Notification.objects.create(
            recipient=other_user,
            notification_type='report_received',
            title='Other Notification',
            message='Test'
        )
        
        self.client.login(username='@johndoe', password='Password123')
        url = reverse('mark_notification_read', kwargs={'notification_id': other_notification.id})
        response = self.client.get(url)
        
        # Should get 404
        self.assertEqual(response.status_code, 404)
