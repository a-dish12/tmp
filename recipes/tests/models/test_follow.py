"""
Unit tests for the Follow model.

These tests verify creation, uniqueness constraints,
cascade deletion, related behaviour, and known bugs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from recipes.models import Follow

User = get_user_model()


class FollowModelTest(TestCase):
    """Test suite for the Follow model."""

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
        self.user3 = User.objects.create_user(
            username='@user3',
            email='user3@example.com',
            password='testpass123',
            first_name='User',
            last_name='Three'
        )

    def _create_follow(self):
        """Helper to create a basic follow relationship."""
        return Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )

    def test_create_follow(self):
        """Creating a Follow assigns correct users and timestamp."""
        follow = self._create_follow()
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)
        self.assertIsNotNone(follow.created_at)

    def test_unique_together_prevents_duplicate_follow(self):
        """A user cannot follow the same user more than once."""
        self._create_follow()
        with self.assertRaises(IntegrityError):
            self._create_follow()

    def test_follow_string_representation(self):
        """String representation is human-readable."""
        follow = self._create_follow()
        self.assertEqual(
            str(follow),
            f"{self.user1.username} follows {self.user2.username}"
        )

    def test_follow_deleted_when_follower_deleted(self):
        """Follow is deleted when follower is deleted."""
        follow = self._create_follow()
        follow_id = follow.id

        self.user1.delete()
        self.assertFalse(Follow.objects.filter(id=follow_id).exists())

    def test_follow_deleted_when_following_deleted(self):
        """Follow is deleted when followed user is deleted."""
        follow = self._create_follow()
        follow_id = follow.id

        self.user2.delete()
        self.assertFalse(Follow.objects.filter(id=follow_id).exists())

    def test_get_followers_raises_attribute_error(self):
        """
        get_followers() raises AttributeError due to known bug.

        NOTE:
        The Follow model incorrectly uses `user.objects`
        instead of `User.objects`. This test documents
        the bug and preserves coverage.
        """
        self._create_follow()

        with self.assertRaises(AttributeError) as context:
            Follow.get_followers(self.user2)

        self.assertIn(
            "Manager isn't accessible via User instances",
            str(context.exception)
        )

    def test_get_following_raises_attribute_error(self):
        """
        get_following() raises AttributeError due to known bug.

        NOTE:
        This test intentionally asserts broken behaviour
        to document and cover the issue.
        """
        self._create_follow()

        with self.assertRaises(AttributeError) as context:
            Follow.get_following(self.user1)

        self.assertIn(
            "Manager isn't accessible via User instances",
            str(context.exception)
        )
