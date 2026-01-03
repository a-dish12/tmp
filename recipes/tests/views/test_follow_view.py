from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from recipes.models import Follow, FollowRequest, Notification

User = get_user_model()


class FollowViewTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='@user1',
            email='user1@example.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )

    def test_follow_creates_relation_and_redirects(self):

        self.client.force_login(self.user1)
        url = reverse('follow_user', kwargs={'user_id': self.user2.id})

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('user_profile', kwargs={'user_id': self.user2.id})
        )

        self.assertTrue(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).exists()
        )

    def test_follow_private_account_creates_notification(self):
        """Test that following a private account creates a notification."""
        self.user2.is_private = True
        self.user2.save()
        
        self.client.force_login(self.user1)
        url = reverse('follow_user', kwargs={'user_id': self.user2.id})
        
        # Initially no notifications
        self.assertEqual(Notification.objects.filter(recipient=self.user2).count(), 0)
        
        response = self.client.post(url)
        
        # Check follow request was created
        self.assertTrue(
            FollowRequest.objects.filter(
                from_user=self.user1,
                to_user=self.user2
            ).exists()
        )
        
        # Check notification was created
        self.assertEqual(Notification.objects.filter(recipient=self.user2).count(), 1)
        notification = Notification.objects.get(recipient=self.user2)
        self.assertEqual(notification.notification_type, 'follow_request')
        self.assertIn(self.user1.username, notification.message)
    
    def test_follow_private_account_duplicate_no_notification(self):
        """Test that duplicate follow requests don't create duplicate notifications."""
        self.user2.is_private = True
        self.user2.save()
        
        self.client.force_login(self.user1)
        url = reverse('follow_user', kwargs={'user_id': self.user2.id})
        
        # First request
        self.client.post(url)
        self.assertEqual(Notification.objects.filter(recipient=self.user2).count(), 1)
        
        # Second request (duplicate)
        self.client.post(url)
        # Should still be only 1 notification
        self.assertEqual(Notification.objects.filter(recipient=self.user2).count(), 1)

    def test_follow_does_not_duplicate(self):
        Follow.objects.create(follower=self.user1, following=self.user2)

        self.client.force_login(self.user1)
        url = reverse('follow_user', kwargs={'user_id': self.user2.id})

        response = self.client.post(url)

        # redirect still correct
        self.assertRedirects(
            response,
            reverse('user_profile', kwargs={'user_id': self.user2.id})
        )

        # Still exactly one follow object
        self.assertEqual(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).count(),
            1
        )

class UnfollowViewTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='@user1',
            email='user1@example.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )

    def test_unfollow_deletes_follow_and_redirects(self):
        Follow.objects.create(follower=self.user1, following=self.user2)

        self.client.force_login(self.user1)
        url = reverse('unfollow_user', kwargs={'user_id': self.user2.id})

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('user_profile', kwargs={'user_id': self.user2.id})
        )

        self.assertFalse(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).exists()
        )
