from django.contrib.auth.hashers import check_password
from django.test import TestCase

from recipes.models import User
from recipes.forms import PasswordForm


class PasswordFormTestCase(TestCase):
    """Unit tests for the PasswordForm."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.valid_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123',
        }

    # ---------- Field presence ----------

    def test_form_has_required_fields(self):
        form = PasswordForm(user=self.user)
        self.assertIn('password', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('password_confirmation', form.fields)

    # ---------- Valid form ----------

    def test_form_accepts_valid_input(self):
        form = PasswordForm(user=self.user, data=self.valid_input)
        self.assertTrue(form.is_valid())

    # ---------- Password validation ----------

    def test_new_password_requires_uppercase_letter(self):
        self._assert_invalid_new_password('password123')

    def test_new_password_requires_lowercase_letter(self):
        self._assert_invalid_new_password('PASSWORD123')

    def test_new_password_requires_number(self):
        self._assert_invalid_new_password('PasswordABC')

    def test_password_confirmation_must_match(self):
        data = self.valid_input.copy()
        data['password_confirmation'] = 'WrongPassword123'
        form = PasswordForm(user=self.user, data=data)
        self.assertFalse(form.is_valid())

    # ---------- Current password validation ----------

    def test_current_password_must_be_correct(self):
        data = self.valid_input.copy()
        data['password'] = 'WrongPassword123'
        form = PasswordForm(user=self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_form_requires_user(self):
        form = PasswordForm(data=self.valid_input)
        self.assertFalse(form.is_valid())

    # ---------- Saving ----------

    def test_save_updates_user_password(self):
        form = PasswordForm(user=self.user, data=self.valid_input)
        self.assertTrue(form.is_valid())
        form.save()

        self.user.refresh_from_db()
        self.assertTrue(check_password('NewPassword123', self.user.password))
        self.assertFalse(check_password('Password123', self.user.password))

    def test_save_returns_false_when_no_user(self):
        form = PasswordForm(user=None, data=self.valid_input)
        form.full_clean()
        result = form.save()
        self.assertFalse(result)

    # ---------- Helpers ----------

    def _assert_invalid_new_password(self, new_password):
        data = self.valid_input.copy()
        data['new_password'] = new_password
        data['password_confirmation'] = new_password
        form = PasswordForm(user=self.user, data=data)
        self.assertFalse(form.is_valid())
