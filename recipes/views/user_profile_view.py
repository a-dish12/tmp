from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from recipes.models import Follow, FollowRequest, Recipe

User = get_user_model()


def user_profile(request, user_id):
    """
    Displays a user's profile page.

    This view handles both viewing one's own profile and viewing another
    user's profile, including follow status, follow requests, and the
    user's published recipes.
    """

    # Retrieve the profile user or return 404 if not found
    profile_user = get_object_or_404(User, pk=user_id)

    # Default state flags for follow logic
    is_following = False
    request_pending = False
    incoming_follow_requests = None

    if request.user.is_authenticated:
        # Viewing someone else's profile
        if request.user.id != profile_user.id:
            # Check if the current user is already following this profile
            is_following = Follow.objects.filter(
                follower=request.user,
                following=profile_user
            ).exists()

            # Check if a follow request has already been sent
            request_pending = FollowRequest.objects.filter(
                from_user=request.user,
                to_user=profile_user
            ).exists()

        # Viewing own profile: fetch incoming follow requests
        else:
            incoming_follow_requests = FollowRequest.objects.filter(
                to_user=profile_user
            )

    # Fetch all recipes created by the profile user (newest first)
    recipes = Recipe.objects.filter(
        author=profile_user
    ).order_by('-created_at')

    context = {
        'profile_user': profile_user,
        'is_following': is_following,
        'request_pending': request_pending,
        'incoming_follow_requests': incoming_follow_requests,
        'followers_count': profile_user.follower_relations.count(),
        'following_count': profile_user.following_relations.count(),
        'recipes': recipes,
    }

    return render(request, "user_profile.html", context)
