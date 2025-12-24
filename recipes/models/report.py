"""Report model for content moderation."""
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Report(models.Model):
    """Model for user-submitted reports of inappropriate content."""
    
    REASON_CHOICES = [
        ('spam', 'Spam or Advertising'),
        ('inappropriate', 'Inappropriate Content'),
        ('harassment', 'Harassment or Bullying'),
        ('offensive', 'Offensive Language'),
        ('copyright', 'Copyright Violation'),
        ('misinformation', 'False or Misleading Information'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    ACTION_CHOICES = [
        ('none', 'No Action Taken'),
        ('dismissed', 'Report Dismissed'),
        ('hidden', 'Content Hidden'),
        ('deleted', 'Content Deleted'),
        ('warned', 'Author Warned'),
        ('banned', 'Author Banned'),
    ]
    
    # Reporter information
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_submitted'
    )
    
    # Generic relation to reported content (Recipe or Comment)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Report details
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(help_text="Please provide details about why you're reporting this content")
    
    # Status and review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Admin review fields
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_reviewed'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_action = models.CharField(max_length=20, choices=ACTION_CHOICES, default='none')
    resolution_notes = models.TextField(blank=True, help_text="Admin notes about the decision")
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['reported_by', 'content_type', 'object_id']  # One report per user per content
    
    def __str__(self):
        return f"Report #{self.id} - {self.get_reason_display()} by {self.reported_by.username}"
    
    def get_content_title(self):
        """Get a displayable title for the reported content."""
        if not self.content_object:
            return f"[Deleted {self.content_type.model}]"
        if hasattr(self.content_object, 'title'):
            return self.content_object.title
        elif hasattr(self.content_object, 'text'):
            return self.content_object.text[:50] + '...'
        return str(self.content_object)
    
    def get_content_author(self):
        """Get the author of the reported content."""
        if not self.content_object:
            return None
        if hasattr(self.content_object, 'author'):
            return self.content_object.author
        elif hasattr(self.content_object, 'user'):
            return self.content_object.user
        return None
    
    def get_absolute_url(self):
        """Get URL to view the reported content."""
        if not self.content_object:
            return None
        from django.urls import reverse
        if self.content_type.model == 'recipe':
            return reverse('recipe_detail', kwargs={'pk': self.object_id})
        elif self.content_type.model == 'comment':
            comment = self.content_object
            if comment:
                return reverse('recipe_detail', kwargs={'pk': comment.recipe.pk}) + f'#comment-{comment.pk}'
        return None
