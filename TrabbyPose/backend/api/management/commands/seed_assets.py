"""
Django management command to seed the database with initial puppet assets,
preset poses, expressions, and their configurations.

Usage:
    python manage.py seed_assets
    python manage.py seed_assets --clear  (to clear and reseed)
"""

from typing import Dict, List, Tuple
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import PuppetPart, PosePreset, PartConfiguration


class Command(BaseCommand):
    """
    Management command to seed initial database with puppet assets
    and preset configurations.
    """

    help = "Seed the database with initial puppet parts, poses, and expressions"

    def add_arguments(self, parser):
        """Define command-line arguments."""
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Execute the seeding operation."""
        if options["clear"]:
            self._clear_existing_data()

        try:
            self._seed_puppet_parts()
            self._seed_body_poses()
            self._seed_expressions()
            self.stdout.write(
                self.style.SUCCESS("✓ Database seeded successfully!")
            )
        except Exception as e:
            raise CommandError(f"Seeding failed: {str(e)}")

    def _clear_existing_data(self):
        """Clear all puppet-related data from database."""
        self.stdout.write("Clearing existing data...")
        PartConfiguration.objects.all().delete()
        PosePreset.objects.all().delete()
        PuppetPart.objects.all().delete()
        self.stdout.write(self.style.WARNING("✓ Existing data cleared"))

    def _seed_puppet_parts(self):
        """Create initial puppet parts/assets."""
        self.stdout.write("Seeding puppet parts...")

        parts_data: List[Dict] = [
            # Head Parts
            {
                "name": "Round Head",
                "part_type": PuppetPart.PartType.HEAD,
                "asset_url": "/assets/trabby/sprites/head_round.svg",
                "description": "A friendly round head for Trabby"
            },
            {
                "name": "Square Head",
                "part_type": PuppetPart.PartType.HEAD,
                "asset_url": "/assets/trabby/sprites/head_square.svg",
                "description": "A bold square-shaped head"
            },
            # Torso Parts
            {
                "name": "Standard Torso",
                "part_type": PuppetPart.PartType.TORSO,
                "asset_url": "/assets/trabby/sprites/torso_standard.svg",
                "description": "Standard rectangular torso"
            },
            {
                "name": "Athletic Torso",
                "part_type": PuppetPart.PartType.TORSO,
                "asset_url": "/assets/trabby/sprites/torso_athletic.svg",
                "description": "More muscular torso variant"
            },
            # Limb Parts (Arms & Legs)
            {
                "name": "Left Arm Up",
                "part_type": PuppetPart.PartType.LIMB,
                "asset_url": "/assets/trabby/sprites/arm_left_up.svg",
                "description": "Left arm raised upward"
            },
            {
                "name": "Right Arm Up",
                "part_type": PuppetPart.PartType.LIMB,
                "asset_url": "/assets/trabby/sprites/arm_right_up.svg",
                "description": "Right arm raised upward"
            },
            {
                "name": "Left Arm Down",
                "part_type": PuppetPart.PartType.LIMB,
                "asset_url": "/assets/trabby/sprites/arm_left_down.svg",
                "description": "Left arm at rest"
            },
            {
                "name": "Right Arm Down",
                "part_type": PuppetPart.PartType.LIMB,
                "asset_url": "/assets/trabby/sprites/arm_right_down.svg",
                "description": "Right arm at rest"
            },
            {
                "name": "Left Leg",
                "part_type": PuppetPart.PartType.LIMB,
                "asset_url": "/assets/trabby/sprites/leg_left.svg",
                "description": "Left leg"
            },
            {
                "name": "Right Leg",
                "part_type": PuppetPart.PartType.LIMB,
                "asset_url": "/assets/trabby/sprites/leg_right.svg",
                "description": "Right leg"
            },
            # Face Elements (Eyes, Mouth, Eyebrows)
            {
                "name": "Eyes Neutral",
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/eyes_neutral.svg",
                "description": "Neutral expression eyes"
            },
            {
                "name": "Eyes Happy",
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/eyes_happy.svg",
                "description": "Happy expression eyes (closed, smiling)"
            },
            {
                "name": "Eyes Surprised",
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/eyes_surprised.svg",
                "description": "Surprised expression eyes (wide open)"
            },
            {
                "name": "Eyes Confident",
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/eyes_confident.svg",
                "description": "Confident expression eyes (determined)"
            },
            {
                "name": "Mouth Neutral",
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/mouth_neutral.svg",
                "description": "Neutral mouth"
            },
            {
                "name": "Mouth Smile",
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/mouth_smile.svg",
                "description": "Happy smile"
            },
            {
                "name": "Mouth Open",
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/mouth_open.svg",
                "description": "Surprised open mouth"
            },
            # Extra Parts
            {
                "name": "Thumbs Up Hand",
                "part_type": PuppetPart.PartType.EXTRA,
                "asset_url": "/assets/trabby/sprites/hand_thumbs_up.svg",
                "description": "Hand giving thumbs up gesture"
            },
            {
                "name": "Pointing Hand",
                "part_type": PuppetPart.PartType.EXTRA,
                "asset_url": "/assets/trabby/sprites/hand_pointing.svg",
                "description": "Hand pointing forward"
            },
        ]

        for part_data in parts_data:
            part, created = PuppetPart.objects.get_or_create(
                name=part_data["name"],
                part_type=part_data["part_type"],
                defaults={
                    "asset_url": part_data["asset_url"],
                    "description": part_data.get("description", "")
                }
            )
            if created:
                self.stdout.write(f"  ✓ Created: {part.name}")
            else:
                self.stdout.write(f"  • Exists: {part.name}")

    def _seed_body_poses(self):
        """Create preset body poses."""
        self.stdout.write("Seeding body poses...")

        # Fetch puppet parts (assume they exist from previous seed)
        parts = {
            part.name: part
            for part in PuppetPart.objects.all()
        }

        poses_data: List[Dict] = [
            {
                "name": "Neutral",
                "slug": "neutral",
                "description": "Character standing in neutral pose with arms at sides",
                "is_expression": False,
                "parts": [
                    ("Round Head", {"x": 200, "y": 100, "rotation": 0, "z": 5}),
                    ("Standard Torso", {"x": 200, "y": 180, "rotation": 0, "z": 4}),
                    ("Left Arm Down", {"x": 160, "y": 200, "rotation": 0, "z": 3}),
                    ("Right Arm Down", {"x": 240, "y": 200, "rotation": 0, "z": 3}),
                    ("Left Leg", {"x": 190, "y": 280, "rotation": 0, "z": 2}),
                    ("Right Leg", {"x": 210, "y": 280, "rotation": 0, "z": 2}),
                ]
            },
            {
                "name": "Thumbs Up",
                "slug": "thumbs-up",
                "description": "Character giving enthusiastic thumbs up with right hand",
                "is_expression": False,
                "parts": [
                    ("Round Head", {"x": 200, "y": 100, "rotation": 0, "z": 5}),
                    ("Standard Torso", {"x": 200, "y": 180, "rotation": 0, "z": 4}),
                    ("Left Arm Down", {"x": 160, "y": 200, "rotation": 0, "z": 3}),
                    ("Right Arm Up", {"x": 240, "y": 120, "rotation": 0, "z": 3}),
                    ("Thumbs Up Hand", {"x": 250, "y": 80, "rotation": 0, "z": 2}),
                    ("Left Leg", {"x": 190, "y": 280, "rotation": 0, "z": 1}),
                    ("Right Leg", {"x": 210, "y": 280, "rotation": 0, "z": 1}),
                ]
            },
            {
                "name": "Pointing",
                "slug": "pointing",
                "description": "Character pointing forward with right hand",
                "is_expression": False,
                "parts": [
                    ("Round Head", {"x": 200, "y": 100, "rotation": 0, "z": 5}),
                    ("Standard Torso", {"x": 200, "y": 180, "rotation": 0, "z": 4}),
                    ("Left Arm Down", {"x": 160, "y": 200, "rotation": 0, "z": 3}),
                    ("Right Arm Up", {"x": 260, "y": 160, "rotation": 45, "z": 3}),
                    ("Pointing Hand", {"x": 290, "y": 130, "rotation": 45, "z": 2}),
                    ("Left Leg", {"x": 190, "y": 280, "rotation": 0, "z": 1}),
                    ("Right Leg", {"x": 210, "y": 280, "rotation": 0, "z": 1}),
                ]
            },
        ]

        for pose_data in poses_data:
            pose, created = PosePreset.objects.get_or_create(
                slug=pose_data["slug"],
                defaults={
                    "name": pose_data["name"],
                    "description": pose_data["description"],
                    "is_expression": pose_data["is_expression"],
                }
            )

            if created:
                self.stdout.write(f"  ✓ Created pose: {pose.name}")
            else:
                self.stdout.write(f"  • Exists: {pose.name}")

            # Create part configurations
            for part_name, config_data in pose_data["parts"]:
                if part_name in parts:
                    config, created = PartConfiguration.objects.get_or_create(
                        pose_preset=pose,
                        puppet_part=parts[part_name],
                        defaults={
                            "position_x": config_data["x"],
                            "position_y": config_data["y"],
                            "rotation": config_data["rotation"],
                            "z_index": config_data["z"],
                            "scale": 1.0,
                        }
                    )
                    if created:
                        self.stdout.write(
                            f"    ✓ Added part: {part_name}"
                        )

    def _seed_expressions(self):
        """Create preset facial expressions."""
        self.stdout.write("Seeding facial expressions...")

        parts = {
            part.name: part
            for part in PuppetPart.objects.all()
        }

        expressions_data: List[Dict] = [
            {
                "name": "Happy",
                "slug": "happy",
                "description": "Cheerful facial expression with smile",
                "is_expression": True,
                "parts": [
                    ("Eyes Happy", {"x": 185, "y": 110, "rotation": 0, "z": 10}),
                    ("Mouth Smile", {"x": 200, "y": 140, "rotation": 0, "z": 9}),
                ]
            },
            {
                "name": "Surprised",
                "slug": "surprised",
                "description": "Shocked or amazed facial expression",
                "is_expression": True,
                "parts": [
                    ("Eyes Surprised", {"x": 185, "y": 110, "rotation": 0, "z": 10}),
                    ("Mouth Open", {"x": 200, "y": 140, "rotation": 0, "z": 9}),
                ]
            },
            {
                "name": "Confident",
                "slug": "confident",
                "description": "Determined and confident facial expression",
                "is_expression": True,
                "parts": [
                    ("Eyes Confident", {"x": 185, "y": 110, "rotation": 0, "z": 10}),
                    ("Mouth Neutral", {"x": 200, "y": 140, "rotation": 0, "z": 9}),
                ]
            },
        ]

        for expr_data in expressions_data:
            expr, created = PosePreset.objects.get_or_create(
                slug=expr_data["slug"],
                defaults={
                    "name": expr_data["name"],
                    "description": expr_data["description"],
                    "is_expression": expr_data["is_expression"],
                }
            )

            if created:
                self.stdout.write(f"  ✓ Created expression: {expr.name}")
            else:
                self.stdout.write(f"  • Exists: {expr.name}")

            # Create part configurations
            for part_name, config_data in expr_data["parts"]:
                if part_name in parts:
                    config, created = PartConfiguration.objects.get_or_create(
                        pose_preset=expr,
                        puppet_part=parts[part_name],
                        defaults={
                            "position_x": config_data["x"],
                            "position_y": config_data["y"],
                            "rotation": config_data["rotation"],
                            "z_index": config_data["z"],
                            "scale": 1.0,
                        }
                    )
                    if created:
                        self.stdout.write(
                            f"    ✓ Added part: {part_name}"
                        )
