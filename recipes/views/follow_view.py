from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model


from recipes.models import Follow, FollowRequest

User = get_user_model()


@login_required
def follow_user(request, user_id):
    # the user to be followed 
    followed = get_object_or_404(User, pk = user_id)

    # user can not follow itself
    if followed == request.user:
        return redirect("user_profile", user_id = user_id)
    
    # if private: create request, else follow
    if followed.is_private:
        FollowRequest.objects.get_or_create(from_user = request.user, to_user = followed)
    else:
        Follow.objects.get_or_create(follower = request.user, following = followed)
    
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


@login_required
def cancel_follow_request(request, user_id):
    to_user = get_object_or_404(User, pk=user_id)
    
    FollowRequest.objects.filter(from_user=request.user, to_user=to_user).delete()
    return redirect("user_profile", user_id=user_id)

@login_required
def accept_follow_request(request, request_id):
    follow_request= get_object_or_404(FollowRequest, pk=request_id, to_user=request.user)
    from_user_id = follow_request.from_user.id
    from_user = follow_request.from_user
    to_user = follow_request.to_user

    Follow.objects.get_or_create(follower=from_user, following=to_user)
    follow_request.delete()

    return redirect('user_profile', user_id=from_user_id)

@login_required
def reject_follow_request(request, request_id):
    follow_request= get_object_or_404(FollowRequest, pk=request_id, to_user=request.user)
    from_user_id = follow_request.from_user.id
    
    follow_request.delete()
    return redirect('user_profile', user_id=request.user.id)