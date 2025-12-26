from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from recipes.models import Follow, FollowRequest, Recipe

User = get_user_model()

def user_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    
    # default values
    is_following = False
    request_pending = False
    incoming_follow_requests = None
    
    if request.user.is_authenticated:
        # Viewing other user's profile
        if request.user.id != profile_user.id:
            # Following logic
            is_following = Follow.objects.filter(
                follower=request.user,
                following=profile_user
            ).exists()
            request_pending = FollowRequest.objects.filter(
                from_user=request.user, 
                to_user=profile_user
            ).exists()
        # Viewing own profile: list of all pending requests sent 
        else:
            incoming_follow_requests = FollowRequest.objects.filter(
                to_user=profile_user  
            )
    
    # Get the user's recipes
    recipes = Recipe.objects.filter(author=profile_user).order_by('-created_at')
    
    context = {
        'profile_user': profile_user,
        'is_following': is_following,
        'request_pending': request_pending,
        'incoming_follow_requests': incoming_follow_requests,
        'followers_count': profile_user.follower_relations.count(),
        'following_count': profile_user.following_relations.count(),
        'recipes': recipes,  # Add recipes to context
    }
    
    return render(request, "user_profile.html", context)