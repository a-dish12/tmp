from django.test import TestCase, override_settings
from django.urls import reverse, resolve
import importlib
import recipify.urls

class URLSmokeTest(TestCase):
    """Smoke tests for all URL patterns"""

    def test_named_urls_resolve(self):
        """All named URLS should resolve without error"""
        url_names = [
            'home',
            'dashboard',
            'following_dashboard',
            'log_in',
            'log_out',
            'password',
            'profile',
            'sign_up',
            'create_recipe',
            'user_recipes',
            'search_users',
            'search_users_ajax',
            'dashboard-surprise',
            'surprise-result',
            'notifications_dropdown',
            'mark_all_notifications_read',
            'planner_range',
            'planner_events',
            'ingredients_list',
        ]
        for name in url_names:
            with self.subTest(name=name):
                url = reverse(name)
                self.assertIsNotNone(resolve(url))


class URLWithArgsTests(TestCase):
    """URLs that require parameters"""
    def test_urls_with_arguments_resolve(self):
        urls=[
            reverse('user_profile', args=[1]),
            reverse('follow_user', args=[1]),
            reverse('unfollow_user', args=[1]),
            reverse('user_following', args=[1]),
            reverse('accept_follow_request', args=[1]),
            reverse('reject_follow_request', args=[1]),
            reverse('cancel_follow_request', args=[1]),
            reverse('user_followers', args=[1]),
            reverse('planner_day', args=['2024-01-01']),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertIsNotNone(resolve(url))


class RecipeURLTest(TestCase):
    def test_recipe_urls_resolve(self):
        urls = [
            reverse('recipe_detail', args=[1]),
            reverse('edit_recipe', args=[1]),
            reverse('delete_recipe', args=[1]),
            reverse('rate_recipe', args=[1]),
            reverse('add_to_calendar', args=[1]),
            reverse('report_recipe', args=[1]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertIsNotNone(resolve(url))

class DebugStaticURLTest(TestCase):
    @override_settings(DEBUG=True)
    def test_debug_static_and_media_urls(self):
        """Ensure static/media URL patterns are added when the DEBUG=True"""
        importlib.reload(recipify.urls)
        urlpatterns = recipify.urls.urlpatterns

        self.assertTrue(any('static' in str(p.pattern) for p in urlpatterns))
