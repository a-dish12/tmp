"""Views for notifications."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from recipes.models import Notification


@login_required
def notifications_list(request):
    """Display all notifications for the current user."""
    notifications = request.user.notifications.all()[:50]  # Last 50
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications.html', context)


@login_required
def notifications_dropdown(request):
    """AJAX view for notification dropdown."""
    notifications = request.user.notifications.all()[:10]  # Last 10
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    notifications_data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message[:100],
        'is_read': n.is_read,
        'created_at': n.created_at.strftime('%b %d, %Y %I:%M %p'),
        'action_url': n.action_url or '#'
    } for n in notifications]
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count
    })


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    # Redirect to action URL if available
    if notification.action_url:
        return redirect(notification.action_url)
    return redirect('notifications_list')


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read."""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications_list')
