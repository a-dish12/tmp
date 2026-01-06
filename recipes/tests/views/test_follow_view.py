"""Tests for follow, unfollow, and follow request views."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from recipes.models import Follow, FollowRequest

User = get_user_model()


class FollowUserViewTestCase(TestCase):
    """Tests for following users."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='@user1',
            email='user1@example.com',
            password='testpass123',
        )
        self.user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='testpass123',
        )

        self.url = reverse('follow_user', kwargs={'user_id': self.user2.id})

    def test_follow_creates_relation_and_redirects(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse('user_profile', kwargs={'user_id': self.user2.id}),
        )

        self.assertTrue(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2,
            ).exists()
        )

    def test_follow_does_not_duplicate(self):
        Follow.objects.create(follower=self.user1, following=self.user2)

        self.client.force_login(self.user1)
        self.client.post(self.url)

        self.assertEqual(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2,
            ).count(),
            1,
        )

    def test_user_cannot_follow_self(self):
        self.client.force_login(self.user1)
        url = reverse('follow_user', kwargs={'user_id': self.user1.id})
        self.client.post(url)

        self.assertFalse(Follow.objects.exists())
        self.assertFalse(FollowRequest.objects.exists())


class UnfollowUserViewTestCase(TestCase):
    """Tests for unfollowing users."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='@user1',
            email='user1@example.com',
            password='testpass123',
        )
        self.user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='testpass123',
        )

        Follow.objects.create(follower=self.user1, following=self.user2)
        self.url = reverse('unfollow_user', kwargs={'user_id': self.user2.id})

    def test_unfollow_deletes_relation_and_redirects(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse('user_profile', kwargs={'user_id': self.user2.id}),
        )

        self.assertFalse(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2,
            ).exists()
        )


class FollowRequestCreationTestCase(TestCase):
    """Tests for private accounts and follow request creation."""

    def setUp(self):
        self.follower = User.objects.create_user(
            username='@follower',
            email='follower@test.com',
            password='testpass123',
        )
        self.private_user = User.objects.create_user(
            username='@private',
            email='private@test.com',
            password='testpass1234',
            is_private=True,
        )

        self.client.force_login(self.follower)
        self.url = reverse('follow_user', kwargs={'user_id': self.private_user.id})

    def test_follow_private_user_creates_follow_request(self):
        self.client.post(self.url)

        self.assertTrue(
            FollowRequest.objects.filter(
                from_user=self.follower,
                to_user=self.private_user,
            ).exists()
        )
        self.assertFalse(Follow.objects.exists())


class FollowRequestActionTestCase(TestCase):
    """Tests for accepting, rejecting, and cancelling follow requests."""

    def setUp(self):
        self.from_user = User.objects.create_user(
            username='@from',
            email='from@example.com',
            password='testpass123',
        )
        self.to_user = User.objects.create_user(
            username='@to',
            email='to@example.com',
            password='testpass1234',
            is_private=True,
        )

        self.request = FollowRequest.objects.create(
            from_user=self.from_user,
            to_user=self.to_user,
        )

    def test_accept_follow_request_creates_follow(self):
        self.client.force_login(self.to_user)
        url = reverse('accept_follow_request', kwargs={'request_id': self.request.id})
        self.client.post(url)

        self.assertTrue(
            Follow.objects.filter(
                follower=self.from_user,
                following=self.to_user,
            ).exists()
        )
        self.assertFalse(FollowRequest.objects.exists())

    def test_reject_follow_request_deletes_request_only(self):
        self.client.force_login(self.to_user)
        url = reverse('reject_follow_request', kwargs={'request_id': self.request.id})
        self.client.post(url)

        self.assertFalse(FollowRequest.objects.exists())
        self.assertFalse(Follow.objects.exists())

    def test_cancel_follow_request(self):
        self.client.force_login(self.from_user)
        url = reverse('cancel_follow_request', kwargs={'user_id': self.to_user.id})
        self.client.post(url)

        self.assertFalse(FollowRequest.objects.exists())


class FollowersFollowingPageTestCase(TestCase):
    """Tests for followers and following list pages."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='@user1',
            email='user1@example.com',
            password='testpass123',
        )
        self.user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='testpass123',
        )

        Follow.objects.create(follower=self.user1, following=self.user2)

    def test_followers_page_lists_followers(self):
        url = reverse('user_followers', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '@user1')

    def test_following_page_lists_followed_users(self):
        url = reverse('user_following', kwargs={'user_id': self.user1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '@user2')