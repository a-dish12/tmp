"""Unit tests for the log in form."""

from django import forms
from django.test import TestCase

from recipes.forms import LogInForm
from recipes.models import User


class LogInFormTestCase(TestCase):
    """Unit tests of the log in form."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.valid_input = {
            'username': '@janedoe',
            'password': 'Password123'
        }

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)

        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.valid_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        form = LogInForm(data={
            'username': '',
            'password': 'Password123'
        })
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        form = LogInForm(data={
            'username': '@janedoe',
            'password': ''
        })
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_username_format(self):
        """Form validation does not check credential correctness."""
        form = LogInForm(data={
            'username': 'ja',
            'password': 'Password123'
        })
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        """Form validation does not check credential correctness."""
        form = LogInForm(data={
            'username': '@janedoe',
            'password': 'pwd'
        })
        self.assertTrue(form.is_valid())

    def test_can_authenticate_valid_user(self):
        fixture = User.objects.get(username='@johndoe')
        form = LogInForm(data={
            'username': '@johndoe',
            'password': 'Password123'
        })

        user = form.get_user()
        self.assertEqual(user, fixture)

    def test_invalid_credentials_do_not_authenticate(self):
        form = LogInForm(data={
            'username': '@johndoe',
            'password': 'WrongPassword123'
        })

        user = form.get_user()
        self.assertIsNone(user)

    def test_blank_password_does_not_authenticate(self):
        form = LogInForm(data={
            'username': '@johndoe',
            'password': ''
        })

        user = form.get_user()
        self.assertIsNone(user)

    def test_blank_username_does_not_authenticate(self):
        form = LogInForm(data={
            'username': '',
            'password': 'Password123'
        })

        user = form.get_user()
        self.assertIsNone(user)
