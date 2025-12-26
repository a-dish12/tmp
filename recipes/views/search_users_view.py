from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from recipes.models import User


@login_required
def search_users(request):
    """Display user search page with initial user list."""
    search_query = request.GET.get('search', '').strip()
    
    # Get all users except the current user
    users = User.objects.exclude(id=request.user.id).order_by('username')
    
    # Apply search filter if search query exists
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 12)  # Show 12 users per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'search_query': search_query,
    }
    
    return render(request, 'search_users.html', context)


@login_required
def search_users_ajax(request):
    """Handle AJAX requests for user search with debouncing."""
    query = request.GET.get('q', '').strip()
    
    if not query:
        # Return all users except current user if no search query
        users = User.objects.exclude(id=request.user.id).order_by('username')
    else:
        # Search in username, first name, and last name
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id).order_by('username')
    
    # Prepare user data for JSON response
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name(),
            'gravatar_url': user.mini_gravatar(),
        }
        for user in users[:50]  # Limit to 50 results
    ]
    
    return JsonResponse({
        'users': users_data,
        'count': users.count()
    })
