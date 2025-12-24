"""Tests for Report model."""
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from recipes.models import User, Recipe, Comment, Report


class ReportModelTestCase(TestCase):
    """Test cases for Report model."""
    
    fixtures = ['recipes/tests/fixtures/default_user.json', 'recipes/tests/fixtures/other_users.json']
    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        
        self.recipe = Recipe.objects.create(
            author=self.user2,
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
    
    def test_create_recipe_report(self):
        """Test creating a report for a recipe."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='This is spam content'
        )
        self.assertEqual(report.reported_by, self.user)
        self.assertEqual(report.content_object, self.recipe)
        self.assertEqual(report.reason, 'spam')
        self.assertEqual(report.status, 'pending')
    
    def test_create_comment_report(self):
        """Test creating a report for a comment."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.comment,
            reason='harassment',
            description='This is harassment'
        )
        self.assertEqual(report.content_object, self.comment)
        self.assertEqual(report.content_type.model, 'comment')
    
    def test_report_str_representation(self):
        """Test string representation of report."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        expected = f"Report #{report.id} - Spam or Advertising by @johndoe"
        self.assertEqual(str(report), expected)
    
    def test_get_content_title_for_recipe(self):
        """Test getting title for recipe report."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertEqual(report.get_content_title(), 'Test Recipe')
    
    def test_get_content_title_for_comment(self):
        """Test getting title for comment report."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.comment,
            reason='offensive',
            description='Offensive'
        )
        self.assertTrue('Test comment' in report.get_content_title())
    
    def test_get_content_author_for_recipe(self):
        """Test getting author for recipe report."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertEqual(report.get_content_author(), self.user2)
    
    def test_get_content_author_for_comment(self):
        """Test getting author for comment report."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.comment,
            reason='offensive',
            description='Offensive'
        )
        self.assertEqual(report.get_content_author(), self.user2)
    
    def test_get_absolute_url_for_recipe(self):
        """Test getting URL for recipe report."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        url = report.get_absolute_url()
        self.assertIn(f'/recipes/{self.recipe.pk}/', url)
    
    def test_get_absolute_url_for_comment(self):
        """Test getting URL for comment report."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.comment,
            reason='offensive',
            description='Offensive'
        )
        url = report.get_absolute_url()
        self.assertIn(f'/recipes/{self.recipe.pk}/', url)
        self.assertIn(f'#comment-{self.comment.pk}', url)
    
    def test_unique_report_per_user_per_content(self):
        """Test that a user can only report the same content once."""
        Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        
        with self.assertRaises(Exception):
            Report.objects.create(
                reported_by=self.user,
                content_object=self.recipe,
                reason='inappropriate',
                description='Also inappropriate'
            )
    
    def test_multiple_users_can_report_same_content(self):
        """Test that multiple users can report the same content."""
        Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        
        user3 = User.objects.get(username='@petrapickles')
        report2 = Report.objects.create(
            reported_by=user3,
            content_object=self.recipe,
            reason='inappropriate',
            description='Inappropriate'
        )
        
        self.assertEqual(Report.objects.filter(object_id=self.recipe.pk).count(), 2)
    
    def test_default_status_is_pending(self):
        """Test that default status is pending."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertEqual(report.status, 'pending')
    
    def test_default_admin_action_is_none(self):
        """Test that default admin action is none."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertEqual(report.admin_action, 'none')
    
    def test_report_ordering_by_created_at_desc(self):
        """Test that reports are ordered by created_at descending."""
        report1 = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        
        user3 = User.objects.get(username='@petrapickles')
        comment2 = Comment.objects.create(
            user=self.user2,
            recipe=self.recipe,
            text='Another comment'
        )
        report2 = Report.objects.create(
            reported_by=user3,
            content_object=comment2,
            reason='offensive',
            description='Offensive'
        )
        
        reports = list(Report.objects.all())
        self.assertEqual(reports[0], report2)
        self.assertEqual(reports[1], report1)
