from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from recipes.forms import RecipeForm

class DashboardTimeFilteringTests(TestCase):
    def setUp(self):
        self.url = reverse('dashboard')
        times = [20, 45, 60, 90, 120]
        for t in times:
            self.form_input={
            'title':'test recipe ',
            'description':'testing recipe',
            'ingredients':'test eggs',
            'time':t,
            'meal_type':'breakfast'}

            self.client.post(reverse('create_recipe'), self.form_input)

    def test_filter_time_range_0_to_20(self):
        #self.assertNotEqual(Recipe.objects.count(), 0)
        url_response = self.client.get(self.url+'?min_time=0&max_time=20')
        query_response = self.client.get(self.url, query_params={'time__range': [0, 20]})

        self.assertEqual(query_response.status_code, 302)
        self.assertEqual(url_response.content, query_response.content)
        

    def test_filter_time_range_0_to_45(self):
        '''Need to make it learn how to post recipes properly in a test(rewatch vids)'''

        before = Recipe.objects.count()
        self.client.post(reverse('create_recipe'), self.form_input)
        after =  Recipe.objects.count()
        self.assertNotEqual(before, after)
        url_response = self.client.get(self.url+'?min_time=0&max_time=45')
        query_response = self.client.get(self.url, query_params={'time__range': [0, 45]})

        self.assertEqual(query_response.status_code, 302)
        self.assertEqual(url_response.content, query_response.content)

    def test_filter_time_range_0_to_60(self):
        #self.assertNotEqual(Recipe.objects.count(), 0)
        url_response = self.client.get(self.url+'?min_time=0&max_time=60')
        query_response = self.client.get(self.url, query_params={'time__range': [0, 60]})

        self.assertEqual(query_response.status_code, 302)
        self.assertEqual(url_response.content, query_response.content)

    def test_filter_time_range_0_to_90(self):
        #self.assertNotEqual(Recipe.objects.count(), 0)
        url_response = self.client.get(self.url+'?min_time=0&max_time=90')
        query_response = self.client.get(self.url, query_params={'time__range': [0, 90]})

        self.assertEqual(query_response.status_code, 302)
        self.assertEqual(url_response.content, query_response.content)

    def test_filter_time_over_90(self):
        #self.assertNotEqual(Recipe.objects.count(), 0)
        url_response = self.client.get(self.url+'?min_time=90&max_time=1000')
        query_response = self.client.get(self.url, query_params={'time__range': [90, 1000]})

        self.assertEqual(query_response.status_code, 302)
        self.assertEqual(url_response.content, query_response.content)

    def test_all_times(self):
        #self.assertNotEqual(Recipe.objects.count(), 0)
        url_response = self.client.get(self.url+'?min_time=0&max_time=1000')
        query_response = self.client.get(self.url)

        self.assertEqual(url_response.status_code, 302)

    def test_filter_under_20_mins_with_no_results(self):
        #self.assertNotEqual(Recipe.objects.count(), 0)
        Recipe.objects.filter(time__range=[0, 20]).delete()

        url_response = self.client.get(self.url+'?min_time=0&max_time=20')
        query_response = self.client.get(self.url, query_params={'min_time': 0, 'max_time': 20})
        self.assertEqual(url_response.status_code, 302)
        self.assertEqual(url_response.content, query_response.content)