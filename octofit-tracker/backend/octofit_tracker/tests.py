from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Activity, LeaderboardEntry, Team, UserProfile, Workout


class OctoFitTrackerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.create(user=self.user, display_name='Test User')
        self.workout = Workout.objects.create(
            title='Sample Workout',
            difficulty='easy',
            duration_minutes=20,
            exercises=['pushups', 'squats'],
        )

    def test_api_root_returns_endpoints(self):
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('workouts', response.data)
        self.assertIn('leaderboard', response.data)

    def test_userprofile_list_endpoint(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_team(self):
        url = reverse('teams-list')
        payload = {'name': 'Alpha Team', 'description': 'Fitness team'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_create_activity(self):
        url = reverse('activities-list')
        payload = {
            'user': self.profile.id,
            'activity_type': 'running',
            'duration_minutes': 35,
            'distance_km': 5.5,
            'calories_burned': 320,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)

    def test_leaderboard_entry(self):
        entry = LeaderboardEntry.objects.create(user=self.profile, points=150, rank=1)
        self.assertEqual(str(entry), 'Test User - 150 points')
