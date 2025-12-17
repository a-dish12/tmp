from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Follow

class DashboardFollowingViewTests(TestCase):
    
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.url = reverse('following_dashboard')
        #Logged in user
        self.user = get_user_model().objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')

        self.followed_user = get_user_model().objects.get(username='@janedoe')
        self.not_followed_user = get_user_model().objects.get(username='@petrapickles')

        Follow.objects.create(
            follower=self.user,
            following=self.followed_user
        )

        Recipe.objects.create(
            title='Apple Pie',
            description='test description',
            ingredients='test ingredients',
            time=50,
            meal_type='dessert',
            author=self.followed_user)

        Recipe.objects.create(
            title='Spaghetti Bolognese',
            description='test description',
            ingredients='test ingredients',
            time=20,
            meal_type='dinner',
            author=self.not_followed_user)

    def test_following_dashboard_url(self):
        self.assertEqual(self.url,'/dashboard/following/')

    #Retrieving the following dashboard
    def test_get_following_dashboard(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(response.context_data['following_page'], True)
        self.assertEqual(response.context_data['recipes'].count(), 1)
        self.assertContains(response, 'Apple Pie')
        self.assertNotContains(response, 'Spaghetti Bolognese')

    #Retrieving the For You dashboard
    def test_get_general_dashboard(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(response.context_data['following_page'], False)
        self.assertEqual(response.context_data['recipes'].count(), 2)
        self.assertContains(response, 'Apple Pie')
        self.assertContains(response, 'Spaghetti Bolognese')

    #Testing Time filters on following dashboard
    def test_time_filter_on_following_dashboard_results(self):
        response = self.client.get(self.url, {'time_filter': 'under_60'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 1)
        
        self.assertContains(response, 'Apple Pie')
        self.assertNotContains(response, 'Spaghetti Bolognese')

    def test_time_filter_on_following_dashboard_no_results(self):
        response = self.client.get(self.url, {'time_filter': 'under_30'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 0)
        
        self.assertNotContains(response, 'Apple Pie')
        self.assertNotContains(response, 'Spaghetti Bolognese')

    #Testing Meal Type filters on following dashboard
    def test_meal_type_filter_on_following_dashboard_results(self):
        response = self.client.get(self.url, {'meal_type': 'dessert'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 1)
        
        self.assertContains(response, 'Apple Pie')
        self.assertNotContains(response, 'Spaghetti Bolognese')

    def test_meal_type_filter_on_following_dashboard_no_results(self):
        response = self.client.get(self.url, {'meal_type': 'dinner'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 0)
        
        self.assertNotContains(response, 'Apple Pie')
        self.assertNotContains(response, 'Spaghetti Bolognese')

    #Testing Search filters on following dashboard
    def test_search_filter_on_following_dashboard_results(self):
        response = self.client.get(self.url, {'search': 'app'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 1)
        
        self.assertContains(response, 'Apple Pie')
        self.assertNotContains(response, 'Spaghetti Bolognese')

    def test_search_filter_on_following_dashboard_no_results(self):
        response = self.client.get(self.url, {'search': 'spa'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 0)
        
        self.assertNotContains(response, 'Apple Pie')
        self.assertNotContains(response, 'Spaghetti Bolognese')