from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from recipes.models import Follow

User = get_user_model()


class UserProfileViewTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='@user1',
            email='user1@example.com',
            password='testpass123',
            first_name='User',
            last_name='One',
        )
        self.user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='testpass123',
            first_name='User',
            last_name='Two',
        )

    def test_is_following_true_when_logged_in_user_follows_profile_user(self):
        Follow.objects.create(follower=self.user1, following=self.user2)

        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_following'])
        self.assertEqual(response.context['followers_count'], 1)
        self.assertEqual(response.context['following_count'], 0)

    def test_is_following_false_when_not_following(self):
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_following'])
        self.assertEqual(response.context['followers_count'], 0)
        self.assertEqual(response.context['following_count'], 0)
