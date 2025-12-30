"""
Unit tests for the Follow model.

These tests verify the creation, uniqueness constraints, cascade deletion,
and string representation of follow relationships between users.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from recipes.models import Follow

User = get_user_model()


class FollowModelTest(TestCase):
    """
    Test suite for the Follow model.
    """

    def setUp(self):
        """
        Create two sample user accounts for follow relationship testing.
        """
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

    def test_create_follow(self):
        """
        Creating a Follow object assigns the correct users and timestamp.
        """
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)
        self.assertIsNotNone(follow.created_at)

    def test_unique_together_prevents_duplicate_follow(self):
        """
        A user cannot follow the same user more than once.
        """
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        with self.assertRaises(IntegrityError):
            Follow.objects.create(
                follower=self.user1,
                following=self.user2
            )

    def test_follow_string_representation(self):
        """
        The string representation includes both usernames.
        """
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

        self.assertIn(self.user1.username, str(follow))
        self.assertIn(self.user2.username, str(follow))

    def test_follow_deleted_when_follower_deleted(self):
        """
        Follow relationships are deleted when the follower user is deleted.
        """
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        follow_id = follow.id

        self.user1.delete()

        self.assertFalse(Follow.objects.filter(id=follow_id).exists())

    def test_follow_deleted_when_following_deleted(self):
        """
        Follow relationships are deleted when the followed user is deleted.
        """
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        follow_id = follow.id

        self.user2.delete()

        self.assertFalse(Follow.objects.filter(id=follow_id).exists())
