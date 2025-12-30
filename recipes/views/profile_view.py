from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse
from recipes.forms import UserForm
from django.db import transaction
from recipes.models import FollowRequest, Follow
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows authenticated users to view and update their profile information.

    This class-based view renders a profile editing form and handles updates
    to the currently logged-in user's profile. Access is restricted to
    authenticated users via LoginRequiredMixin.
    """

    # The form used to edit the user's profile information
    form_class = UserForm

    # Template used to render the profile update page
    template_name = "profile.html"

    def get_object(self):
        """
        Returns the user object to be edited.

        This ensures that users can only update their own profile and
        prevents access to other users' profile data.

        Returns:
            User: The currently authenticated user instance.
        """
        return self.request.user

    def get_success_url(self):
        """
        Determines the redirect URL after a successful profile update.

        Adds a success message to provide user feedback after saving
        profile changes.

        Returns:
            str: URL to redirect to after a successful update.
        """
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Profile updated!"
        )
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

    def form_valid(self, form):
        """
        If the user switches from private -> public, automatically accept all
        incoming follow requests by converting them into Follow relationships.
        """
        # Old value from DB (reliable)
        was_private = User.objects.get(pk=self.request.user.pk).is_private

        # New value from the submitted form (reliable)
        becoming_public = was_private and (form.cleaned_data.get("is_private") is False)

        # IMPORTANT: accept requests BEFORE the save (in case a signal deletes them on public)
        if becoming_public:
            self._accept_all_incoming_follow_requests(self.request.user)

        return super().form_valid(form)


    def _accept_all_incoming_follow_requests(self, user):
        """
        Convert all incoming FollowRequest objects for this user into Follow
        relationships, then delete the requests.
        """
        with transaction.atomic():
            reqs = FollowRequest.objects.filter(to_user=user).select_related("from_user")

            for req in reqs:
                if req.from_user_id != user.id:
                    Follow.objects.get_or_create(
                        follower=req.from_user,
                        following=user
                    )

            reqs.delete()
