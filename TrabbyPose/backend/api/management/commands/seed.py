from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import random

from api.models import User, Poses, PoseSelection, Export


class Command(BaseCommand):
    help = "Seed basic user + pose system"

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
        # USERS
        # -------------------
        User.objects.bulk_create([
            User(
                first_name=f"User{i}",
                last_name=f"Test{i}",
                user_name=f"user{i}",
                password=make_password("password123"),
                email_address=f"user{i}@example.com",
                is_permitted=1 if i % 2 == 0 else 0,
                created_at=now,
                updated_at=now,
            )
            for i in range(1, 6)
        ])

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
        ])

        poses = list(Poses.objects.all())

        # -------------------
        # POSE SELECTIONS
        # -------------------
        PoseSelection.objects.bulk_create([
            PoseSelection(
                pose_selection_fid=pose,
                selected_at=now,
            )
            for pose in poses
        ])

        # -------------------
        # EXPORTS
        # -------------------
        Export.objects.bulk_create([
            Export(
                export_fid=pose,
                created_at=now,
            )
            for pose in poses[:5]
        ])

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))