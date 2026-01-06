"""
Unit tests for the FollowRequest model.

These tests verify creation, uniqueness constraints,
cascade deletion, related names, and string representation.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from recipes.models import FollowRequest

User = get_user_model()


class FollowRequestModelTest(TestCase):
    """Test suite for the FollowRequest model."""

    def setUp(self):
        self.from_user = User.objects.create_user(
            username='@sender',
            email='sender@example.com',
            password='testpass123'
        )
        self.to_user = User.objects.create_user(
            username='@receiver',
            email='receiver@example.com',
            password='testpass123'
        )

        self.follow_request = FollowRequest.objects.create(
            from_user=self.from_user,
            to_user=self.to_user
        )

    def test_valid_follow_request(self):
        """A FollowRequest with valid users passes validation."""
        try:
            self.follow_request.full_clean()
        except ValidationError:
            self.fail("FollowRequest should be valid")

    def test_follow_request_requires_from_user(self):
        """A FollowRequest without a sender is invalid."""
        self.follow_request.from_user = None
        with self.assertRaises(ValidationError):
            self.follow_request.full_clean()

    def test_follow_request_requires_to_user(self):
        """A FollowRequest without a recipient is invalid."""
        self.follow_request.to_user = None
        with self.assertRaises(ValidationError):
            self.follow_request.full_clean()

    def test_unique_together_prevents_duplicate_requests(self):
        """Duplicate follow requests are not allowed."""
        with self.assertRaises(IntegrityError):
            FollowRequest.objects.create(
                from_user=self.from_user,
                to_user=self.to_user
            )

    def test_follow_request_string_representation(self):
        """String representation includes both users."""
        self.assertEqual(
            str(self.follow_request),
            f"{self.from_user} → {self.to_user}"
        )

    def test_follow_requests_deleted_when_sender_deleted(self):
        """FollowRequest is deleted when sender is deleted."""
        request_id = self.follow_request.id
        self.from_user.delete()

        self.assertFalse(
            FollowRequest.objects.filter(id=request_id).exists()
        )

    def test_follow_requests_deleted_when_receiver_deleted(self):
        """FollowRequest is deleted when receiver is deleted."""
        request_id = self.follow_request.id
        self.to_user.delete()

        self.assertFalse(
            FollowRequest.objects.filter(id=request_id).exists()
        )

    def test_related_name_sent_follow_requests(self):
        """sent_follow_requests returns requests sent by the user."""
        self.assertIn(
            self.follow_request,
            self.from_user.sent_follow_requests.all()
        )

    def test_related_name_received_follow_requests(self):
        """received_follow_requests returns requests received by the user."""
        self.assertIn(
            self.follow_request,
            self.to_user.received_follow_requests.all()
        )