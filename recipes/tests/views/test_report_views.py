"""Tests for report views."""
from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import User, Recipe, Comment, Report, Notification
from django.contrib.contenttypes.models import ContentType


class ReportRecipeViewTestCase(TestCase):
    """Test cases for reporting recipes."""
    
    fixtures = ['recipes/tests/fixtures/default_user.json', 'recipes/tests/fixtures/other_users.json']
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.admin = User.objects.create_superuser(
            username='@testadmin',
            email='testadmin@test.com',
            password='Password123',
            first_name='Admin',
            last_name='User'
        )
        
        self.recipe = Recipe.objects.create(
            author=self.user2,
            title='Test Recipe',
            description='A test recipe',
            ingredients='flour\nsugar',
            instructions='Mix\nBake',
            time=30,
            meal_type='lunch'
        )
        self.url = reverse('report_recipe', kwargs={'recipe_pk': self.recipe.pk})
    
    def test_report_recipe_url(self):
        """Test report recipe URL resolves."""
        self.assertEqual(self.url, f'/recipes/{self.recipe.pk}/report/')
    
    def test_report_recipe_requires_login(self):
        """Test that reporting requires authentication."""
        response = self.client.post(self.url, {
            'reason': 'spam',
            'description': 'This is spam'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)
    
    def test_report_recipe_creates_report(self):
        """Test successful recipe report creation."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, {
            'reason': 'spam',
            'description': 'This is spam content'
        })
        
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.first()
        self.assertEqual(report.reported_by, self.user)
        self.assertEqual(report.content_object, self.recipe)
        self.assertEqual(report.reason, 'spam')
        self.assertRedirects(response, reverse('recipe_detail', kwargs={'pk': self.recipe.pk}))
    
    def test_cannot_report_own_recipe(self):
        """Test that users cannot report their own recipes."""
        self.client.login(username='@janedoe', password='Password123')
        response = self.client.post(self.url, {
            'reason': 'spam',
            'description': 'Testing'
        })
        
        self.assertEqual(Report.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('cannot report your own' in str(m) for m in messages))
    
    def test_cannot_report_twice(self):
        """Test that users cannot report the same recipe twice."""
        self.client.login(username='@johndoe', password='Password123')
        
        # First report
        self.client.post(self.url, {
            'reason': 'spam',
            'description': 'Spam'
        })
        
        # Second report attempt
        response = self.client.post(self.url, {
            'reason': 'inappropriate',
            'description': 'Also inappropriate'
        })
        
        self.assertEqual(Report.objects.count(), 1)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('already reported' in str(m) for m in messages))
    
    def test_staff_cannot_report(self):
        """Test that staff members cannot submit reports."""
        self.client.login(username='@testadmin', password='Password123')
        response = self.client.post(self.url, {
            'reason': 'spam',
            'description': 'Testing'
        })
        
        self.assertEqual(Report.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Staff members cannot submit' in str(m) for m in messages))
    
    def test_report_creates_notification_for_reporter(self):
        """Test that reporting creates notification for the reporter."""
        self.client.login(username='@johndoe', password='Password123')
        self.client.post(self.url, {
            'reason': 'spam',
            'description': 'Spam'
        })
        
        # Reporter gets confirmation notification
        self.assertEqual(Notification.objects.filter(recipient=self.user).count(), 1)
        notif = Notification.objects.filter(recipient=self.user).first()
        self.assertEqual(notif.notification_type, 'report_received')
    
    def test_auto_hide_after_threshold(self):
        """Test that content is auto-hidden after 5 reports."""
        users = [
            self.user,
            User.objects.get(username='@petrapickles'),
            User.objects.get(username='@peterpickles'),
        ]
        
        # Create 2 more users to reach threshold of 5
        for i in range(2):
            user = User.objects.create_user(
                username=f'@user{i}',
                email=f'user{i}@test.com',
                password='Password123',
                first_name=f'User{i}',
                last_name='Test'
            )
            users.append(user)
        
        # Submit 5 reports
        for user in users:
            self.client.login(username=user.username, password='Password123')
            self.client.post(self.url, {
                'reason': 'spam',
                'description': 'Spam'
            })
        
        # Check recipe is hidden
        self.recipe.refresh_from_db()
        self.assertTrue(self.recipe.is_hidden)
    
    def test_missing_reason_shows_error(self):
        """Test that missing reason shows error."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, {
            'description': 'No reason provided'
        })
        
        self.assertEqual(Report.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('both a reason and description' in str(m) for m in messages))
    
    def test_missing_description_shows_error(self):
        """Test that missing description shows error."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, {
            'reason': 'spam'
        })
        
        self.assertEqual(Report.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('both a reason and description' in str(m) for m in messages))


class ReportCommentViewTestCase(TestCase):
    """Test cases for reporting comments."""
    
    fixtures = ['recipes/tests/fixtures/default_user.json', 'recipes/tests/fixtures/other_users.json']
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            description='A test recipe',
            ingredients='flour\nsugar',
            instructions='Mix\nBake',
            time=30,
            meal_type='lunch'
        )
        
        self.comment = Comment.objects.create(
            user=self.user2,
            recipe=self.recipe,
            text='Test comment'
        )
        self.url = reverse('report_comment', kwargs={'comment_pk': self.comment.pk})
    
    def test_report_comment_creates_report(self):
        """Test successful comment report creation."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, {
            'reason': 'offensive',
            'description': 'This is offensive'
        })
        
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.first()
        self.assertEqual(report.content_object, self.comment)
        self.assertEqual(report.reason, 'offensive')
    
    def test_cannot_report_own_comment(self):
        """Test that users cannot report their own comments."""
        self.client.login(username='@janedoe', password='Password123')
        response = self.client.post(self.url, {
            'reason': 'offensive',
            'description': 'Testing'
        })
        
        self.assertEqual(Report.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('cannot report your own' in str(m) for m in messages))
    
    def test_auto_hide_comment_after_threshold(self):
        """Test that comment is auto-hidden after 3 reports."""
        users = [
            self.user,
            User.objects.get(username='@petrapickles'),
            User.objects.get(username='@peterpickles'),
        ]
        
        # Submit 3 reports
        for user in users:
            self.client.login(username=user.username, password='Password123')
            self.client.post(self.url, {
                'reason': 'offensive',
                'description': 'Offensive'
            })
        
        # Check comment is hidden
        self.comment.refresh_from_db()
        self.assertTrue(self.comment.is_hidden)
    
    def test_report_comment_url(self):
        """Test report comment URL resolves."""
        self.assertEqual(self.url, f'/comments/{self.comment.pk}/report/')
    
    def test_report_comment_requires_login(self):
        """Test that reporting requires authentication."""
        response = self.client.post(self.url, {
            'reason': 'spam',
            'description': 'This is spam'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)
    
    def test_cannot_report_comment_twice(self):
        """Test that users cannot report the same comment twice."""
        self.client.login(username='@johndoe', password='Password123')
        
        # First report
        self.client.post(self.url, {
            'reason': 'spam',
            'description': 'This is spam'
        })
        
        # Second report
        response = self.client.post(self.url, {
            'reason': 'offensive',
            'description': 'Also offensive'
        })
        
        self.assertEqual(Report.objects.count(), 1)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('already reported' in str(m) for m in messages))
    
    def test_staff_cannot_report_comment(self):
        """Test that staff members cannot submit reports."""
        admin = User.objects.create_superuser(
            username='@testadmin2',
            email='testadmin2@test.com',
            password='Password123',
            first_name='Admin',
            last_name='User'
        )
        self.client.login(username='@testadmin2', password='Password123')
        response = self.client.post(self.url, {
            'reason': 'spam',
            'description': 'Testing'
        })
        
        self.assertEqual(Report.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Staff members cannot submit' in str(m) for m in messages))
    
    def test_comment_report_creates_notification_for_reporter(self):
        """Test that reporting creates notification for the reporter."""
        self.client.login(username='@johndoe', password='Password123')
        self.client.post(self.url, {
            'reason': 'spam',
            'description': 'Spam'
        })
        
        # Reporter gets confirmation notification
        self.assertEqual(Notification.objects.filter(recipient=self.user).count(), 1)
        notif = Notification.objects.filter(recipient=self.user).first()
        self.assertEqual(notif.notification_type, 'report_received')
    
    def test_comment_missing_reason_shows_error(self):
        """Test that missing reason shows error."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, {
            'description': 'No reason provided'
        })
        
        self.assertEqual(Report.objects.count(), 0)
    
    def test_comment_missing_description_shows_error(self):
        """Test that missing description shows error."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, {
            'reason': 'spam'
        })
        
        self.assertEqual(Report.objects.count(), 0)
