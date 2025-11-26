from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from recipes.models import Follow

User = get_user_model()

class FollowModelTest(TestCase):

    #2 sample user accounts to run the tests.
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
    
    # Test create Follow creates the correct follow relation and assigns the right attributes
    def test_create_follow(self):
        follow = Follow.objects.create(
            follower = self.user1,
            following = self.user2
        )

        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)
        self.assertIsNotNone(follow.created_at)

    # Test following same account twice raises Integrity Error
    def test_unique_together_prevents_duplicate_follow(self):
        Follow.objects.create(
            follower = self.user1, 
            following = self.user2)

        with self.assertRaises(IntegrityError):
            Follow.objects.create(follower=self.user1, following=self.user2)
