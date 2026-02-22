from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Очистити всі колекції
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()

        # Створити команди
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Створити користувачів
        users = [
            User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel),
            User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel),
            User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc),
            User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc),
        ]

        # Створити активності
        Activity.objects.create(user=users[0], type='run', duration=30, date='2024-01-01')
        Activity.objects.create(user=users[1], type='swim', duration=45, date='2024-01-02')
        Activity.objects.create(user=users[2], type='cycle', duration=60, date='2024-01-03')
        Activity.objects.create(user=users[3], type='run', duration=25, date='2024-01-04')

        # Створити воркаути
        Workout.objects.create(name='Pushups', description='Do 20 pushups', suggested_for='all')
        Workout.objects.create(name='Situps', description='Do 30 situps', suggested_for='all')

        # Створити leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=80)

        # Створити унікальний індекс на email
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { unique: true })')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
