from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from recipes.models import Follow, FriendRequest

User = get_user_model()

def user_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)

    # default values
    is_following = False
    is_friend = False
    outgoing_request = None
    incoming_request = None
    incoming_friend_requests = None  # <-- initialise here

    if request.user.is_authenticated:
        # Viewing other user's profile
        if request.user.id != profile_user.id:
            # Following logic
            is_following = Follow.objects.filter(
                follower=request.user,
                following=profile_user
            ).exists()

            # Friends logic
            is_friend = request.user.friends.filter(pk=profile_user.pk).exists()

            # Friend requests between these two users
            outgoing_request = FriendRequest.objects.filter(
                from_user=request.user,
                to_user=profile_user
            ).first()

            incoming_request = FriendRequest.objects.filter(
                from_user=profile_user,
                to_user=request.user
            ).first()

        # Viewing own profile : list of all pending requests sent 
        else:
            incoming_friend_requests = FriendRequest.objects.filter(
                to_user=profile_user  
            )

    context = {
        'profile_user': profile_user,
        'is_following': is_following,
        'is_friend': is_friend,
        'outgoing_request': outgoing_request,
        'incoming_request': incoming_request,
        'incoming_friend_requests': incoming_friend_requests,
        'followers_count': profile_user.follower_relations.count(),
        'following_count': profile_user.following_relations.count(),
    }

    return render(request, "user_profile.html", context)
