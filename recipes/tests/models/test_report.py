"""Tests for Report model."""

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from unittest.mock import PropertyMock, patch

from recipes.models import User, Recipe, Comment, Report


class ReportModelTestCase(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

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

    def test_str_representation(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertIn('Spam or Advertising', str(report))

    def test_get_content_title_recipe(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertEqual(report.get_content_title(), 'Test Recipe')

    def test_get_content_title_comment(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.comment,
            reason='offensive',
            description='Offensive'
        )
        self.assertIn('Test comment', report.get_content_title())

    def test_get_content_title_deleted_object(self):
        ct = ContentType.objects.get_for_model(Recipe)

        report = Report.objects.create(
            reported_by=self.user,
            content_type=ct,
            object_id=9999,
            reason='other',
            description='Other'
        )

        self.assertEqual(report.get_content_title(), "[Deleted recipe]")

    def test_get_content_title_fallback_str(self):
        """Fallback to str() when object has no title or text attribute."""
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.comment,
            reason='other',
            description='Other'
        )

        class MockObject:
            def __str__(self):
                return "MockObjectString"

        with patch.object(Report, 'content_object', new_callable=PropertyMock) as mock_content:
            mock_content.return_value = MockObject()
            self.assertEqual(report.get_content_title(), "MockObjectString")

    def test_get_content_author_recipe(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertEqual(report.get_content_author(), self.user2)

    def test_get_content_author_comment(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.comment,
            reason='offensive',
            description='Offensive'
        )
        self.assertEqual(report.get_content_author(), self.user2)

    def test_get_content_author_deleted_object(self):
        ct = ContentType.objects.get_for_model(Recipe)

        report = Report.objects.create(
            reported_by=self.user,
            content_type=ct,
            object_id=99999,
            reason='spam',
            description='Spam'
        )

        self.assertIsNone(report.get_content_author())

    def test_get_content_author_no_author_or_user_attribute(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )

        class MockObject:
            pass

        with patch.object(Report, 'content_object', new_callable=PropertyMock) as mock_content:
            mock_content.return_value = MockObject()
            self.assertIsNone(report.get_content_author())

    def test_get_absolute_url_recipe(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertIn(f'/recipes/{self.recipe.pk}/', report.get_absolute_url())

    def test_get_absolute_url_comment(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.comment,
            reason='offensive',
            description='Offensive'
        )
        url = report.get_absolute_url()
        self.assertIn(f'/recipes/{self.recipe.pk}/', url)
        self.assertIn(f'#comment-{self.comment.pk}', url)

    def test_get_absolute_url_deleted_object(self):
        ct = ContentType.objects.get_for_model(Recipe)

        report = Report.objects.create(
            reported_by=self.user,
            content_type=ct,
            object_id=9999,
            reason='other',
            description='Other'
        )

        self.assertIsNone(report.get_absolute_url())

    def test_get_absolute_url_unknown_content_type(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='other',
            description='Other'
        )

        with patch.object(report.content_type, 'model', 'unknownmodel'):
            self.assertIsNone(report.get_absolute_url())

    def test_get_absolute_url_comment_type_but_comment_is_none(self):
        ct = ContentType.objects.get_for_model(Comment)

        report = Report.objects.create(
            reported_by=self.user,
            content_type=ct,
            object_id=99999,
            reason='offensive',
            description='Offensive'
        )

        self.assertIsNone(report.content_object)
        self.assertIsNone(report.get_absolute_url())

    def test_unique_together_constraint(self):
        Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )

        with self.assertRaises(IntegrityError):
            Report.objects.create(
                reported_by=self.user,
                content_object=self.recipe,
                reason='offensive',
                description='Different reason'
            )

    def test_different_users_can_report_same_content(self):
        ct = ContentType.objects.get_for_model(Recipe)

        Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )

        report2 = Report.objects.create(
            reported_by=self.user2,
            content_object=self.recipe,
            reason='offensive',
            description='Offensive'
        )

        self.assertIsNotNone(report2)
        self.assertEqual(
            Report.objects.filter(content_type=ct, object_id=self.recipe.pk).count(),
            2
        )

    def test_default_status_is_pending(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertEqual(report.status, 'pending')

    def test_default_admin_action_is_none(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='Spam'
        )
        self.assertEqual(report.admin_action, 'none')

    def test_ordering_by_created_at_descending(self):
        report1 = Report.objects.create(
            reported_by=self.user,
            content_object=self.recipe,
            reason='spam',
            description='First'
        )

        report2 = Report.objects.create(
            reported_by=self.user2,
            content_object=self.recipe,
            reason='offensive',
            description='Second'
        )

        reports = list(Report.objects.all())
        self.assertEqual(reports[0], report2)
        self.assertEqual(reports[1], report1)

    def test_all_reason_choices_in_display(self):
        reasons = [
            'spam', 'inappropriate', 'harassment',
            'offensive', 'copyright',
            'misinformation', 'other'
        ]

        for reason in reasons:
            report = Report.objects.create(
                reported_by=self.user,
                content_object=self.comment,
                reason=reason,
                description=f'Test {reason}'
            )
            self.assertIsNotNone(report.get_reason_display())
            report.delete()
