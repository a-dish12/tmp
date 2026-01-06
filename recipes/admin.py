from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from recipes.models import User, Recipe, Comment, Rating, Follow, FollowRequest, PlannedDay, PlannedMeal, Report, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_private']
    list_filter = ['is_staff', 'is_superuser', 'is_private']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'meal_type', 'time', 'total_views', 'is_hidden', 'created_at']
    list_filter = ['meal_type', 'is_hidden', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'total_views', 'last_viewed_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'user', 'recipe', 'is_hidden', 'created_at']
    list_filter = ['is_hidden', 'created_at']
    search_fields = ['text', 'user__username', 'recipe__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'stars', 'created_at']
    list_filter = ['stars', 'created_at']
    search_fields = ['recipe__title', 'user__username']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_preview', 'reported_by', 'reason', 'status', 'admin_action', 'created_at', 'view_content_link']
    list_filter = ['status', 'admin_action', 'reason', 'content_type', 'created_at']
    search_fields = ['reported_by__username', 'description']
    readonly_fields = ['reported_by', 'content_type', 'object_id', 'created_at', 'view_content_link', 'content_details', 'reason', 'report_description', 'reviewed_by', 'reviewed_at']
    actions = ['bulk_dismiss_reports', 'bulk_hide_content', 'bulk_delete_content']
    
    # Hide the "save and add another" and "save and continue editing" buttons
    def has_add_permission(self, request):
        return False
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
    fieldsets = (
        ('Report Information', {
            'fields': ('reported_by', 'created_at', 'content_type', 'object_id', 'content_details', 'view_content_link')
        }),
        ('Report Details', {
            'fields': ('reason', 'report_description')
        }),
        ('Admin Review - Take Action Here', {
            'fields': ('status', 'admin_action', 'resolution_notes', 'reviewed_by', 'reviewed_at'),
            'classes': ('wide',),
            'description': 'Change the status to "Resolved" and select an action from the dropdown to handle this report. Once resolved, this report cannot be edited again.'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.status in ['resolved', 'dismissed']:
            # lock resolved reports to prevent tampering with decisions
            return readonly + ['status', 'admin_action', 'resolution_notes']
        return readonly
    
    def report_description(self, obj):
        return obj.description
    report_description.short_description = 'Description'
    
    def bulk_dismiss_reports(self, request, queryset):
        pending_reports = queryset.filter(status='pending')
        count = 0
        for report in pending_reports:
            report.status = 'dismissed'
            report.admin_action = 'dismissed'
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            report.save()
            
            # Notify reporter
            Notification.create_report_resolved_notification(
                report.reported_by,
                report.admin_action,
                report.get_content_title()
            )
            count += 1
        self.message_user(request, f"Dismissed {count} report(s).")
    bulk_dismiss_reports.short_description = "Dismiss selected reports"
    
    def bulk_hide_content(self, request, queryset):
        """bulk action to hide content and notify both reporter and author"""
        pending_reports = queryset.filter(status='pending')
        count = 0
        for report in pending_reports:
            content_title = report.get_content_title()
            content_author = report.get_content_author()
            content_object = report.content_object
            
            report.status = 'resolved'
            report.admin_action = 'hidden'
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            report.save()
            
            # set is_hidden flag on the content
            if content_object:
                content_object.is_hidden = True
                content_object.save()
            
            # Notify reporter and author
            Notification.create_report_resolved_notification(
                report.reported_by,
                report.admin_action,
                content_title
            )
            if content_author:
                Notification.create_content_removed_notification(
                    content_author,
                    report.content_type.model,
                    content_title,
                    report.get_reason_display()
                )
            count += 1
        self.message_user(request, f"Hidden content from {count} report(s).")
    bulk_hide_content.short_description = "Hide content from selected reports"
    
    def bulk_delete_content(self, request, queryset):
        """bulk action to permanently delete content and notify both parties"""
        pending_reports = queryset.filter(status='pending')
        count = 0
        for report in pending_reports:
            content_title = report.get_content_title()
            content_author = report.get_content_author()
            content_object = report.content_object
            
            report.status = 'resolved'
            report.admin_action = 'deleted'
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            report.save()
            
            # permanently remove the content
            if content_object:
                content_object.delete()
            
            # Notify reporter and author
            Notification.create_report_resolved_notification(
                report.reported_by,
                report.admin_action,
                content_title
            )
            if content_author:
                Notification.create_content_removed_notification(
                    content_author,
                    report.content_type.model,
                    content_title,
                    report.get_reason_display()
                )
            count += 1
        self.message_user(request, f"Deleted content from {count} report(s).")
    bulk_delete_content.short_description = "Delete content from selected reports"
    
    def content_preview(self, obj):
        """Show preview of reported content."""
        title = obj.get_content_title()
        if obj.content_type.model == 'recipe':
            return format_html('<span style="color: #ff8a65;">🍳 {}</span>', title)
        elif obj.content_type.model == 'comment':
            return format_html('<span style="color: #64b5f6;">💬 {}</span>', title)
        return title
    content_preview.short_description = 'Content'
    
    def view_content_link(self, obj):
        """Provide link to view the reported content."""
        url = obj.get_absolute_url()
        if url:
            return format_html('<a href="{}" target="_blank" class="button">View Content →</a>', url)
        return '-'
    view_content_link.short_description = 'View Reported Content'
    
    def content_details(self, obj):
        """Show detailed information about the reported content."""
        author = obj.get_content_author()
        content_type = obj.content_type.model.capitalize()
        content_title = obj.get_content_title()
        
        details = f"<strong>Type:</strong> {content_type}<br>"
        details += f"<strong>Title/Text:</strong> {content_title}<br>"
        
        if not obj.content_object:
            details += f"<strong>Status:</strong> <span style='color: red;'>Content has been deleted</span><br>"
        elif author:
            details += f"<strong>Author:</strong> {author.username}<br>"
        
        # Count total reports for this content
        report_count = Report.objects.filter(
            content_type=obj.content_type,
            object_id=obj.object_id
        ).count()
        details += f"<strong>Total Reports:</strong> {report_count}"
        
        return format_html(details)
    content_details.short_description = 'Content Details'
    
    def save_model(self, request, obj, form, change):
        """handles report resolution, sends notifications and executes admin actions"""
        if change:
            old_status = Report.objects.get(pk=obj.pk).status
            
            # when report moves from pending to resolved/dismissed
            if old_status == 'pending' and obj.status in ['resolved', 'dismissed']:
                obj.reviewed_by = request.user
                obj.reviewed_at = timezone.now()
                
                # grab content details before possible deletion
                content_title = obj.get_content_title()
                content_author = obj.get_content_author()
                content_type_str = obj.content_type.model
                content_object = obj.content_object
                
                # save report before deleting content to preserve report record
                super().save_model(request, obj, form, change)
                
                # let reporter know their report was handled
                Notification.create_report_resolved_notification(
                    obj.reported_by,
                    obj.admin_action,
                    content_title
                )
                
                # notify author if their content was hidden or deleted
                if content_author and obj.admin_action in ['hidden', 'deleted']:
                    Notification.create_content_removed_notification(
                        content_author,
                        content_type_str,
                        content_title,
                        obj.get_reason_display()
                    )
                    
                    # Actually hide/delete the content AFTER saving report
                    if obj.admin_action == 'hidden' and content_object:
                        content_object.is_hidden = True
                        content_object.save()
                    elif obj.admin_action == 'deleted' and content_object:
                        content_object.delete()
                
                # If author was warned
                if content_author and obj.admin_action == 'warned':
                    Notification.create_warning_notification(
                        content_author,
                        obj.get_reason_display()
                    )
                
                return  # Already saved above
        
        # Normal save for non-resolved reports
        super().save_model(request, obj, form, change)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username']
    readonly_fields = ['created_at']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']


@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'created_at']
    search_fields = ['from_user__username', 'to_user__username']


@admin.register(PlannedDay)
class PlannedDayAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    list_filter = ['date']
    search_fields = ['user__username']


@admin.register(PlannedMeal)
class PlannedMealAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'planned_day', 'meal_type']
    list_filter = ['meal_type']
    search_fields = ['recipe__title', 'planned_day__user__username']
