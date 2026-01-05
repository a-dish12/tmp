from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from recipes.models import Follow, FollowRequest

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

class FollowRequestTests(TestCase):
    """Tests for private accounts and follow request handling"""

    def setUp(self):
        self.follower = User.objects.create_user(
            username='@follower',
            email = 'follower@test.com',
            password='testpass123'
        )
        self.private_user = User.objects.create_user(
            username='@private',
            email = 'private@test.com',
            password='testpass1234'
        )
        self.private_user.is_private = True
        self.private_user.save()
        self.client.force_login(self.follower)
    
    def test_follow_private_user_creates_follow_request(self):
        """Following a private user should create a FollowRequest"""
        url = reverse('follow_user', kwargs={'user_id': self.private_user.id})
        self.client.post(url)

        self.assertTrue(
            FollowRequest.objects.filter(
                from_user = self.follower,
                to_user = self.private_user
            ).exists()
        )
        self.assertFalse(
            Follow.objects.filter(
                follower = self.follower,
                following = self.private_user
            ).exists()
        )
    
    def test_follow_self_does_nothing(self):
        """User should not be able to follow themselves"""
        url = reverse('follow_user', kwargs={'user_id': self.follower.id})
        self.client.post(url)

        self.assertEqual(Follow.objects.count(),0)
        self.assertEqual(FollowRequest.objects.count(), 0)

class FollowRequestActionTests(TestCase):
    """Tests for accpeting, rejecting, and cancelling follow requests"""
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
        )
        self.to_user.is_private = True
        self.to_user.save()

        self.request = FollowRequest.objects.create(
            from_user = self.from_user,
            to_user = self.to_user
        )
    def test_accept_follow_request_creates_follow(self):
        """Accepting a follow request creates Follow and deletes request"""
        self.client.force_login(self.to_user)
        url = reverse('accept_follow_request', kwargs={'request_id': self.request.id})
        self.client.post(url)

        self.assertTrue(
            Follow.objects.filter(
                follower = self.from_user,
                following = self.to_user
            ).exists()
        )
        self.assertFalse(FollowRequest.objects.filter(id=self.request.id).exists())
    
    def test_reject_follow_request_deletes_request_only(self):
        """Rejecting deletes request but doesn't create follow"""
        self.client.force_login(self.to_user)
        url = reverse('reject_follow_request', kwargs={"request_id": self.request.id})
        self.client.post(url)

        self.assertFalse(FollowRequest.objects.filter(id=self.request.id).exists())
        self.assertFalse(Follow.objects.exists())
    
    def test_cancel_follow_request(self):
        """Sender can cancel their own follow request"""
        self.client.force_login(self.from_user)

        url = reverse('cancel_follow_request', kwargs={'user_id': self.to_user.id})
        self.client.post(url)

        self.assertFalse(FollowRequest.objects.exists())

class FollowersFollowingPageTests(TestCase):
    """Tests for followers and following list views"""
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
        Follow.objects.create(follower = self.user1, following = self.user2)

    def test_user_followers_page(self):
        """Followers page shows users following profile"""
        url = reverse('user_followers', kwargs= {'user_id': self.user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response, '@user1')

    def test_user_following_page(self):
        """Following page shows user profile is following"""
        url = reverse('user_following', kwargs = {'user_id': self.user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '@user2')
