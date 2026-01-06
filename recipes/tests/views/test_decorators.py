"""Tests for login_prohibited decorator and LoginProhibitedMixin."""

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

from recipes.views import login_prohibited, LoginProhibitedMixin


class LoginProhibitedDecoratorTestCase(TestCase):
    """Tests for the login_prohibited decorator."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_authenticated_user_is_redirected(self):
        @login_prohibited
        def dummy_view(request):
            return HttpResponse("OK")

        request = self.factory.get("/")
        request.user = self._create_logged_in_user()

        response = dummy_view(request)

        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_can_access_view(self):
        @login_prohibited
        def dummy_view(request):
            return HttpResponse("OK")

        request = self.factory.get("/")
        request.user = AnonymousUser()

        response = dummy_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "OK")

    def _create_logged_in_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username="user",
            password="Password123",
            email="user@test.com",
        )


class LoginProhibitedMixinTestCase(TestCase):
    """Tests for LoginProhibitedMixin."""

    def test_get_redirect_url_raises_exception_when_not_configured(self):
        mixin = LoginProhibitedMixin()

        with self.assertRaises(ImproperlyConfigured):
            mixin.get_redirect_when_logged_in_url()

    def test_get_redirect_url_returns_configured_url(self):
        class TestMixin(LoginProhibitedMixin):
            redirect_when_logged_in_url = "/dashboard/"

        mixin = TestMixin()

        self.assertEqual(mixin.get_redirect_when_logged_in_url(), "/dashboard/")
