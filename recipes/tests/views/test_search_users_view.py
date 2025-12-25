from django.test import TestCase
from django.urls import reverse
from recipes.models import User
import json


class SearchUsersViewTestCase(TestCase):
    """Tests for the user search page and functionality."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('search_users')
        
        # Create additional test users
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
        """Test that search users URL resolves correctly."""
        self.assertEqual(self.url, '/search-users/')

    def test_search_users_requires_login(self):
        """Test that search users page requires authentication."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/log_in/?next={self.url}')

    def test_search_users_page_loads(self):
        """Test that search users page loads successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_users.html')

    def test_search_users_displays_search_bar(self):
        """Test that search page displays search input."""
        response = self.client.get(self.url)
        self.assertContains(response, 'id="userSearchInput"')
        self.assertContains(response, 'Search by username or name')

    def test_search_users_excludes_current_user(self):
        """Test that current user is excluded from results."""
        response = self.client.get(self.url)
        users = response.context['users']
        
        self.assertNotIn(self.user, users)
        self.assertIn(self.user2, users)
        self.assertIn(self.user3, users)
        self.assertIn(self.user4, users)

    def test_search_users_displays_all_other_users(self):
        """Test that all users except current are displayed."""
        response = self.client.get(self.url)
        
        self.assertContains(response, '@janedoe')
        self.assertContains(response, '@bobsmith')
        self.assertContains(response, '@alicejohnson')
        self.assertNotContains(response, '@johndoe')

    def test_search_users_displays_view_profile_links(self):
        """Test that each user card has a view profile link."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'View Profile')
        self.assertContains(response, f'/users/{self.user2.id}/')
        self.assertContains(response, f'/users/{self.user3.id}/')


class SearchUsersAjaxTestCase(TestCase):
    """Tests for AJAX user search functionality."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.ajax_url = reverse('search_users_ajax')
        
        # Create test users
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
        """Test that AJAX search requires authentication."""
        self.client.logout()
        response = self.client.get(self.ajax_url)
        self.assertEqual(response.status_code, 302)

    def test_ajax_search_returns_json(self):
        """Test that AJAX endpoint returns JSON response."""
        response = self.client.get(self.ajax_url)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_ajax_search_no_query_returns_all_users(self):
        """Test that empty query returns all users except current."""
        response = self.client.get(self.ajax_url)
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['users']), 3)

    def test_ajax_search_by_username(self):
        """Test searching users by username."""
        response = self.client.get(self.ajax_url, {'q': 'jane'})
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['username'], '@janedoe')

    def test_ajax_search_by_first_name(self):
        """Test searching users by first name."""
        response = self.client.get(self.ajax_url, {'q': 'Bob'})
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['first_name'], 'Bob')

    def test_ajax_search_by_last_name(self):
        """Test searching users by last name."""
        response = self.client.get(self.ajax_url, {'q': 'Smith'})
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['last_name'], 'Smith')

    def test_ajax_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        response = self.client.get(self.ajax_url, {'q': 'ALICE'})
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['first_name'], 'Alice')

    def test_ajax_search_partial_match(self):
        """Test that search matches partial strings."""
        response = self.client.get(self.ajax_url, {'q': 'doe'})
        data = json.loads(response.content)
        
        # Should match both janedoe and johndoe (but johndoe is excluded)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['username'], '@janedoe')

    def test_ajax_search_no_results(self):
        """Test search with no matching results."""
        response = self.client.get(self.ajax_url, {'q': 'nonexistent'})
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['users']), 0)

    def test_ajax_search_excludes_current_user(self):
        """Test that current user is never in search results."""
        response = self.client.get(self.ajax_url, {'q': 'john'})
        data = json.loads(response.content)
        
        # Should match johndoe and alicejohnson, but johndoe is excluded
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['users'][0]['username'], '@alicejohnson')

    def test_ajax_response_includes_gravatar(self):
        """Test that AJAX response includes gravatar URL."""
        response = self.client.get(self.ajax_url, {'q': 'jane'})
        data = json.loads(response.content)
        
        self.assertIn('gravatar_url', data['users'][0])
        self.assertIsNotNone(data['users'][0]['gravatar_url'])

    def test_ajax_response_includes_full_name(self):
        """Test that AJAX response includes full name."""
        response = self.client.get(self.ajax_url, {'q': 'jane'})
        data = json.loads(response.content)
        
        self.assertEqual(data['users'][0]['full_name'], 'Jane Doe')

    def test_ajax_search_limits_results(self):
        """Test that AJAX search limits results to 50 users."""
        # Create 60 users
        for i in range(60):
            User.objects.create_user(
                username=f'@user{i}',
                email=f'user{i}@example.com',
                password='Password123',
                first_name=f'User{i}',
                last_name='Test'
            )
        
        response = self.client.get(self.ajax_url)
        data = json.loads(response.content)
        
        # Should have 63 total users but return max 50
        self.assertEqual(data['count'], 63)
        self.assertEqual(len(data['users']), 50)
