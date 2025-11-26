from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model

from recipes.models import Follow

User = get_user_model()


@login_required
def follow_user(request, user_id):
    # the user to be followed 
    followed = get_object_or_404(User, pk = user_id)

    # user can not follow itself
    if followed == request.user:
        return redirect("user_profile", user_id = user_id)
    
    # if a follow relation doesnt already exist, create one
    Follow.objects.get_or_create(
        follower = request.user,
        following = followed
    )

    return redirect("user_profile", user_id = user_id)


@login_required
def unfollow_user(request, user_id):
    # the user to be unfollowed
    unfollowed = get_object_or_404(User, pk = user_id)

    #delete any following relation 
    Follow.objects.filter(
        follower = request.user,
        following = unfollowed 
    ).delete()

    return redirect("user_profile", user_id = user_id)