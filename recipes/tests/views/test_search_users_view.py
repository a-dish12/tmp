from django.test import TestCase
from django.urls import reverse
from recipes.models import User
import json


class SearchUsersViewTestCase(TestCase):
    """Tests for the user search page."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('search_users')

        self.user2 = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123',
            first_name='Jane',
            last_name='Doe'
        )
        self.user3 = User.objects.create_user(
            username='@bobsmith',
            email='bob@example.com',
            password='Password123',
            first_name='Bob',
            last_name='Smith'
        )
        self.user4 = User.objects.create_user(
            username='@alicejohnson',
            email='alice@example.com',
            password='Password123',
            first_name='Alice',
            last_name='Johnson'
        )

        self.client.login(username='@johndoe', password='Password123')

    def test_search_users_url(self):
        self.assertEqual(self.url, '/search-users/')

    def test_search_users_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/log_in/?next={self.url}')

    def test_search_users_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_users.html')

    def test_search_users_excludes_current_user(self):
        response = self.client.get(self.url)
        users = response.context['users']

        self.assertNotIn(self.user, users)
        self.assertIn(self.user2, users)
        self.assertIn(self.user3, users)
        self.assertIn(self.user4, users)

    def test_search_users_displays_all_other_users(self):
        response = self.client.get(self.url)

        self.assertContains(response, '@janedoe')
        self.assertContains(response, '@bobsmith')
        self.assertContains(response, '@alicejohnson')
        self.assertNotContains(response, '@johndoe')

    def test_search_users_with_query(self):
        response = self.client.get(self.url, {'search': 'jane'})
        users = response.context['users']

        self.assertEqual(len(users), 1)
        self.assertIn(self.user2, users)
        self.assertNotIn(self.user3, users)
        self.assertNotIn(self.user4, users)

        self.assertEqual(response.context['search_query'], 'jane')


class SearchUsersAjaxTestCase(TestCase):
    """Tests for AJAX user search."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('search_users_ajax')

        self.user2 = User.objects.create_user(
            username='@janedoe',
            email='jane@example.com',
            password='Password123',
            first_name='Jane',
            last_name='Doe'
        )
        self.user3 = User.objects.create_user(
            username='@bobsmith',
            email='bob@example.com',
            password='Password123',
            first_name='Bob',
            last_name='Smith'
        )
        self.user4 = User.objects.create_user(
            username='@alicejohnson',
            email='alice@example.com',
            password='Password123',
            first_name='Alice',
            last_name='Johnson'
        )

        self.client.login(username='@johndoe', password='Password123')

    def test_ajax_search_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_ajax_search_returns_json(self):
        response = self.client.get(self.url)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_ajax_search_no_query_returns_all_users(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)

        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['users']), 3)

    def test_ajax_search_by_username(self):
        response = self.client.get(self.url, {'q': 'jane'})
        data = json.loads(response.content)

        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['username'], '@janedoe')

    def test_ajax_search_by_first_name(self):
        response = self.client.get(self.url, {'q': 'Bob'})
        data = json.loads(response.content)

        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['first_name'], 'Bob')

    def test_ajax_search_by_last_name(self):
        response = self.client.get(self.url, {'q': 'Smith'})
        data = json.loads(response.content)

        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['last_name'], 'Smith')

    def test_ajax_search_case_insensitive(self):
        response = self.client.get(self.url, {'q': 'ALICE'})
        data = json.loads(response.content)

        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['first_name'], 'Alice')

    def test_ajax_search_partial_match(self):
        response = self.client.get(self.url, {'q': 'doe'})
        data = json.loads(response.content)

        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['username'], '@janedoe')

    def test_ajax_search_no_results(self):
        response = self.client.get(self.url, {'q': 'nonexistent'})
        data = json.loads(response.content)

        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['users']), 0)

    def test_ajax_search_excludes_current_user(self):
        response = self.client.get(self.url, {'q': 'john'})
        data = json.loads(response.content)

        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['username'], '@alicejohnson')

    def test_ajax_response_includes_gravatar(self):
        response = self.client.get(self.url, {'q': 'jane'})
        data = json.loads(response.content)

        self.assertIn('gravatar_url', data['users'][0])

    def test_ajax_response_includes_full_name(self):
        response = self.client.get(self.url, {'q': 'jane'})
        data = json.loads(response.content)

        self.assertEqual(data['users'][0]['full_name'], 'Jane Doe')

    def test_ajax_search_limits_results(self):
        for i in range(60):
            User.objects.create_user(
                username=f'@user{i}',
                email=f'user{i}@example.com',
                password='Password123'
            )

        response = self.client.get(self.url)
        data = json.loads(response.content)

        self.assertEqual(data['count'], 63)
        self.assertEqual(len(data['users']), 50)
