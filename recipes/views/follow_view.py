from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model

from recipes.models import Follow, FollowRequest, Notification

User = get_user_model()


@login_required
def follow_user(request, user_id):
    # for private accounts creates follow request, otherwise follows directly
    followed = get_object_or_404(User, pk=user_id)

    # Prevent users from following themselves
    if followed == request.user:
        return redirect("user_profile", user_id=user_id)

    # If the target user is private, create a follow request
    # Otherwise, create a follow relationship directly
    if followed.is_private:
        follow_request, created = FollowRequest.objects.get_or_create(
            from_user=request.user,
            to_user=followed
        )
        # Send notification only if this is a new request
        if created:
            Notification.create_follow_request_notification(request.user, followed)
    else:
        Follow.objects.get_or_create(
            follower=request.user,
            following=followed
        )

    return redirect("user_profile", user_id=user_id)


@login_required
def unfollow_user(request, user_id):

    # The user to be unfollowed
    unfollowed = get_object_or_404(User, pk=user_id)

    # Delete any existing follow relationship
    Follow.objects.filter(
        follower=request.user,
        following=unfollowed
    ).delete()

    return redirect("user_profile", user_id=user_id)


def user_followers(request, user_id):

    profile_user = get_object_or_404(User, pk=user_id)

    # Query all users who follow the profile user
    followers = User.objects.filter(
        id__in=Follow.objects.filter(
            following=profile_user
        ).values("follower_id")
    )

    return render(request, "user_followers.html", {
        "profile_user": profile_user,
        "followers": followers,
    })


def user_following(request, user_id):

    profile_user = get_object_or_404(User, pk=user_id)

    # Query all users that the profile user is following
    following = User.objects.filter(
        id__in=Follow.objects.filter(
            follower=profile_user
        ).values("following_id")
    )

    return render(request, "user_following.html", {
        "profile_user": profile_user,
        "following": following,
    })


@login_required
def cancel_follow_request(request, user_id):

    to_user = get_object_or_404(User, pk=user_id)

    # Delete the follow request sent by the current user
    FollowRequest.objects.filter(
        from_user=request.user,
        to_user=to_user
    ).delete()

    return redirect("user_profile", user_id=user_id)


@login_required
def accept_follow_request(request, request_id):

    follow_request = get_object_or_404(
        FollowRequest,
        pk=request_id,
        to_user=request.user
    )

    from_user_id = follow_request.from_user.id
    from_user = follow_request.from_user
    to_user = follow_request.to_user

    # Create the follow relationship
    Follow.objects.get_or_create(
        follower=from_user,
        following=to_user
    )

    # Remove the follow request after acceptance
    follow_request.delete()

    return redirect('user_profile', user_id=from_user_id)


@login_required
def reject_follow_request(request, request_id):

    follow_request = get_object_or_404(
        FollowRequest,
        pk=request_id,
        to_user=request.user
    )

    from_user_id = follow_request.from_user.id

    # Delete the follow request without creating a follow relationship
    follow_request.delete()

    return redirect('user_profile', user_id=from_user_id)
