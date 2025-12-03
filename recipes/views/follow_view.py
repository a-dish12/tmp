from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
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

def user_followers(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)

    followers = User.objects.filter(
        id__in=Follow.objects.filter(following=profile_user).values("follower_id")
    )

    return render(request, "user_followers.html", {
        "profile_user": profile_user,
        "followers": followers,
    })


def user_following(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)

    following = User.objects.filter(
        id__in=Follow.objects.filter(follower=profile_user).values("following_id")
    )

    return render(request, "user_following.html", {
        "profile_user": profile_user,
        "following": following,
    })