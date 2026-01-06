"""Tests for the profile update view."""

from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import MagicMock

from recipes.models import User, Follow, FollowRequest
from recipes.tests.test_helpers import reverse_with_next
from recipes.views.profile_view import ProfileUpdateView


class ProfileViewTest(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.url = reverse('profile')
        self.factory = RequestFactory()

    def _build_request(self):
        """
        Build a fake POST request suitable for directly invoking CBV logic.
        """
        request = self.factory.post(self.url)
        request.user = self.user
        request._messages = MagicMock()
        return request

    # ----------------------------------------------------
    # Access control
    # ----------------------------------------------------

    def test_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url)

    # ----------------------------------------------------
    # Private → Public follow-request promotion logic
    # ----------------------------------------------------

    def test_becoming_public_with_requests(self):
        """
        When a user switches from private → public,
        incoming follow requests should be accepted.
        """
        self.user.is_private = True
        self.user.save()

        FollowRequest.objects.create(
            from_user=self.other_user,
            to_user=self.user
        )

        form = MagicMock()
        form.cleaned_data = {'is_private': False}

        request = self._build_request()
        view = ProfileUpdateView()
        view.request = request

        view.form_valid(form)

        self.assertTrue(
            Follow.objects.filter(
                follower=self.other_user,
                following=self.user
            ).exists()
        )
        self.assertEqual(FollowRequest.objects.count(), 0)

    def test_becoming_public_with_no_requests(self):
        """
        Switching to public with no incoming requests should be a no-op.
        """
        self.user.is_private = True
        self.user.save()

        form = MagicMock()
        form.cleaned_data = {'is_private': False}

        request = self._build_request()
        view = ProfileUpdateView()
        view.request = request

        view.form_valid(form)

        self.assertEqual(Follow.objects.count(), 0)
        self.assertEqual(FollowRequest.objects.count(), 0)

    def test_not_becoming_public(self):
        """
        If user was already public, follow requests must not be auto-accepted.
        """
        self.user.is_private = False
        self.user.save()

        FollowRequest.objects.create(
            from_user=self.other_user,
            to_user=self.user
        )

        form = MagicMock()
        form.cleaned_data = {'is_private': False}

        request = self._build_request()
        view = ProfileUpdateView()
        view.request = request

        view.form_valid(form)

        self.assertEqual(Follow.objects.count(), 0)
        self.assertEqual(FollowRequest.objects.count(), 1)

    def test_self_follow_is_excluded(self):
        """
        A user must never be allowed to follow themselves,
        even via follow-request promotion.
        """
        self.user.is_private = True
        self.user.save()

        FollowRequest.objects.create(
            from_user=self.user,
            to_user=self.user
        )
        FollowRequest.objects.create(
            from_user=self.other_user,
            to_user=self.user
        )

        form = MagicMock()
        form.cleaned_data = {'is_private': False}

        request = self._build_request()
        view = ProfileUpdateView()
        view.request = request

        view.form_valid(form)

        self.assertFalse(
            Follow.objects.filter(
                follower=self.user,
                following=self.user
            ).exists()
        )
        self.assertTrue(
            Follow.objects.filter(
                follower=self.other_user,
                following=self.user
            ).exists()
        )
