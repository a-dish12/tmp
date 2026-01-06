"""Tests for the log in view."""

from django.contrib import messages
from django.test import TestCase
from django.urls import reverse

from recipes.forms import LogInForm
from recipes.models import User
from recipes.tests.test_helpers import LogInTester, MenuTesterMixin, reverse_with_next


class LogInViewTestCase(TestCase, LogInTester, MenuTesterMixin):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(username='@johndoe')

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')

    def test_get_log_in_renders_page(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        self.assertIsInstance(response.context['form'], LogInForm)
        self.assertFalse(response.context['next'])
        self.assert_no_menu(response)

    def test_get_log_in_with_redirect_param(self):
        destination = reverse('profile')
        response = self.client.get(reverse_with_next('log_in', destination))

        self.assertEqual(response.context['next'], destination)

    def test_logged_in_user_is_redirected(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('dashboard'))

    def test_unsuccessful_login_shows_error(self):
        response = self.client.post(
            self.url,
            {'username': '@johndoe', 'password': 'WrongPassword123'},
        )

        self.assertFalse(self._is_logged_in())
        self.assertTemplateUsed(response, 'log_in.html')
        self.assertEqual(len(response.context['messages']), 1)
        self.assertEqual(list(response.context['messages'])[0].level, messages.ERROR)

    def test_login_with_blank_username(self):
        response = self.client.post(
            self.url,
            {'username': '', 'password': 'Password123'},
        )

        self.assertFalse(self._is_logged_in())
        self.assertEqual(len(response.context['messages']), 1)

    def test_login_with_blank_password(self):
        response = self.client.post(
            self.url,
            {'username': '@johndoe', 'password': ''},
        )

        self.assertFalse(self._is_logged_in())
        self.assertEqual(len(response.context['messages']), 1)

    def test_successful_login_redirects_to_dashboard(self):
        response = self.client.post(
            self.url,
            {'username': '@johndoe', 'password': 'Password123'},
            follow=True,
        )

        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, reverse('dashboard'))
        self.assert_menu(response)

    def test_successful_login_with_next_redirect(self):
        destination = reverse('profile')

        response = self.client.post(
            self.url,
            {'username': '@johndoe', 'password': 'Password123', 'next': destination},
            follow=True,
        )

        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, destination)

    def test_post_redirects_when_already_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.post(
            self.url,
            {'username': '@wronguser', 'password': 'WrongPassword123'},
        )

        self.assertRedirects(response, reverse('dashboard'))

    def test_invalid_login_preserves_next(self):
        destination = reverse('profile')

        response = self.client.post(
            self.url,
            {'username': '@johndoe', 'password': 'WrongPassword123', 'next': destination},
        )

        self.assertEqual(response.context['next'], destination)

    def test_inactive_user_cannot_log_in(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            self.url,
            {'username': '@johndoe', 'password': 'Password123'},
        )

        self.assertFalse(self._is_logged_in())
        self.assertEqual(len(response.context['messages']), 1)
