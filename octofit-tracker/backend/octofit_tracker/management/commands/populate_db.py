from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from octofit_tracker import models as app_models


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()

        # Clear existing data
        app_models.Activity.objects.all().delete()
        app_models.LeaderboardEntry.objects.all().delete()
        app_models.Workout.objects.all().delete()
        app_models.Team.objects.all().delete()
        app_models.UserProfile.objects.all().delete()
        User.objects.all().delete()

        # Create Users and profiles
        users_data = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'display_name': 'Iron Man'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'display_name': 'Captain America'},
            {'username': 'batman', 'email': 'batman@dc.com', 'display_name': 'Batman'},
            {'username': 'superman', 'email': 'superman@dc.com', 'display_name': 'Superman'},
        ]

        profiles = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='password'
            )
            profile = app_models.UserProfile.objects.create(
                user=user,
                display_name=user_data['display_name'],
                bio=f"{user_data['display_name']} is ready to track fitness.",
            )
            profiles.append(profile)

        # Create Teams and assign members
        marvel = app_models.Team.objects.create(
            name='Team Marvel',
            description='A team of Marvel heroes',
        )
        dc = app_models.Team.objects.create(
            name='Team DC',
            description='A team of DC heroes',
        )
        marvel.members.set(profiles[:2])
        dc.members.set(profiles[2:])

        # Create Activities
        app_models.Activity.objects.create(
            user=profiles[0],
            activity_type='running',
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=280,
        )
        app_models.Activity.objects.create(
            user=profiles[1],
            activity_type='cycling',
            duration_minutes=45,
            distance_km=18.0,
            calories_burned=400,
        )
        app_models.Activity.objects.create(
            user=profiles[2],
            activity_type='swimming',
            duration_minutes=60,
            distance_km=2.0,
            calories_burned=520,
        )
        app_models.Activity.objects.create(
            user=profiles[3],
            activity_type='running',
            duration_minutes=25,
            distance_km=4.0,
            calories_burned=240,
        )

        # Create Workouts
        app_models.Workout.objects.create(
            title='Morning Cardio',
            description='A quick cardio workout to start the day.',
            difficulty='easy',
            duration_minutes=20,
            exercises=['jumping jacks', 'burpees', 'mountain climbers'],
        )
        app_models.Workout.objects.create(
            title='Strength Training',
            description='Full body strength routine.',
            difficulty='medium',
            duration_minutes=40,
            exercises=['push-ups', 'squats', 'plank'],
        )

        # Create Leaderboard entries
        app_models.LeaderboardEntry.objects.create(user=profiles[0], points=120, rank=1)
        app_models.LeaderboardEntry.objects.create(user=profiles[1], points=110, rank=2)
        app_models.LeaderboardEntry.objects.create(user=profiles[2], points=100, rank=3)
        app_models.LeaderboardEntry.objects.create(user=profiles[3], points=90, rank=4)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
