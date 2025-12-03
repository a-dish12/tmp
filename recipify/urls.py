from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from recipes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('recipes/create/', views.CreateRecipeView.as_view(), name='create_recipe'),
    path('recipes/my-recipes/', views.UserRecipesView.as_view(), name='user_recipes'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('users/<int:user_id>/follow/', views.follow_user, name = 'follow_user'),
    path('users/<int:user_id>/unfollow/', views.unfollow_user, name = 'unfollow_user'),
    path("user/<int:user_id>/followers/", views.user_followers, name="user_followers"),
    path("user/<int:user_id>/following/", views.user_following, name="user_following"),
    path('user/<int:user_id>/friend-request/', views.send_friend_request, name='send_friend_request'),
    path('friend-request/<int:request_id>/accept/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-request/<int:request_id>/reject/', views.reject_friend_request, name='reject_friend_request'),
    path("user/<int:user_id>/unfriend/", views.unfriend_user, name="unfriend_user")

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
