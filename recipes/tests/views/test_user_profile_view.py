from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Follow, FollowRequest, Recipe

User = get_user_model()


class UserProfileViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='@user1',
            email='user1@example.com',
            password='testpass123',
            first_name='User',
            last_name='One',
        )
        self.user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='testpass123',
            first_name='User',
            last_name='Two',
        )
        self.user3 = User.objects.create_user(
            username='@user3',
            email='user3@example.com',
            password='testpass123',
            first_name='User',
            last_name='Three',
        )

    def test_is_following_true_when_logged_in_user_follows_profile_user(self):
        """Test that is_following is True when user follows the profile user."""
        Follow.objects.create(follower=self.user1, following=self.user2)
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_following'])
        self.assertEqual(response.context['followers_count'], 1)
        self.assertEqual(response.context['following_count'], 0)

    def test_is_following_false_when_not_following(self):
        """Test that is_following is False when user doesn't follow the profile user."""
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_following'])
        self.assertEqual(response.context['followers_count'], 0)
        self.assertEqual(response.context['following_count'], 0)

    def test_request_pending_true_when_follow_request_sent(self):
        """Test that request_pending is True when user has sent a follow request."""
        FollowRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['request_pending'])
        self.assertFalse(response.context['is_following'])

    def test_request_pending_false_when_no_follow_request_sent(self):
        """Test that request_pending is False when no follow request exists."""
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['request_pending'])

    def test_viewing_own_profile_shows_incoming_follow_requests(self):
        """Test that viewing own profile shows incoming follow requests (line 43)."""
        # Create incoming follow requests for user1
        FollowRequest.objects.create(from_user=self.user2, to_user=self.user1)
        FollowRequest.objects.create(from_user=self.user3, to_user=self.user1)
        
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_own_profile'])
        self.assertIsNotNone(response.context['incoming_follow_requests'])
        self.assertEqual(response.context['incoming_follow_requests'].count(), 2)

    def test_viewing_own_profile_with_no_incoming_requests(self):
        """Test viewing own profile when there are no incoming follow requests."""
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_own_profile'])
        self.assertIsNotNone(response.context['incoming_follow_requests'])
        self.assertEqual(response.context['incoming_follow_requests'].count(), 0)

    def test_anonymous_user_viewing_profile(self):
        """Test that anonymous users can view profiles (branch 24->48)."""
        # Don't log in - test as anonymous user
        url = reverse('user_profile', kwargs={'user_id': self.user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_following'])
        self.assertFalse(response.context['request_pending'])
        self.assertFalse(response.context['is_own_profile'])
        self.assertIsNone(response.context['incoming_follow_requests'])

    def test_profile_shows_user_recipes(self):
        """Test that profile displays user's recipes."""
        # Create recipes for user1
        recipe1 = Recipe.objects.create(
            author=self.user1,
            title='Recipe 1',
            description='Description 1',
            ingredients='Ingredient 1',
            instructions='Instructions 1',
            time=30,
            meal_type='lunch'
        )
        recipe2 = Recipe.objects.create(
            author=self.user1,
            title='Recipe 2',
            description='Description 2',
            ingredients='Ingredient 2',
            instructions='Instructions 2',
            time=45,
            meal_type='dinner'
        )
        
        self.client.force_login(self.user2)
        url = reverse('user_profile', kwargs={'user_id': self.user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('recipes', response.context)
        self.assertEqual(response.context['recipes'].count(), 2)
        # Verify recipes are ordered by created_at descending (newest first)
        recipes_list = list(response.context['recipes'])
        self.assertEqual(recipes_list[0], recipe2)
        self.assertEqual(recipes_list[1], recipe1)

    def test_profile_with_no_recipes(self):
        """Test profile display when user has no recipes."""
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recipes'].count(), 0)

    def test_nonexistent_user_returns_404(self):
        """Test that requesting a non-existent user returns 404."""
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)

    def test_followers_and_following_counts(self):
        """Test that follower and following counts are correct."""
        # user1 follows user2
        Follow.objects.create(follower=self.user1, following=self.user2)
        # user3 follows user2
        Follow.objects.create(follower=self.user3, following=self.user2)
        # user2 follows user1
        Follow.objects.create(follower=self.user2, following=self.user1)
        
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # user2 has 2 followers (user1 and user3)
        self.assertEqual(response.context['followers_count'], 2)
        # user2 is following 1 user (user1)
        self.assertEqual(response.context['following_count'], 1)

    def test_context_contains_all_required_fields(self):
        """Test that context contains all expected fields."""
        self.client.force_login(self.user1)
        url = reverse('user_profile', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify all expected context keys exist
        expected_keys = [
            'profile_user',
            'is_following',
            'is_own_profile',
            'request_pending',
            'incoming_follow_requests',
            'followers_count',
            'following_count',
            'recipes'
        ]
        
        for key in expected_keys:
            self.assertIn(key, response.context)