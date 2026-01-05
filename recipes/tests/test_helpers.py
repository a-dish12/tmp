from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.helpers import visible_recipes_for
from recipes.models import Recipe, Follow
from with_asserts.mixin import AssertHTMLMixin
User = get_user_model()

def reverse_with_next(url_name, next_url):
    """Extended version of reverse to generate URLs with redirects"""
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url


class LogInTester:
    """Class support login in tests."""
 
    def _is_logged_in(self):
        """Returns True if a user is logged in.  False otherwise."""

        return '_auth_user_id' in self.client.session.keys()

class MenuTesterMixin(AssertHTMLMixin):
    """Class to extend tests with tools to check the presents of menu items."""

    menu_urls = [
        reverse('log_out')
    ]

    def assert_menu(self, response):
        """Check that menu is present."""

        for url in self.menu_urls:
            with self.assertHTML(response, f'a[href="{url}"]'):
                pass

    def assert_no_menu(self, response):
        """Check that no menu is present."""
        
        for url in self.menu_urls:
            self.assertNotHTML(response, f'a[href="{url}"]')

class ReverseWithNextTest(TestCase):
    """Tests forr reverse_with_next helper"""
    def test_reverse_with_next_appends_query(self):
        url=reverse_with_next("log_in", "/dashboard/")
        self.assertEqual(url, f"{reverse('log_in')}?next=/dashboard/")
    def test_reverse_with_next_empty_next(self):
        url= reverse_with_next("log_in", "")
        self.assertEqual(url, f"{reverse('log_in')}?next=")

    def test_reverse_with_next_special_chars(self):
        url = reverse_with_next("log_in", "/foo?bar=baz")
        self.assertEqual(url, f"{reverse('log_in')}?next=/foo?bar=baz")


class LogInTesterTest(TestCase, LogInTester):
    """Tests for LogInTester login detection
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="password123",
            email="user1@test.com"
        )
    def test_is_logged_in_false(self):
        self.assertFalse(self._is_logged_in())
    def test_is_logged_in_true(self):
        self.client.login(username="user1", password="password123")
        self.assertTrue(self._is_logged_in())
    def test_is_logged_in_after_logout(self):
        """Ensure logout clears authentication"""
        self.client.login(username="user1", password = "password123")
        self.client.logout()
        self.assertFalse(self._is_logged_in())
    def test_is_logged_in_without_session(self):
        """Directly clearing session should return False"""
        self.client.login(username="user1", password="password123")
        self.client.session.flush()
        self.assertFalse(self._is_logged_in())


class MenuTesterMixinTest(TestCase, MenuTesterMixin):
    """Tests menu assertion helpers"""
    def setUp(self):
        self.user = User.objects.create_user(
            username="menuuser",
            password="password123",
            email="menu@test.com"
        )
    def test_assert_menu_raises_when_missing(self):
        """assert_menu should fail if menu is missing"""
        response = self.client.get(reverse("log_in"))
        with self.assertRaises(AssertionError):
            self.assert_menu(response)

    def  test_assert_menu_passes_when_logged_in(self):
        """Menu should be present on authenticaed pages"""
        self.client.login(username="menuuser", password="password123")
        response = self.client.get(reverse("dashboard"))
        self.assert_menu(response)
    def test_assert_no_menu_passes_when_logged_out(self):
        """Menu should not be present for unauthenticated users"""
        response = self.client.get(reverse("log_in"))
        self.assert_no_menu(response)
    def test_assert_menu_fails_when_not_logged_in(self):
        response=self.client.get(reverse("dashboard"), follow=True)
        self.assert_no_menu(response)

class VisibleRecipesForTest(TestCase):
    """Tests for visible_recipes_for helper"""
    def setUp(self):
        self.public_user = User.objects.create_user(
            username="public",
            password="password123",
            email="public@test.com",
            is_private=False
        )
        self.private_user = User.objects.create_user(
            username="private",
            password="password123",
            email="private@test.com",
            is_private=True
        )
        self.viewer = User.objects.create_user(
            username="viewer",
            password="password123",
            email="viewer@test.com"
        )
        self.public_recipe = Recipe.objects.create(
            title="Public Recipe",
            description="desc",
            ingredients="i",
            instructions="cook",
            time=10,
            meal_type="lunch",
            author=self.public_user
        )
        self.private_recipe = Recipe.objects.create(
            title="Public Recipe",
            description="desc",
            ingredients="i",
            instructions="cook",
            time=10,
            meal_type="lunch",
            author=self.private_user
        )
    def test_anonymous_user_sees_only_public_recipes(self):
        qs = visible_recipes_for(None)
        self.assertIn(self.public_recipe, qs)
        self.assertNotIn(self.private_recipe, qs)
    def test_authenticated_user_sees_public_recipe(self):
        qs = visible_recipes_for(self.viewer)
        self.assertIn(self.public_recipe, qs)
    def test_authenticated_user_with_no_follows_and_no_private_users(self):
        qs = visible_recipes_for(self.viewer)
        self.assertEqual(list(qs), [self.public_recipe])

    def test_authenticated_user_does_not_see_unfollowed_private_recipe(self):
        qs = visible_recipes_for(self.viewer)
        self.assertIn(self.public_recipe, qs)
        self.assertNotIn(self.private_recipe, qs)
    def test_authenticated_user_sees_followed_private_recipes(self):
        Follow.objects.create(
            follower = self.viewer,
            following = self.private_user
        )
        qs = visible_recipes_for(self.viewer)
        self.assertIn(self.private_recipe, qs)
    def test_user_sees_own_private_recipes(self):
        own_private_recipe=Recipe.objects.create(
            title="My private recipe",
            description="desc",
            ingredients="i",
            instructions="cook",
            time=10,
            meal_type="lunch",
            author= self.viewer
        )
        qs = visible_recipes_for(self.viewer)
        self.assertIn(own_private_recipe, qs)
    def test_authenticated_user_object_sees_only_public_recipes(self):
        anon_user = User()
        qs = visible_recipes_for(anon_user)
        self.assertIn(self.public_recipe, qs)
        self.assertNotIn(self.private_recipe, qs)