from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import random

from api.models import User, Poses, PoseSelection, Export


class Command(BaseCommand):
    help = "Seed basic user + pose system with admin and regular users"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true")

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding started...")

        now = timezone.now()

        # -------------------
        # RESET (optional)
        # -------------------
        if kwargs.get("reset"):
            self.stdout.write("Clearing data...")
            Export.objects.all().delete()
            PoseSelection.objects.all().delete()
            Poses.objects.all().delete()
            User.objects.all().delete()

        # -------------------
        # CREATE ADMIN USER
        # -------------------
        admin_user, created = User.objects.get_or_create(
            user_name="admin",
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "password": make_password("admin123"),
                "email_address": "admin@trabby.local",
                "is_permitted": 1,
                "is_admin": True,
                "created_at": now,
                "updated_at": now,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Admin user created:\n"
                    f"  Username: admin\n"
                    f"  Password: admin123"
                )
            )
        else:
            self.stdout.write("  Admin user already exists")

        # -------------------
        # CREATE REGULAR USERS
        # -------------------
        existing_users = list(User.objects.all())
        
        for i in range(1, 6):
            user_name = f"user{i}"
            if not User.objects.filter(user_name=user_name).exists():
                user = User.objects.create(
                    first_name=f"User{i}",
                    last_name=f"Test{i}",
                    user_name=user_name,
                    password=make_password("password123"),
                    email_address=f"user{i}@example.com",
                    is_permitted=1 if i % 2 == 0 else 0,
                    is_admin=False,
                    created_at=now,
                    updated_at=now,
                )
                existing_users.append(user)

        users = list(User.objects.all())

        # -------------------
        # POSES
        # -------------------
        Poses.objects.bulk_create([
            Poses(
                poses_fid=random.choice(users),
                name_of_poses_generated=f"Pose {i}",
                configuration={
                    "style": random.choice(["happy", "neutral", "dynamic", "idle"]),
                    "intensity": random.randint(1, 10),
                    "mirror": random.choice([True, False]),
                },
                created_at=now,
            )
            for i in range(10)
            if Poses.objects.count() < 10  # Avoid duplicates on re-run
        ])

        poses = list(Poses.objects.all())

        # -------------------
        # POSE SELECTIONS
        # -------------------
        for pose in poses:
            if not PoseSelection.objects.filter(pose_selection_fid=pose).exists():
                PoseSelection.objects.create(
                    pose_selection_fid=pose,
                    selected_at=now,
                )

        # -------------------
        # EXPORTS
        # -------------------
        for pose in poses[:5]:
            if not Export.objects.filter(export_fid=pose).exists():
                Export.objects.create(
                    export_fid=pose,
                    created_at=now,
                )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))