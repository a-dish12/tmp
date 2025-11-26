from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from recipes.models import Follow

User = get_user_model()

def user_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)

    #default is not following the user
    is_following = False
    if request.user.is_authenticated and request.user.id != profile_user.id:
        # if a following relation between the users exists then is_Following is true
        is_following = Follow.objects.filter(
            follower = request.user, following = profile_user
        ).exists()

    context = {
        'profile_user': profile_user,
        'is_following': is_following,
        'followers_count': profile_user.follower_relations.count(),
        'following_count': profile_user.following_relations.count()
    }

    return render(request, "user_profile.html", context)

