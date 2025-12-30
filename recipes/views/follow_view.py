from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model

from recipes.models import Follow, FollowRequest

User = get_user_model()


@login_required
def follow_user(request, user_id):
    """
    Handles a request by the logged-in user to follow another user.

    If the target user has a private account, a follow request is created.
    Otherwise, a follow relationship is created immediately.
    """

    # The user that the current user wants to follow
    followed = get_object_or_404(User, pk=user_id)

    # Prevent users from following themselves
    if followed == request.user:
        return redirect("user_profile", user_id=user_id)

    # If the target user is private, create a follow request
    # Otherwise, create a follow relationship directly
    if followed.is_private:
        FollowRequest.objects.get_or_create(
            from_user=request.user,
            to_user=followed
        )
    else:
        Follow.objects.get_or_create(
            follower=request.user,
            following=followed
        )

    return redirect("user_profile", user_id=user_id)


@login_required
def unfollow_user(request, user_id):
    """
    Removes an existing follow relationship between the logged-in user
    and the specified user.
    """

    # The user to be unfollowed
    unfollowed = get_object_or_404(User, pk=user_id)

    # Delete any existing follow relationship
    Follow.objects.filter(
        follower=request.user,
        following=unfollowed
    ).delete()

    return redirect("user_profile", user_id=user_id)


def user_followers(request, user_id):
    """
    Displays a list of users who are following the specified user.
    """

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
    """
    Displays a list of users that the specified user is following.
    """

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
    """
    Allows a user to cancel a previously sent follow request.
    """

    to_user = get_object_or_404(User, pk=user_id)

    # Delete the follow request sent by the current user
    FollowRequest.objects.filter(
        from_user=request.user,
        to_user=to_user
    ).delete()

    return redirect("user_profile", user_id=user_id)


@login_required
def accept_follow_request(request, request_id):
    """
    Allows a user to accept an incoming follow request.

    This creates a follow relationship and removes the follow request.
    """

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
    """
    Allows a user to reject an incoming follow request.
    """

    follow_request = get_object_or_404(
        FollowRequest,
        pk=request_id,
        to_user=request.user
    )

    from_user_id = follow_request.from_user.id

    # Delete the follow request without creating a follow relationship
    follow_request.delete()
    return redirect('user_profile', user_id=request.user.id)
