"""Unit tests for the UserForm."""

from django import forms
from django.test import TestCase

from recipes.forms import UserForm
from recipes.models import User


class UserFormTestCase(TestCase):
    """Unit tests for the UserForm."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.valid_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@example.org',
            'is_private': False,
        }

    # ---------- Field presence ----------

    def test_form_has_required_fields(self):
        form = UserForm()
        for field in ['first_name', 'last_name', 'username', 'email', 'is_private']:
            self.assertIn(field, form.fields)

        self.assertIsInstance(form.fields['email'], forms.EmailField)
        self.assertIsInstance(form.fields['is_private'].widget, forms.CheckboxInput)

    # ---------- Validation ----------

    def test_valid_user_form(self):
        form = UserForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation_for_username(self):
        form = UserForm(data=self.valid_data | {'username': 'badusername'})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_rejects_invalid_email(self):
        form = UserForm(data=self.valid_data | {'email': 'not-an-email'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    # ---------- Saving behaviour ----------

    def test_form_updates_existing_user(self):
        user = User.objects.get(username='@johndoe')

        form = UserForm(instance=user, data=self.valid_data)
        self.assertTrue(form.is_valid())

        before_count = User.objects.count()
        updated_user = form.save()
        after_count = User.objects.count()

        self.assertEqual(before_count, after_count)
        self.assertEqual(updated_user.pk, user.pk)

        self.assertEqual(updated_user.username, '@janedoe')
        self.assertEqual(updated_user.first_name, 'Jane')
        self.assertEqual(updated_user.last_name, 'Doe')
        self.assertEqual(updated_user.email, 'janedoe@example.org')
        self.assertFalse(updated_user.is_private)
