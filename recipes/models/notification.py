"""Notification model for user notifications."""
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    """Model for in-app notifications to users."""
    
    NOTIFICATION_TYPES = [
        ('report_received', 'Report Received'),
        ('report_resolved', 'Report Resolved'),
        ('content_removed', 'Content Removed'),
        ('content_hidden', 'Content Hidden'),
        ('content_restored', 'Content Restored'),
        ('warning_issued', 'Warning Issued'),
        ('follow_request', 'Follow Request'),
        ('comment_reply', 'Comment Reply'),
        ('recipe_rated', 'Recipe Rated'),
        ('general', 'General'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Optional link to related object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # URL to navigate to when clicked (optional)
    action_url = models.CharField(max_length=500, blank=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    @classmethod
    def create_report_received_notification(cls, reporter):
        return cls.objects.create(
            recipient=reporter,
            notification_type='report_received',
            title='Report Received',
            message='Thank you for your report. We will review it shortly and take appropriate action.'
        )
    
    @classmethod
    def create_report_resolved_notification(cls, reporter, action_taken, content_title):
        if action_taken in ['hidden', 'deleted']:
            message = f'Your report has been reviewed. The content "{content_title}" has been removed. Thank you for helping keep our community safe.'
        elif action_taken == 'dismissed':
            message = f'Your report has been reviewed. After investigation, we found no violation of our guidelines.'
        else:
            message = f'Your report has been reviewed and appropriate action has been taken. Thank you.'
        
        return cls.objects.create(
            recipient=reporter,
            notification_type='report_resolved',
            title='Report Resolved',
            message=message
        )
    
    @classmethod
    def create_content_removed_notification(cls, author, content_type_str, content_title, reason):
        return cls.objects.create(
            recipient=author,
            notification_type='content_removed',
            title=f'Your {content_type_str} Was Removed',
            message=f'Your {content_type_str} "{content_title}" has been removed for violating our community guidelines. Reason: {reason}'
        )
    
    @classmethod
    def create_warning_notification(cls, user, reason):
        return cls.objects.create(
            recipient=user,
            notification_type='warning_issued',
            title='Community Guidelines Warning',
            message=f'You have received a warning for violating our community guidelines. Reason: {reason}. Please review our guidelines to avoid further action.'
        )
    
    @classmethod
    def create_follow_request_notification(cls, from_user, to_user):
        from django.urls import reverse
        return cls.objects.create(
            recipient=to_user,
            notification_type='follow_request',
            title='New Follow Request',
            message=f'{from_user.username} has requested to follow you.',
            action_url=reverse('user_profile', kwargs={'user_id': from_user.id})
        )
    
    @classmethod
    def create_rating_notification(cls, rater, recipe, stars):
        from django.urls import reverse
        return cls.objects.create(
            recipient=recipe.author,
            notification_type='recipe_rated',
            title='New Recipe Rating',
            message=f'{rater.username} rated your recipe "{recipe.title}" {stars} star{"s" if stars != 1 else ""}.',
            action_url=reverse('recipe_detail', kwargs={'pk': recipe.id})
        )
    
    @classmethod
    def create_comment_notification(cls, commenter, recipe):
        from django.urls import reverse
        return cls.objects.create(
            recipient=recipe.author,
            notification_type='comment_reply',
            title='New Comment',
            message=f'{commenter.username} commented on your recipe "{recipe.title}".',
            action_url=reverse('recipe_detail', kwargs={'pk': recipe.id})
        )
