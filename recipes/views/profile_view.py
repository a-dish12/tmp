from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse
from recipes.forms import UserForm


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
