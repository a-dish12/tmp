from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

class DashboardTimeFilteringTests(TestCase):

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = get_user_model().objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')

        self.other_user = get_user_model().objects.get(username='@janedoe')
        times = [20, 45, 60, 90, 120]
        for t in times:
            Recipe.objects.create(
            title='test recipe ',
            description='testing recipe',
            ingredients='test eggs',
            time=t,
            meal_type='breakfast',
            author=self.other_user)
            

        self.assertNotEqual(Recipe.objects.count(), 0)

    TIME_FILTERS = (
        {"key": "under_20", "label": "Up to 20 minutes", "min": 0, "max": 20},
        {"key": "under_30", "label": "Up to 30 minutes", "min": 0, "max": 30},
        {"key": "under_45", "label": "Up to 45 minutes", "min": 0, "max": 45},
        {"key": "under_60", "label": "Up to 60 minutes", "min": 0, "max": 60},
        {"key": "over_90", "label": "90 minutes and above", "min": 90, "max": 1000},
    )

    def test_new_style_filter_time_range_0_to_20(self):
        response = self.client.get(self.url,{'time_filter':'under_20'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 1)
        
        self.assertContains(response, 'Prep time: 20 minutes')
        self.assertNotContains(response, 'Prep time: 45 minutes')
        self.assertNotContains(response, 'Prep time: 60 minutes')
        self.assertNotContains(response, 'Prep time: 90 minutes')
        self.assertNotContains(response, 'Prep time: 120 minutes')

    def test_legacy_filter_time_range_0_to_20(self):
        response = self.client.get(self.url, {'min_time':0, 'max_time':20})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 1)
        
        self.assertContains(response, 'Prep time: 20 minutes')
        self.assertNotContains(response, 'Prep time: 45 minutes')
        self.assertNotContains(response, 'Prep time: 60 minutes')
        self.assertNotContains(response, 'Prep time: 90 minutes')
        self.assertNotContains(response, 'Prep time: 120 minutes')

    def test_legacy_filter_time_range_0_to_30(self):
        response = self.client.get(self.url, {'min_time':0, 'max_time':30})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 1)
        
        self.assertContains(response, 'Prep time: 20 minutes')
        self.assertNotContains(response, 'Prep time: 45 minutes')
        self.assertNotContains(response, 'Prep time: 60 minutes')
        self.assertNotContains(response, 'Prep time: 90 minutes')
        self.assertNotContains(response, 'Prep time: 120 minutes')

    def test_legacy_filter_time_range_0_to_45(self):
        response = self.client.get(self.url, {'min_time':0, 'max_time':45})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 2)
        
        self.assertContains(response, 'Prep time: 20 minutes')
        self.assertContains(response, 'Prep time: 45 minutes')
        self.assertNotContains(response, 'Prep time: 60 minutes')
        self.assertNotContains(response, 'Prep time: 90 minutes')
        self.assertNotContains(response, 'Prep time: 120 minutes')

    def test_legacy_filter_time_range_0_to_60(self):
        response = self.client.get(self.url, {'min_time':0, 'max_time':60})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 3)
        
        self.assertContains(response, 'Prep time: 20 minutes')
        self.assertContains(response, 'Prep time: 45 minutes')
        self.assertContains(response, 'Prep time: 60 minutes')
        self.assertNotContains(response, 'Prep time: 90 minutes')
        self.assertNotContains(response, 'Prep time: 120 minutes')

    def test_legacy_filter_time_over_90(self):
        response = self.client.get(self.url, {'min_time':90, 'max_time':1000})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 2)
        
        self.assertNotContains(response, 'Prep time: 20 minutes')
        self.assertNotContains(response, 'Prep time: 45 minutes')
        self.assertNotContains(response, 'Prep time: 60 minutes')
        self.assertContains(response, 'Prep time: 90 minutes')
        self.assertContains(response, 'Prep time: 120 minutes')

    def test_all_times(self):
        response = self.client.get(self.url, {'min_time':0, 'max_time':1000})
        query_response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['recipes'].count(), 5)
        
        self.assertContains(response, 'Prep time: 20 minutes')
        self.assertContains(response, 'Prep time: 45 minutes')
        self.assertContains(response, 'Prep time: 60 minutes')
        self.assertContains(response, 'Prep time: 90 minutes')
        self.assertContains(response, 'Prep time: 120 minutes')

    def test_filter_under_20_mins_with_no_results(self):
        Recipe.objects.filter(time__range=[0, 20]).delete()
        self.assertEqual(Recipe.objects.filter(time__range=[0, 20]).count(), 0)

        response = self.client.get(self.url, {'min_time':0, 'max_time':20})
        self.assertEqual(response.context_data['recipes'].count(), 0)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes available from other users yet.')
        self.assertNotContains(response, 'Prep time: 20 minutes')
        self.assertNotContains(response, 'Prep time: 45 minutes')
        self.assertNotContains(response, 'Prep time: 60 minutes')
        self.assertNotContains(response, 'Prep time: 90 minutes')
        self.assertNotContains(response, 'Prep time: 120 minutes')