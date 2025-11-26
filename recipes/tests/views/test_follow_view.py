from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from recipes.models import Follow

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
