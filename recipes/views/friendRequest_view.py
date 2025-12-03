from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from recipes.models import FriendRequest 

User = get_user_model()

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, pk=user_id)

    if to_user == request.user:
        return redirect('user_profile', user_id=user_id)

    # Don't send if already friends
    if request.user.is_friends_with(to_user):
        return redirect('user_profile', user_id=user_id)

    FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=to_user,
    )
    return redirect('user_profile', user_id=user_id)


@login_required
def accept_friend_request(request, request_id):
    relation = get_object_or_404(FriendRequest, pk=request_id, to_user=request.user)

    # Make them friends
    request.user.befriend(relation.from_user)
    relation.delete()
    return redirect('user_profile', user_id=relation.from_user.id)


@login_required
def reject_friend_request(request, request_id):
    fr = get_object_or_404(FriendRequest, pk=request_id, to_user=request.user)
    fr.delete()
    return redirect('user_profile', user_id=request.user.id)


@login_required
def unfriend_user(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated and request.user != other_user:
        request.user.friends.remove(other_user)

    return redirect('user_profile', user_id=user_id)